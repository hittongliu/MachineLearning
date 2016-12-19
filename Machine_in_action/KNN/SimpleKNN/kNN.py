#-*- coding: utf-8 -*-

from numpy import *
import operator

def createDataSet() :
  # create a matrix for learning
  group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
  labels = ['A', 'A', 'B', 'B']
  return group, labels

# classify the input data for using KNN
# dataSet = [ [, , , , , , ,],
#                   [, , , , , , ,],
#                   [, , , , , , ,],
#                 ]
# newInput=[, , , , , , ,]
def KNNClassify(newInput, dataSet, labels, k) :
  numSamples = dataSet.shape[0]

  # calculte Euclidean distance
  diff = tile(newInput, (numSamples, 1)) - dataSet
  squarediff = diff ** 2
  squareDist = sum(squarediff, axis = 1)
  distanceList = squareDist ** 0.5

  # sort the distance return the index
  sortindex = argsort(distanceList)

  classCount = {}
  for i in range(k) :
    label = labels[sortindex[i]]
    classCount[label] = classCount.get(label, 0) + 1

  maxCount = 0
  for key, value in classCount.items() :
    if value > maxCount :
      maxCount = value
      maxIndex = key
  return maxIndex
