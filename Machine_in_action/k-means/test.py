from t import *
from numpy import mat

dataMat = mat (loadDataSet('./test.txt'))
k = 4
mycentroies, cluster = kMeans(dataMat, k)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data1 = dataMat[nonzero(cluster[:,0].A == 0)[0]]
print(data1)
print('h9')
data2 = dataMat[nonzero(cluster[:,0].A == 1)[0]]
print(data2)
print('zhn')
data3 = dataMat[nonzero(cluster[:,0].A == 2)[0]]
print(data3)
data4 = dataMat[nonzero(cluster[:,0].A == 3)[0]]

plt.plot(data1[:, 0], data1[:, 1], 'r.')
plt.plot(data2[:, 0], data2[:, 1], 'go')
plt.plot(data3[:, 0], data3[:, 1], 'b*')
plt.plot(data4[:, 0], data4[:, 1], 'y+')

plt.plot(mycentroies[0, 0], mycentroies[0, 1], 'ro')
plt.plot(mycentroies[1, 0], mycentroies[1, 1], 'g.')
plt.plot(mycentroies[2, 0], mycentroies[2, 1], 'b+')
plt.plot(mycentroies[3, 0], mycentroies[3, 1], 'y*')

plt.show()