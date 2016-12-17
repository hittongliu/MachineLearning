#-*- coding: utf-8 -*-
#使用聚类算法聚类消费者的行为

import pandas as pd

inputfile = './consumption_data.xls'
k = 3
iteration = 500
data = pd.read_excel(inputfile)

data_zs = 1.0*(data - data.mean())/data.std()
