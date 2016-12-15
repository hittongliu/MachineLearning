#-*- coding: utf-8 -*-
import pandas as pd

#取出数据
filename = './sales_data.xls'
data = pd.read_excel (filename, index_col = u'序号')

data[data == u'是'] = 1
data[data == u'好'] = 1
data[data == u'高'] = 1
data[data != 1] = -1
x = data.iloc[:,:3].as_matrix().astype(int)
y = data.iloc[:,3].as_matrix().astype(int)

#建立决策模型，训练模型
from sklearn.tree import DecisionTreeClassifier as DTC
dtc = DTC(criterion = 'entropy')
dtc.fit(x, y)
yp = dtc.predict(x).reshape(len(y))
from cm_plot import *
cm_plot(y, yp).show()

#为了可视化的输出，输出为dot文件
from sklearn.tree import export_graphviz
x = pd.DataFrame(x)
from sklearn.externals.six import StringIO
with open("tree.dot", 'w') as f:
  f = export_graphviz(dtc, feature_names = x.columns, out_file = f)

