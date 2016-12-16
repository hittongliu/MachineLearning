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
  n = (shape(dataMat)[1])
  print (n)
  return dataMat

def distEclud(vecA, vecB) :
  return sqrt(sum((vecA - vecB) ** 2))

