#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 22:51:00 2018
sns.set_palette('dark')    
@author: alena
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 
#%%
sns.set_style("darkgrid")
sns.set_color_codes()
sns.set_palette('muted') 

font = {'family' : 'serif',
        'serif' : 'Times New Roman', 'size' : 17}
plt.rc('font', **font)
#%%
#1
data0 = pd.read_csv('railways201208.csv') 
stations0 = pd.read_csv('stations.csv')

dat = pd.DataFrame(data0)
stations = pd.DataFrame(stations0)

print(dat.head())
print(stations.head())
#%%
#2
dat['log Distance'] = dat['dist'].apply(np.log)
#%%
# график для расстояния          
fig = plt.figure(figsize=(9, 7))
sns.distplot(dat['dist'], bins = 86,kde=True,
             kde_kws={"color": "g", "lw": 3, "label": "log Distance", "shade":True},
             hist_kws={"histtype": "stepfilled","alpha": 1, "color": "b"}) 
plt.show()
#fig.savefig('pic1.pdf')
#%%
# график для логарифмов расстояния
fig = plt.figure(figsize=(10, 7))
sns.distplot(dat['log Distance'], bins = 88,kde=True,
             kde_kws={"color": "g", "lw": 3, "label": "log Distance", "shade":True},
             hist_kws={"histtype": "stepfilled","alpha": 1, "color": "b"})
plt.show()
#fig.savefig('pic2.pdf')
#%%
#3   
# создаем столбец с буквенными обозначениями типов грузов
dat['commodity1'] = dat['commodity']

dict={1:'Coal', 2:'Oil', 3:'Ores', 4:'Metals',5:'Wood', 
      6:'Constructions', 7:'Fertilizers', 8:'Grains', 
      9:'Petrol', 10:'Other'}

for i in dict.keys():
    dat['commodity'].replace(i, value=dict[i], inplace=True )
    
dat = dat.rename(columns={'commodity':'Commodity type'}) 
dat = dat.set_index('commodity1')
dat = dat.sort_index(axis = 0)
#%%
#boxplot
fig = plt.figure(figsize=(10, 8))
sns.boxplot(x='Commodity type', y='log Distance', data=dat,linewidth=3.5)
plt.xticks(rotation='vertical')
plt.show()
#fig.savefig('pic3.pdf',bbox_inches = 'tight')
#%%
#4
#plt.rc('font', family='serif')
dat = dat.set_index('Commodity type')
dat1 = dat.copy()

# создаем столбец с медианами
for i in dat1.index.unique():
    dat1.loc[i,'median'] = int(dat1.loc[i,'weight'].median())

# создаем колонку с разделением на Light/Heavy
dat1['Weight'] = dat1['weight'] - dat1['median']
dat1['median'] = dat1['median'].astype(int)

def compare(x):
    x = int(x)
    if x > 0:
        return('Heavy')
    elif x < 0:
        return('Light')
    else:
        return('Light')
         
dat1['Weight'] = dat1['Weight'].apply(compare)

#%%
fig = plt.figure(figsize=(9, 7))
sns.violinplot(x=dat1.index, y='log Distance',
               hue='Weight', hue_order=['Light','Heavy'], split=True,
               data=dat1,linewidth=3)
plt.xticks(rotation='vertical')
plt.legend(title='Weight',loc='lower right')
plt.show()
#fig.savefig('pic4.pdf',bbox_inches = 'tight')

#%%
#5
# создаем нужные столбцы
dat1.dtypes
dat1['weight'] = dat1['weight'].astype(float)
dat1['dist'] = dat1['dist'].astype(float)

dat1 = dat1[dat1['amount'].notnull()]

dat1['log(weight*dist)'] = np.log(dat1['weight']*dat1['dist'])
dat1['log(amount)'] = np.log(dat1['amount']) 

dat1 = dat1[dat1['log(amount)'].notnull()]

#%%
dat2 = dat1.copy()
dat2 = dat2.reset_index()
dat2 = dat2.set_index('amount')
dat2.drop(dat2[dat2.index == 0].index, inplace=True)
len(dat2)

g = sns.jointplot(x='log(weight*dist)',y='log(amount)', data=dat2, kind='reg')
g.fig.set_figwidth(8)
g.fig.set_figheight(7)
g.savefig('pic5.svg',bbox_inches = 'tight')
plt.show()



