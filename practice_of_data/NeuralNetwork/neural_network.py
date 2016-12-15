#-*- coding: utf-8 -*-
# 使用神经网络预测销量的高低

import pandas as pd

#参数初始化
inputfile = './sales_data.xls'
data = pd.read_excel(inputfile, index_col = u'序号')

data[data == u'好'] = 1
data[data == u'是'] = 1
data[data == u'高'] = 1
data[data != 1] = 0

x = data.iloc[:,:3].as_matrix().astype(int)
y = data.iloc[:,3].as_matrix().astype(int)

from keras.models import Sequential
from keras.layers.core import Dense, Activation

model = Sequential() #建立模型
model.add(Dense(10, input_dim = 3))
model.add(Activation('relu')) #用relu函数作为激活函数，能够大幅提供准确度
model.add(Dense(1))
model.add(Activation('sigmoid')) #由于是0-1输出，用sigmoid函数作为激活函

model.compile(loss = 'binary_crossentropy',
    optimizer = 'adam', class_mode = 'binary')
#训练模型,训练1000次，每次迭代的样本数目为10
model.fit(x, y, nb_epoch = 1000, batch_size = 10)
#预测
yp = model.predict_classes(x).reshape(len(y))
from cm_plot import *
cm_plot(y, yp).show()
