#-*- coding: utf-8 -*-
from __future__ import absolute_import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train_df = pd.read_csv('./input/train.csv', index_col = 0)
test_df = pd.read_csv('./input/test.csv', index_col = 0)
# print train_df.head()

# 对SalePrice做取log处理，看一下效果，log1p为了防止负值，画出直方图
prices = pd.DataFrame({"TotalBsmtSF":train_df["TotalBsmtSF"], "log(TotalBsmtSF+1)": np.log1p(train_df["TotalBsmtSF"])})
prices.hist()
plt.show()
mins = train_df['GarageYrBlt'].min()
print train_df['GarageYrBlt']
train_df['GarageYrBlt'] = 2016 - train_df['GarageYrBlt']
numpy_GarageYrBlt = list(train_df['GarageYrBlt'])
out_GarageList = []
# print train_df['GarageYrBlt']
count1 = 0;count2 = 0;count3 = 0;count4 = 0;count5 = 0;count6 = 0;count7 = 0;count8 = 0;count9 = 0
for x in numpy_GarageYrBlt:
    if x >= 50: out_GarageList.append(1);count8 += 1
    elif x >= 40: out_GarageList.append(2);count7 += 1
    elif x >= 30: out_GarageList.append(3);count6 += 1
    elif x >= 20: out_GarageList.append(4);count5 += 1
    elif x >= 15: out_GarageList.append(5);count4 += 1
    elif x >= 10: out_GarageList.append(6);count3 += 1
    elif x >= 5: out_GarageList.append(7);count2 += 1
    elif x >= 0: out_GarageList.append(8);count1 += 1
    else: out_GarageList.append(0);count9 += 1
sumn = float(len(out_GarageList))
nonzero = sumn - count9
count1 =  int(count1 / nonzero * count9)
count2 =  int(count2 / nonzero * count9)
count3 =  int(count3 / nonzero * count9)
count4 =  int(count4 / nonzero * count9)
count5 =  int(count5 / nonzero * count9)
count6 =  int(count6 / nonzero * count9)
count7 =  int(count7 / nonzero * count9)
for i in range(int(sumn)):
    if out_GarageList[i] == 0 and count1 > 0:out_GarageList[i] = 8;count1 -= 1
    elif out_GarageList[i] == 0 and count2 > 0:out_GarageList[i] = 7;count2 -= 1
    elif out_GarageList[i] == 0 and count3 > 0:out_GarageList[i] = 6;count3 -= 1
    elif out_GarageList[i] == 0 and count4 > 0:out_GarageList[i] = 5;count4 -= 1
    elif out_GarageList[i] == 0 and count5 > 0:out_GarageList[i] = 4;count5 -= 1
    elif out_GarageList[i] == 0 and count6 > 0:out_GarageList[i] = 3;count6 -= 1
    elif out_GarageList[i] == 0 and count6 > 0:out_GarageList[i] = 2;count7 -= 1
    elif out_GarageList[i] == 0 :out_GarageList[i] = 1
print out_GarageList
train_df['GarageYrBlt'] = pd.Series(out_GarageList, index = train_df['GarageYrBlt'].index)
print train_df['TotalBsmtSF']
print train_df['TotalBsmtSF'].value_counts()
# print mins
# data = (train_df['GarageYrBlt'].value_counts(ascending = True))
# print data
# data.to_csv(path_or_buf = './data1.csv', index = False)
