#-*- coding: utf-8 -*-
from numpy import *
def loadDataset():
  dataMat = []
  labelMat = []
  file = open('./testSet.txt')
  linestr = file.readlines()
  for line in linestr:
    str1 = line.strip().split()
    dataMat.append([1, float(str1[0]), float(str1[1])])
    labelMat.append(float(str1[2]))
  return dataMat, labelMat

def sigmode(inX):
  return 1.0/(1 + exp(-inX))

#简易版线性回归
def gradAscent(dataMat, labelMat):
  iter1 = 500
  alpha = 0.001 #更新的步长
  dataMat = mat(dataMat)
  labelMat = mat(labelMat).T
  m,n = shape(dataMat)
  weights = ones((n, 1))
  for i in range(iter1):
    h = sigmode(dataMat * weights)
    # 梯度下降法更新w，每次更新的大小为xi(yi-p1)
    # 用到了每个样本，迭代的次数为500次。
    error = labelMat - h
    weights = weights + alpha * dataMat.T * error
  print('over')
  print(weights)
  return weights

#随机线性回归
#每次随机选择一个样本更新
def randomAscent(dataMat, labelMat):
  dataMat = array(dataMat)
  m,n = shape(dataMat)
  weights = ones((n))
  numiter = 5
  for i in range(numiter):
    dataIndex = range(m)
    for j in range(m):
      alpha2 = 4 / (1.0 + j + i) + 0.01
      randindex = int(random.uniform(0, len(dataIndex)))
      h = sum(dataMat[randindex] * weights)
      error = labelMat[randindex] - sigmode(h)
      weights = weights + alpha2 * error * dataMat[randindex]
      del (dataIndex[randindex])
  return weights

#画图函数
def plotFit(weights):
  import matplotlib.pyplot as plt
  dataMat, labelMat = loadDataset()
  dataMat = array(dataMat)
  labelMat = array(labelMat)
  weights = array(weights)
  n = shape(dataMat)[0]
  xcord1 = []; ycord1 = []
  xcord2 = []; ycord2 = []
  for i in range(n):
    if (labelMat[i]) == 1:
      xcord1.append(dataMat[i, 1]);ycord1.append(dataMat[i, 2])
    else:
      xcord2.append(dataMat[i, 1]);ycord2.append(dataMat[i, 2])
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
  ax.scatter(xcord2, ycord2, s=30, c='green')
  x = arange(-3.0, 3.0, 0.1)
  y = (-weights[0]-weights[1]*x)/weights[2]
  ax.plot(x, y)
  plt.xlabel('X1'); plt.ylabel('X2');
  plt.show()






