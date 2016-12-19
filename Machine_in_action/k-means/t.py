#-*- coding: utf-8 -*-
from numpy import *
from numpy.random.mtrand import power

def loadDataSet(filename) :
  dataMat = []
  fr = open(filename)
  for line in fr.readlines() :
    curLine = line.strip().split() #split()默认按照所有的空格/换行符／制表符进行分割，strip()返回除去两侧范围的字符串
    fltLine = map(float, curLine)
    dataMat.append(fltLine)
# print(dataMat)
  n = (shape(dataMat)[1]) #shape()返回矩阵的行数和列数,[1]返回列数
  # print (n)
  return dataMat

def distEclud(vecA, vecB) :
  return sqrt(sum((vecA - vecB) ** 2))

def randCent(dataSet, k) :
  # k个中心，每个中心的维度要和dataset的维度一致。
  # 要生成K*n的聚类中心
  n = shape(dataSet)[1]
  centroids = mat(zeros((k, n)))
  for j in range(n):
    minj = min(dataSet[:, j])
    rangj = float(max(dataSet[:, j]) - minj)
    centroids[:, j] = minj + rangj * random.rand(k, 1)
  # print(centroids)
  return centroids

def kMeans(dataSet, k, distMeas = distEclud,
  createCent = randCent) :
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m, 2)))
  centroids = createCent(dataSet,k)
  clusterChanged = True
  while clusterChanged :
    clusterChanged = False
    for i in range(m) :
      mini = inf; mindex = -1
      for j in range(k) :
        dist = distMeas(dataSet[i, :].A,centroids[j, :].A)
        if dist < mini :
          mini = dist
          mindex = j
      if clusterAssment[i,0] != mindex : clusterChanged = True
      clusterAssment[i,:] = mindex, mini **2
    print(clusterChanged)
    print(centroids)
    for cent in range(k) :
      temp = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
      centroids[cent,:] = mean(temp, axis = 0)
  print(clusterAssment)
  return centroids, clusterAssment






