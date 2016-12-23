from apriori import *

dataSet = loadDataSet()
L, supportData = apriori(dataSet)
print L[0]
print L[1]
print L[2]
print L[3]
bigRuleList = generateRules(L, supportData, 0.7)