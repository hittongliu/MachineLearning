from numpy import *

def randCent(dataSet, k) :
  n = shape(dataSet)[1]
  centroids = mat(zeros((k, n)))
  p = 5
  for j in range(p):
    minj = min(dataSet[:, j])
    rangj = float(max(dataSet[:, j]) - minj)
    centroids[:, j] = minj + rangj * random.rand(k, 1)
  print(centroids)
  return centroids
