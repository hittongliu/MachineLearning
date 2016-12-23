from Logregress import *

dataMat, labelMat = loadDataset()
weights = randomAscent(dataMat, labelMat)
plotFit(weights)