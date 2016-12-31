#-*- coding: utf-8 -*-
from numpy import *

# load the dataSet
# 数据最后一列为预测的值。


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        linestr = line.strip().split()
        fltLine = map(float, linestr)
        dataMat.append(fltLine)
    return dataMat

# 三个参数：数据集合，待切分的特征和该特征的某个值。
# 将数据切分得到两个子集并返回


def binSplitDataSet(dataSet, feature, value):
    dataSet = mat(eye(4))
    mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    print mat1
    return mat0, mat1

# 叶子节点创建函数，数据最后一列为要预测的数值。直接取均值作为最后的预测结果


def regLeaf(dataSet):
    return mean(dataSet[:, -1])

# 误差计算函数，当前小集合中所有预测值的平方误差。
# 因为是会以当前集合的均值作为初步的预测值的，看这个预测值的误差是不是符合要求。


def regErr(dataSet):
    return var(dataSet[:, -1]) * shape(dataSet)[0]


# 创建一棵树，四个参数，leaftype为叶子节点创建函数，errtype误差计算函数
# 每次调用chooseBestSplit选择策略，如果可以继续分裂，分裂后得到的左右子树继续分裂。
def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat == None:
        return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lset, rset = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lset, regLeaf, regErr, ops)
    retTree['right'] = createTree(rset, regLeaf, regErr, ops)
    return retTree

# 选择当前的最佳策略
# 返回可分类的特征和分类的特征值。可按照是否大于这个特征值将集合分为两类
# ops[0]表示当前分裂减小的误差最低要满足的条件，大于ops[0]才会进行继续分裂。
# ops[1]表示切分的最小的样本数目。


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    tols = ops[0]
    tolN = ops[1]
    # 如果所有值相等则退出
    if len(set(dataSet[:, -1].T.tolist())) == 1:
        return None, leafType(dataSet)  # 默认的选取策略为当前集合的均值
    m, n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf
    bestIndex = 0
    bestValue = 0
    for i in range(n - 1):
        iset = set(dataSet[:, i])
        for splitvalue in iset:
            mat0, mat1 = binSplitDataSet(dataSet, i, splitvalue)
            err0 = errType(mat0)
            err1 = errType(mat1)
            if (err0 + err1) < bestS:bestS = err0 + err1;bestIndex = i;bestValue = splitvalue
    if (S - bestValue) < tols:return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat[1])[0] < tolN):
      return None, leafType(dataSet)  # 如果切分之后的数据数目小于tolN，那么也不继续分裂
    return bestIndex, bestValue


# 利用测试集进行剪枝处理
def isTree(obj):
  return (type(obj).__name__ == 'dict')

def getMean(tree):
  if isTree(tree['right']):tree['right'] = getMean(tree['right'])
  if isTree(tree['left']):tree['left'] = getMean(tree['left'])
  return (tree['left'] + tree['right']) / 2.0

# 利用树在测试集上进行回归预测，直到发现当前节点的左右节点都是叶子，这个时候判断是否合并。
# 判断的标准是，测试集在当前的表现和合并后的表现
def prune(tree, testData):
  if shape(testData) == 0:return getMean(tree) #测试集在当前节点分配的个数为０，回收全部节点
  if isTree[tree['left']] or isTree[tree['right']]:
    lset, rset = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
  if isTree(tree['left']):prune(tree['left'], lset)
  if isTree(tree['right']):prune(tree['right'], lset)
  if not isTree(tree['left']) and not isTree(tree['right']):
    lset, rset = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    treeMean = (tree['left'] + tree['right']) / 2.0
    errMerge = sum(power(testData[:, -1] - treeMean, 2))
    errNoMerge = sum(power(lset[:, -1] - tree['left'], 2)) + sum(power(rset[:, -1] - tree['right'], 2))
    # 判断是否merge，如果merge，就变成叶子节点，返回。如果不merge，就返回当前的树。
    if errNoMerge > errMerge:
      return treeMean
    else:return tree
  return tree