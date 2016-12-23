#-*- coding: utf-8 -*-
from numpy import *
def loadDataSet():
    return [[1, 3, 4, 6], [2, 4, 3, 5, 6], [1, 2, 3, 5, 6], [2, 4, 5, 6]]

# return the elements of dataSet
# C1 = set([1, 2, 3, 4, 5)


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1 = map(frozenset, C1)
    return C1

# delete the Ck elements not active
# the origin dataSet is D


def scanD(D, Ck, minSupport):
    Ssan = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                Ssan[can] = Ssan.get(can, 0) + 1
    number = float(len(D))
    supportData = {}
    retlist = []
    for key in Ssan:
        count = Ssan[key]
        percent = float(count / number)
        if percent >= minSupport:
            retlist.append(key)
        supportData[key] = percent
    return retlist, supportData

# create Ck by Lk,
# Lk = ([1, 2,3]) then
# CK = set([1,2], [1,3], [2,3])


def aprioriGen(Lk, k):
    lenlk = len(Lk)
    Cklist = []
    for i in range(lenlk):
        data1 = list(Lk[i])[:k-2]
        for j in range(i+1, lenlk):
            data2 = list(Lk[j])[:k-2]
            data1.sort()
            data2.sort()
            if data1 == data2:
                Cklist.append(Lk[i] | Lk[j])
    return Cklist

# get the data


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = aprioriGen(L[k-2], k)
        Lk, supportk = scanD(D, Ck, minSupport)
        supportData.update(supportk)
        L.append(Lk)
        k += 1
    return L, supportData


def calcConf(freqSet, H, supportData, br1, minConf=0.7):
  # '''
  # 计算规则的可信度，返回满足最小可信度的规则。
  # freqSet(frozenset):频繁项集
  # H(frozenset):频繁项集中所有的元素
  # freqset-H / H
  # supportData(dic):频繁项集中所有元素的支持度
  # brl(tuple):满足可信度条件的关联规则
  # minConf(float):最小可信度
  # '''
  prunedH = []
  for conseq in H:
    conf = supportData[freqSet] / supportData[freqSet - conseq]
    if conf >= minConf:
      print freqSet-conseq, '----->', conseq, 'conf: ', conf
      br1.append((freqSet - conseq, conseq, conf))
      prunedH.append(conseq)
  return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf = 0.7):
    # '''
    # 对频繁项集中元素超过2的项集进行合并。
    # freqSet(frozenset):频繁项集
    # H(frozenset):频繁项集中的所有元素，即可以出现在规则右部的元素
    # supportData(dict):所有项集的支持度信息
    # brl(tuple):生成的规则
    # '''
  m = len(H[0])
  print "m: ", m
  if len(freqSet) > m+1:
    Hmp1 = aprioriGen(H, m+1)
    print "Hmp1: ", Hmp1
    Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
    if (len(Hmp1) > 0):
      rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

def generateRules(L, supportData, minConf = 0.7):
    # '''
    # 根据频繁项集和最小可信度生成规则。
    # L(list):存储频繁项集
    # supportData(dict):存储着所有项集（不仅仅是频繁项集）的支持度
    # minConf(float):最小可信度
    # '''
  bigRuleList = []
  for i in range(1, len(L)):
    for freqSet in L[i]:
      H1 = [frozenset([item]) for item in freqSet]
      print "i: ", i, "H1 :", H1
      if i >1:
        calcConf(freqSet, H1, supportData, bigRuleList, minConf)
        rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
      else:
        calcConf(freqSet, H1, supportData, bigRuleList, minConf)
  return bigRuleList

