from kNN import *

train_x, train_y, test_x, test_y = loaddataSet()

numberTest = test_x.shape[0]
trueCount = 0;
for i in range(numberTest) :
  print('predict the testlist i :')
  print(i)
  label = KNNClassify(test_x[i, :], train_x, train_y, 3)
  print (label)
  if label == test_y[i] : trueCount += 1; print('predict true')

accuracy = float(trueCount) / numberTest

print(accuracy)