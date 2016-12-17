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

#构造CART决策树模型
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier()
tree.fit(train[:,:3], train[:, 3])
predict_result = tree.predict(train[:, :3]).reshape(len(train))
from cm_plot import *
cm_plot(train[:, 3], predict_result)
test_result = tree.predict(test[:, :3]).reshape(len(test))
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






