def randCent(dataSet, k) :
  n = shape(dataSet)[1]
  centroids = mat(zeros((k, n))
  for j in range(n):
    minj = min(dataSet[:, j])
    rangj = float(max(dataSet[:, j]) - minj)
    centroids[:, j] = minj + rangj * random.rand(k, 1)
  print(centroids)
  return centroids
