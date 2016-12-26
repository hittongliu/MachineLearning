#-*- coding: utf-8 -*-
from __future__ import absolute_import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train_df = pd.read_csv('./input/train.csv', index_col = 0)
test_df = pd.read_csv('./input/test.csv', index_col = 0)
# print train_df.head()

# 对SalePrice做取log处理，看一下效果，log1p为了防止负值，画出直方图
prices = pd.DataFrame({"price":train_df["SalePrice"], "log(price+1)": np.log1p(train_df["SalePrice"])})
prices.hist()
# plt.show()

# 去掉最后一列房产价格，合并训练集和测试集作统一处理
y_train = np.log1p(train_df.pop('SalePrice'))
all_def = pd.concat((train_df, test_df), axis = 0)
# print all_def.shape
# # 处理GarageYrBlt数据
# all_def['GarageYrBlt'] = 2016 - all_def['GarageYrBlt']
# numpy_GarageYrBlt = list(all_def['GarageYrBlt'])
# out_GarageList = []
# # print all_def['GarageYrBlt']
# count1 = 0;count2 = 0;count3 = 0;count4 = 0;count5 = 0;count6 = 0;count7 = 0;count8 = 0;count9 = 0
# for x in numpy_GarageYrBlt:
#     if x >= 50: out_GarageList.append(1);count8 += 1
#     elif x >= 40: out_GarageList.append(2);count7 += 1
#     elif x >= 30: out_GarageList.append(3);count6 += 1
#     elif x >= 20: out_GarageList.append(4);count5 += 1
#     elif x >= 15: out_GarageList.append(5);count4 += 1
#     elif x >= 10: out_GarageList.append(6);count3 += 1
#     elif x >= 5: out_GarageList.append(7);count2 += 1
#     elif x >= 0: out_GarageList.append(8);count1 += 1
#     else: out_GarageList.append(0);count9 += 1
# sumn = float(len(out_GarageList))
# nonzero = sumn - count9
# count1 =  int(count1 / nonzero * count9)
# count2 =  int(count2 / nonzero * count9)
# count3 =  int(count3 / nonzero * count9)
# count4 =  int(count4 / nonzero * count9)
# count5 =  int(count5 / nonzero * count9)
# count6 =  int(count6 / nonzero * count9)
# count7 =  int(count7 / nonzero * count9)
# for i in range(int(sumn)):
#     if out_GarageList[i] == 0 and count1 > 0:out_GarageList[i] = 8;count1 -= 1;continue
#     elif out_GarageList[i] == 0 and count2 > 0:out_GarageList[i] = 7;count2 -= 1;continue
#     elif out_GarageList[i] == 0 and count3 > 0:out_GarageList[i] = 6;count3 -= 1;continue
#     elif out_GarageList[i] == 0 and count4 > 0:out_GarageList[i] = 5;count4 -= 1;continue
#     elif out_GarageList[i] == 0 and count5 > 0:out_GarageList[i] = 4;count5 -= 1;continue
#     elif out_GarageList[i] == 0 and count6 > 0:out_GarageList[i] = 3;count6 -= 1;continue
#     elif out_GarageList[i] == 0 and count7 > 0:out_GarageList[i] = 2;count7 -= 1;continue
#     elif out_GarageList[i] == 0 :out_GarageList[i] = 1

# all_def['GarageYrBlt'] = pd.Series(out_GarageList, index = all_def['GarageYrBlt'].index)
print all_def['GarageYrBlt']
# 把所有的标签都转换为01表示，比如属性A有三种取值，那么用100,010,001表示
# 所以列数会增多，本来79列，现在为303列
all_def['MSSubClass'] = all_def['MSSubClass'].astype(str)
all_dumpy_def = pd.get_dummies(all_def)
print all_dumpy_def.shape
mean_cols = all_dumpy_def.mean()
all_dumpy_def = all_dumpy_def.fillna(mean_cols)
print all_dumpy_def.isnull().sum().sum()

# 标准化numerical列,注意这里选取的是数据是all_def
numeric_col = all_def.columns[all_def.dtypes != 'object']
numeric_col_means = all_dumpy_def.loc[:, numeric_col].mean()
numeric_col_std = all_dumpy_def.loc[:, numeric_col].std()
all_dumpy_def.loc[:, numeric_col] = (all_dumpy_def.loc[:, numeric_col] - numeric_col_means) / numeric_col_std
# all_dumpy_def['GarageYrBlt'] = pd.Series(out_GarageList, index = all_def['GarageYrBlt'].index)
# 处理完毕 再讲数据拆分开
dumpy_train_df = all_dumpy_def.loc[train_df.index]
dumpy_test_df = all_dumpy_def.loc[test_df.index]
print dumpy_train_df.shape
print dumpy_test_df.shape

#模型测试
x_train = dumpy_train_df.values
x_test = dumpy_test_df.values
from sklearn.linear_model import Ridge
ridge = Ridge(15)

# from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import cross_val_score

# params = [1, 10, 15, 25, 30, 35, 40]
# test_scores = []
# for param in params:
#   clf = BaggingRegressor(n_estimators = param, base_estimator = ridge)
#   test_score = np.sqrt(-cross_val_score(clf, x_train, y_train, cv = 10, scoring='neg_mean_squared_error'))
#   test_scores.append(np.mean(test_score))
# plt.plot(params, test_scores)
# plt.show()
from xgboost import XGBRegressor
clf = XGBRegressor(max_depth = 5)
clf.fit(x_train, y_train)
y_rf = np.expm1(clf.predict(x_test))
test_score = np.sqrt(-cross_val_score(clf, x_train, y_train, cv=10, scoring='neg_mean_squared_error'))
print np.mean(test_score)

# from sklearn.linear_model import Ridge
# ridge = Ridge(15)
# from sklearn.ensemble import AdaBoostRegressor
# from sklearn.ensemble import BaggingRegressor

# clf2 = BaggingRegressor(n_estimators = 25, base_estimator=ridge)
# clf2.fit(x_train, y_train)
# y_rf2 = np.expm1(clf2.predict(x_test))
# y_rf = y_rf + y_rf2 / 2

submitt = pd.DataFrame(data = { 'SalePrice': y_rf,'id': test_df.index})
submitt.to_csv(path_or_buf = './out.csv', index = False)
# print submitt




