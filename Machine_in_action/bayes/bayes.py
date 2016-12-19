#-*- coding: utf-8 -*-

from numpy import *

def loadDataSet():
  # 该数据取自某狗狗论坛的留言版
  postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr','licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'h'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
  # 标注每条数据的分类，这里0表示正常言论，1表示侮辱性留言
  classVec = [0,1,0,1,0,1]
  return postingList,classVec

def createVocabList(dataSet) :
  vocabSet = set([])
  for docment in dataSet:
    vocabSet = vocabSet | set(docment)
  return list(vocabSet)

# 生成词条向量
def setOfWords2Vec(vocabList, inputset) :
  returnVec = [0]*len(vocabList)
  for word in vocabList :
    if word in inputset :
      returnVec[vocabList.index(word)] = 1;
  return returnVec

# 贝叶斯训练函数
def trainNB0(trainMatrix, trainCategory) :
  numTrainDocs = len(trainMatrix)
  numWords = len(trainMatrix[0])
  pAb = sum(trainCategory)/float(numTrainDocs)
  p0Num = ones(numWords); p1Num = ones(numWords)
  p0Denom = 2.0; p1Denom = 2.0
  for i in range(numTrainDocs) :
    if (trainCategory[i] == 1) :
      p1Num += trainMatrix[i]
      p1Denom += sum(trainMatrix[i])
    else :
      p0Num += trainMatrix[i]
      p0Denom += sum(trainMatrix[i])
  p1Vect = p1Num/p1Denom
  p1Vect = log(p1Vect)
  p0Vect = p0Num/p0Denom
  p0Vect = log(p0Vect)
  return p1Vect, p0Vect, pAb

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1) :
  p1 = sum(vec2Classify * p1Vec) + log(pClass1)
  p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
  print(p1)
  print(p0)
  if p1 > p0 :
    print('脏话')
    return 1
  else :
    print('好听的')
    return 0















