from platSmo import *

dataMat, labelMat = loadDataSet('./testSet.txt')
b, a = smoP(dataMat, labelMat, 0.6, 0.001, 40)