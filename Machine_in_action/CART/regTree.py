#-*- coding: utf-8 -*-

# 根据给定的一堆数据生成线性的预测
def linearSolve(dataSet):
  m, n = shape(dataSet)
  X = mat(ones(m,n)); Y = mat(ones(m,1))
  X[:,1:n] = dataSet[:,0:n-1]
  Y = dataSet[:, -1]
  xTx = X.T * X
  if linalg.det(xTx) == 0.0:
    raise NameError
  ws = xTx.I * (X.T * Y)
  return ws, X, Y

# 在叶子节点上生成线性模型
def modelLeaf(dataSet):
  ws, X, Y = linearSolve(dataSet)
  return ws

# 误差的计算。
def modelErr(dataSet):
  ws, X, Y = linearSolve(dataSet)
  yHat = X * ws
  return sum(power(Y - yHat, 2))