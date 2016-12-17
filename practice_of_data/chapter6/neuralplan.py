#-*- coding: utf-8 -*-
# 神经网络模型预测用户是否偷电
# 三个指标：电量下降趋势，线损，告警类指标

import pandas as pd
from random import shuffle #导入随机函数，打乱数据

inputfile = './model.xls'
data = pd.read_excel(inputfile)

data = data.as_matrix()
shuffle(data)

p = 0.8 #提取的训练数据比例，后百分之20为测试集
train = data[:int(len(data)*p), :]
test = data[int(len(data)*p):, :]

#应用神经网络算法
from keras.models import Sequential
from keras.layers.core import Dense, Activation

net = Sequential()
net.add(Dense(10, input_dim = 3))
net.add(Activation('relu')) #用relu函数作为激活函数，能够大幅提供准确度
net.add(Activation('relu'))
net.add(Dense(1))
net.add(Activation('sigmoid'))
net.compile(loss = 'binary_crossentropy', optimizer
    = 'adam', class_mode = 'binary')
net.fit(train[:,:3], train[:, 3], nb_epoch = 300,
    batch_size = 40)

predict_result = net.predict_classes(train[:, :3]).reshape(len(train))
from cm_plot import *
cm_plot(train[:, 3], predict_result)
test_result = net.predict_classes(test[:, :3]).reshape(len(test))
cm_plot(test[:, 3], test_result)

from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
fpr, tpr, thresholds = roc_curve(test[:, 3], test_result, pos_label = 1)
plt.plot(fpr, tpr, linewidth = 2, label = 'ROC of LM')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.ylim(0, 1.05)
plt.xlim(0, 1.05)
plt.legend(loc=4)
plt.show()






