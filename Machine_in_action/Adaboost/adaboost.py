#-*- coding: utf-8 -*-

from numpy import *
from pandas import *

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels


# 首先定义根据给定的特征(dimen)和特征值(threshVal)分裂的函数
def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
  retArray = ones((dataMatrix.shape[0], 1))
  if threshIneq == 'lt':
    retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
  else:
    retArray[dataMatrix[:, dimen] > threshVal] = -1.0
  return retArray

# 单层决策树生成函数，dataArr为输入数组，classLabels为类别
# D为权重向量，计算误差时候用的，根据误差选择当前最佳的分裂特征和特征值
def buildStump(dataArr, classLabels, D):
  dataMatrix = mat(dataArr);labelMat = mat(classLabels).T
  m,n = shape(dataMatrix)
  numSteps = 10.0;bestStump = {};bestClasEst = mat(zeros((m,1)))
  minError = inf
  """
  三层循环，最外层从所有的特征开始遍历.
  第二层循环遍历特征值，这里不是按照CART算法的方式全部遍历，而是从该列最小值开始，设定一个步长。
  第三层用于选择是正向还是反向。因为这里要预测的结果是１和－１，并不是连续值，不能按照CART算法那样直接按照所有值的均值来预测。
  """
  for i in range n:
    rangeMin = dataMatrix[:,i].min();rangeMax = dataMatrix[:, i].max()
    stepSize = (rangeMax - rangeMin) / numSteps
    for j in range(-1, int(numSteps) + 1):
      threshVal = rangeMin + float(j) * stepSize
      for k in ['lt', 'gt']:
        predictedVals = stumpClassify(dataMatrix, i, threshVal, k)
        errArr = mat(ones((m,1)))
        errArr[predictedVals == classLabels] = 0
        weightedErr = D.T * errArr
        if weightedErr < minError:
          minError = weightedErr
          bestClasEst = predictedVals.copy()
          bestStump{'dim'} = i
          bestStump{'thresh'} = threshVal
          bestStump{'ineq'} = k
  # 返回保存了分裂所用到的特征和阈值的bestStump,预测结果bestClasEst
  return bestStump, minError, bestClasEst

# 基于单层决策树的算法，设定迭代次数，迭代更新权重向量D。
# 每一次根据向量D分类的结果都保存在weekClassArr中。
def adaBoostTrainDS(dataArr, classLabels, numIt = 40):
  weakClassArr = []
  m = shape(dataArr)[0]
  D = mat(ones((m,1)) / m)
  aggClassEst = mat(zeros((m,1)))
  for i in range(numIt):
    bestStump,error,classEst = buildStump(dataArr,classLabels,D)
    print "D:",D.T
    alpha = float(0.5*log((1.0 - error) / max(error,1e-16)))
    bestStump['alpha'] = alpha
    weekClassArr.append(bestStump)
    print "classEst:", classEst.T
    expon = multiply(-1*alpha*mat(classLabels).T,classEst)
    D = multiply(D, exp(expon))
    D = D / D.sum()
    # 计算当前的错误率，如果错误率为0，那么就终止迭代。
    # 这里的sign(aggClassEst)就是最终的结果
    aggClassEst += alpha * classEst
    aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
    errorRate = aggErrors.sum() / m
    print "total errorRate:", errorRate, "\n"
    if errorRate == 0.0:break
  return weekClassArr

#adaboost分类函数，这里的输入
def adaClassify(datToClass, classifierArr):
  dataMatrix = mat(datToClass)
  m = shape(dataMatrix)[0]
  aggClassEst = mat(zeros((m,1)))
  for i in range(len(classifierArr)):
    classEst = stumpClassify(dataMatrix, classifierArr[i]['dim'], classifierArr[i]['thresh'], classifierArr[i]['ineq'])
    aggClassEst += classifierArr[i]['alpha'] * classEst
    print aggClassEst
  return sign(aggClassEst)


































