#########################################
# kNN: k Nearest Neighbors
# Input:      inX: vector to compare to existing dataset (1xN)
#             dataSet: size m data set of known vectors (NxM)
#             labels: data set labels (1xM vector)
#             k: number of neighbors to use for comparison
# Output:     the most popular class label
#########################################

from numpy import *
import os

# convert image to vector
def img2vector(filename) :
  rows = 32
  cols =  32
  imgVector = zeros((1, rows * cols))
  fileIn = open(filename)
  for row in range(rows) :
    line = fileIn.readline()
    for col in range(cols) :
      imgVector[0 , row * 32 + col] = int(line[col])
  return imgVector

def loaddataSet() :
  file = './digits/'

  print "---Getting training set..."
  trainingDigits = os.listdir(file + 'trainingDigits')
  numlist = len(trainingDigits)

  train_x = zeros((numlist, 1024))
  train_y = []

  for i in range(numlist) :
    filename = trainingDigits[i]
    train_x[i, :] = img2vector(file + 'trainingDigits/' + filename)
    label = filename.split('_')[0]
    train_y.append(label)

  print "---Getting testing set..."
  testDigits = os.listdir(file + 'testDigits')
  testnumlist = len(testDigits)

  test_x = zeros((testnumlist, 1024))
  test_y = []

  for i in range(testnumlist) :
    testfilename = testDigits[i]
    test_x[i, :] = img2vector(file + 'trainingDigits/' + testfilename)
    testlabel = testfilename.split('_')[0]
    test_y.append(testlabel)
  return train_x, train_y, test_x, test_y

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