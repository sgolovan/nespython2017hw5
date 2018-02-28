#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:26:26 2018

@author: alena
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile, io
#%%
#1
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
zip = requests.get(url)
my_zip = zipfile.ZipFile(io.BytesIO(zip.content))
my_zip.namelist()

file1 = my_zip.open('survey_results_public.csv')
file2 =my_zip.open('survey_results_schema.csv')

data0 = pd.read_csv(file1,  header = 0)
schema0 = pd.read_csv(file2, header = 0)

data1 = data0.copy()
schema1 = schema0.copy()

data1 = data1.set_index('Respondent')
schema1 = schema1.set_index('Column')
# input
data1.iloc[:,:1].head()
schema1.head()

# Сколько вопросов было в опросе?
print(len(data1.columns))
#  Сколько разработчиков приняло участие в нем?
data1.Professional.value_counts()
print(data1.Professional.value_counts()['Professional developer'])

#group by countries
data_by_country = data1.Country.value_counts()

#%%
# PLOT 1
fig = plt.figure(figsize = (18,24))
coord_world = {'left_lon': -180,'right_lon': 180, 'left_lat': -80, 'right_lat': 80 }
m = Basemap(projection='cyl',llcrnrlat=coord_world['left_lat'],urcrnrlat=coord_world['right_lat'],
            llcrnrlon=coord_world['left_lon'],urcrnrlon=coord_world['right_lon'],resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua') 
plt.show()
#fig.savefig('pic1.svg') 

#%%
# Данные с координатами
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url)
#чтобы избавиться от листа, добавляем [0]
table = pd.read_html(str(response.content))[0]

table = pd.DataFrame(table)

table.head()

data = table.copy()
data.columns = data.iloc[0]
data = data.reindex(data.index.drop(0))

data.head(10)
data_by_country.head(10)

dict = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
'Azerbaidjan': 'Azerbaijan',
'Brunei Darussalam': 'Brunei',
'Falkland Islands': 'Falkland Islands [Islas Malvinas]',
'Heard and McDonald Islands': 'Heard Island and McDonald Islands',
'Slovak Republic': 'Slovakia',
'Tadjikistan': 'Tajikistan',
'Vatican City State': 'Vatican City',
'Virgin Islands (British)': 'British Virgin Islands',
'Virgin Islands (USA)': 'U.S. Virgin Islands',
'Russian Federation': 'Russia',
'Polynesia (French)': 'French Polynesia',
'Pitcairn Island': 'Pitcairn Islands',
'Saint Vincent & Grenadines': 'Saint Vincent and the Grenadines',
'Reunion (French)': 'Réunion',
'Ivory Coast (Cote D\'Ivoire)': 'Côte d\'Ivoire',
'Zaire': 'Congo [DRC]',
'Macedonia': 'Macedonia [FYROM]',
'Martinique (French)': 'Martinique',
'Myanmar': 'Myanmar [Burma]',
'New Caledonia (French)': 'New Caledonia',
'S. Georgia & S. Sandwich Isls.':
'South Georgia and the South Sandwich Islands',
'Moldavia': 'Moldova',
'French Guyana': 'French Guiana',
}
    
# заменяем названия стран
data_by_country = pd.DataFrame(data_by_country)
data_by_country.reset_index(inplace=True)

for i in dict.keys(): 
    data_by_country["index"].replace(i, value=dict[i], inplace=True)

data_by_country.set_index("index", inplace=True)

#%%
# PLOT 2
fig = plt.figure(figsize = (30,50))

m = Basemap(projection='cyl',llcrnrlat=coord_world['left_lat'],urcrnrlat=coord_world['right_lat'],
            llcrnrlon=coord_world['left_lon'],urcrnrlon=coord_world['right_lon'],resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua') # draw a line around the map region

data.dtypes
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

data = data.set_index('name')
x1, y1 = m(data['longitude'], data['latitude'])
m.scatter(x1, y1, marker='o', color='r', s = 10, zorder=10, edgecolors = 'black')#, 'ro', color = color,  zorder=10, markersize=15)

plt.show() 
#fig.savefig('pic2.svg') 
#%%
# PLOT 3
fig = plt.figure(figsize = (30,50))
m = Basemap(projection='cyl',llcrnrlat=coord_world['left_lat'],urcrnrlat=coord_world['right_lat'],
            llcrnrlon=coord_world['left_lon'],urcrnrlon=coord_world['right_lon'],resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

data.dtypes
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# merging datas
df_for_map = pd.concat([data,data_by_country],axis=1, join='inner')
df_for_map = df_for_map.rename(columns = {'Country':'respondents'})
df_for_map.head()

x1, y1 = m(df_for_map['longitude'], df_for_map['latitude'])

m.scatter(x1, y1, marker='o', color='r', s = df_for_map['respondents']/10, zorder=10, edgecolors = 'black')#, 'ro', color = color,  zorder=10, markersize=15)

plt.show()
#fig.savefig('pic3.svg') 






