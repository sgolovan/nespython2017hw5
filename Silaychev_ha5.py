#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 14:14:23 2018

@author: silis123
"""

#Загружаем библиотеки
import requests
import zipfile
import io
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from mpl_toolkits.basemap import Basemap
#%%
#Задание 1.1
r = requests.get('https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM', auth=('user', 'pass'))
fname = 'developer_survey_2017'
path = r
csv1 = 'survey_results_public'
csv2 = 'survey_results_schema'
zf = zipfile.ZipFile(io.BytesIO(r.content)) #Анзипаем скачанный датасет и считываем в два разных csv
zf.extractall()
data = pd.read_csv(zf.open(csv1 + '.csv'), header=0)
schema = pd.read_csv(zf.open(csv2 + '.csv'), header=0)
data = pd.read_csv(zf.open(csv1 + '.csv'), header=0)
schema = pd.read_csv(zf.open(csv2 + '.csv'), header=0)
#%%
schema.head()
len(schema) #количество вопросов
#%%
data.iloc[:,:2].head()
len(data) #количество респондентов
#%%
#задание 1.2
plt.figure(figsize = (18,25)) #использую код с семинара
m = Basemap(projection='cyl',llcrnrlat=35,urcrnrlat=84,
            llcrnrlon=15,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='peru',lake_color='aqua')

m.drawmapboundary(fill_color='aqua')

plt.title("Map for task 2 \n", fontsize=18) #задаю название
plt.show()
#%%
#Задание 1.3

#Задаем ссылку на таблицу
url = "https://developers.google.com/public-data/docs/canonical/countries_csv" 
#парсим
tablesbables = pd.read_html(url, index_col=0)[0]
tablesbables = tablesbables.drop(tablesbables[(tablesbables[1] == 'latitude')].index)
tablesbables = tablesbables.dropna()
tablesbables.replace(np.nan, "NA")
tablesbables.rename(columns = {0 : 'name',1 : 'latitude',2: 'longtitude', 3 : 'Country'}, inplace = True)

#%%
data3 = tablesbables.copy() #копирую на всякий случай, чтобы не испортить начальный датасет

#%%
#код с семинара
plt.figure(figsize = (25,25))
m3 = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m3.drawcoastlines(linewidth=0.25, antialiased = True)
m3.drawcountries(linewidth=0.25, antialiased = False) 
m3.fillcontinents(color='peru',lake_color='aqua')

m3.drawmapboundary(fill_color='aqua') 


for i, j in data3.iterrows(): #это нужно для того, чтобы пройтись по каждой строке датасета и найти все координаты и названия каждой страны, затем прикрепить их к карте 

    lon = j['longtitude']
    lat = j['latitude']
    xpt,ypt = m3(lon,lat)
    lonpt, latpt = m3(xpt,ypt,inverse=True)
    m3.plot(xpt,ypt,'bo', zorder=10, markersize=5)
    plt.text(xpt,ypt, i)

plt.show()

#%%
#Задание 1.4
plt.figure(figsize = (25,25))
coord = {'left_lon': -180,'right_lon': 180, 'left_lat': -90, 'right_lat': 90 } #здесь мне стало интересно попробовать как в примере с африкой, вроде получилось, но не пригодилось
m4 = Basemap(projection='cyl',llcrnrlat=coord['left_lat'],
            urcrnrlat=coord['right_lat'],
            llcrnrlon=coord['left_lon'], urcrnrlon=coord['right_lon'],resolution='c')

m4.drawcoastlines()
m4.drawcountries(linewidth=0.25, antialiased = False)
m4.fillcontinents(color='peru',lake_color='aqua')

m4.drawmapboundary(fill_color='aqua')

#не удержался и использовал начальный датасет, shame on me
#беру код из прошлого задания и немного его исправляю
task4df = data.groupby(['Country']).count().sort_values(['Respondent'], ascending = False)['Respondent']

df4 = pd.DataFrame({'Country' : task4df.index, 'Total' : task4df.values}, index = None)
#совмещаю по Country
merged4 = pd.merge(data3, df4, how='inner', on=['Country'])
#координаты для точек
x1, y1 = m4(merged4['longtitude'], merged4['latitude'])

    #s отвечает за размер, делю на 30, чтобы каши не было
m4.scatter(x1, y1, marker='o', color='green', s = merged4['Total'] / 30, zorder=10)

for i, j in data3.iterrows(): #то же, что и в 1 3, только пришлось немного сместить названия стран, чтобы опять же не было каши

    lon = j['longtitude']
    lat = j['latitude']
    lon = float(lon)
    lat = float(lat)
    lon = lon +1.88
    lat = lat 
    xpt,ypt = m4(lon,lat)
    lonpt, latpt = m4(xpt,ypt,inverse=True)
    plt.text(xpt,ypt, i)
    
    
plt.show()


#%%

#Задание 2.1
#анзипаю и делаю csv
zf = zipfile.ZipFile('railways.zip')
zf.namelist()
zf.extractall(os.getcwd())
zf.close()

railways = pd.DataFrame.from_csv(path='railways201208.csv', sep = ',', header = 0, index_col = 1, encoding='utf-8')
railways[['date_priem', 'sto_code', 'stn_code', 'dist']].head()

stations = pd.DataFrame.from_csv(path='stations.csv', sep = ',', header=0, index_col = 1, encoding='utf-8')
stations[['stshortname',  'stcode']].head()

#%%
#Задание 2.2
#код для чистых данных
sns.distplot(railways['dist'],
             kde_kws = {'color' : 'red' ,'label': 'KDE Distance'},
             hist_kws = {'color':'blue', 'alpha':None}, axlabel = '$Distance$')
#%%
#код для логарифма
railways['log_dist'] = np.log(railways['dist'])

sns.distplot(railways['log_dist'],bins=np.linspace(0 , 10 , 100) ,
             kde_kws = {'color' : 'green' ,'label': 'KDE log Distance'},
             hist_kws = {'color':'blue', 'alpha':None}, axlabel = '$log(Distance)$')

#%%
#Задание 2.3
#использую код с лекции, по большому счету
task3plot = pd.DataFrame()
task3plot['Coal'] = railways[railways['commodity'] == 1]['log_dist']
for i in range(2,11): #такой ренж нужен, чтобы не было лишних боксов
    task3plot = pd.concat([task3plot, railways[railways['commodity'] == i]['log_dist']], axis = 0)
    task3plot.rename(columns = {'Coal' : 'Coal' , 0 : i}, inplace = True) #переименовываю названия

sns.boxplot(task3plot, ax = plt.axes())
plt.axes().set_xlabel('Commodity type')
plt.axes().set_ylabel('log Distance')
plt.axes().set_xticklabels( ['Coal', 'Oil', 'Ores', 'Metals', 'Wood', 'Constructions', 
                     'Fertilizers' , 'Grains' , 'Petrol', 'Others'], rotation = 45)
plt.show()

#%%
#Задание 2.4
# задаю начальный датафрейм, который позволит без лишних трудозатрат построить график
task4plot = pd.DataFrame(columns = ['Commodity', 'log Distance', 'Weight'])
task4plot['Commodity'] = railways['commodity'].replace(to_replace = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        value = ['Coal', 'Oil', 'Ores', 'Metals', 'Woods', 'Constructions', 'Fertilizers', 'Grains', 'Petrol', 'Others'])
task4plot['log Distance'] = railways['log_dist']
#вспомогательный фрейм для определения легкий-тяжелый груз
plotter = pd.DataFrame()
plotter['TrueFalser'] = railways['weight'] < railways['weight'].median()
#сам график
task4plot['Weight'] = plotter.replace(to_replace=[True, False], value=['Light', 'Heavy'])
sns.violinplot(data = task4plot, x = 'Commodity', y = 'log Distance', hue = 'Weight', split = True,
               order = ['Coal', 'Oil', 'Ores', 'Metals', 'Woods', 'Constructions', 'Fertilizers' , 'Grains' , 'Petrol', 'Others'], ax = plt.axes(), hue_order= ['Light', 'Heavy'])
plt.axes().set_xticklabels( ['Coal', 'Oil', 'Ores', 'Metals', 'Wood', 'Constructions', 'Fertilizers' , 'Grains' , 'Petrol', 'Others'], rotation = 45 )
plt.legend(loc = 'best')
plt.show()

#%%
#Задание 2.5
#дропаю значения ниже нуля, чтобы не портить выборку
task5plot = railways[['amount', 'weight', 'dist']][railways['amount'] > 0]
#беру логи
task5plot['logAmount'] = np.log(task5plot['amount'])
task5plot['logWeiDist'] = np.log(task5plot['weight'] * task5plot['dist'])

#сам график
plt.figure(figsize=(15,15))
sns.jointplot(x='logWeiDist', y='logAmount', kind='reg',marginal_kws={'hist_kws': {'edgecolor': "black"}}, data=task5plot, annot_kws={'loc': 'best'})
plt.ylabel('log(Amount)')
plt.xlabel('log(Weight * Distance)')
plt.show()
