#-*- coding: utf-8 -*-
#使用聚类算法聚类消费者的行为

import pandas as pd

inputfile = './consumption_data.xls'
outputfile = './data_output.xls'
k = 4
iteration = 500
data = pd.read_excel(inputfile, index_col = 'Id')

data_zs = 1.0*(data - data.mean())/data.std()

from sklearn.cluster import KMeans
model = KMeans(n_clusters = k, n_jobs = 4, max_iter = iteration)
model.fit(data_zs)

r1 = pd.Series(model.labels_, index = data.index)
# print(data_zs)
r2 = pd.DataFrame(model.cluster_centers_)
print(r2)

r = pd.concat([data, r1], axis = 1)
r.columns = list(data.columns) + [u'聚类类别']
r.to_excel(outputfile)

# TSNE 展示结果
from sklearn.manifold import TSNE

tsne = TSNE()
tsne.fit_transform(data_zs)
tsne = pd.DataFrame(tsne.embedding_, index = data_zs.index)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

d = tsne[r[u'聚类类别'] == 0]
plt.plot(d[0], d[1], 'r.')
d = tsne[r[u'聚类类别'] == 1]
plt.plot(d[0], d[1], 'go')
d = tsne[r[u'聚类类别'] == 2]
plt.plot(d[0], d[1], 'b*')
plt.show()












