#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 15:20:52 2018

@author: maria.ilinykh
"""
#%%
import re
import requests
import numpy as np
import pandas as pd

import zipfile, io
pd.set_option('float_format', '{:6.5f}'.format)
np.set_printoptions(precision=3, suppress=True)

zip_file_url = 'http://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
z.namelist()

file_one = z.open('survey_results_public.csv')
file_two =z.open('survey_results_schema.csv')

file_one = pd.read_csv(file_one)
file_two = pd.read_csv(file_two, header = 0)

data = file_one.set_index('Respondent')
data.iloc[:,:1].head()

schema = file_two.set_index('Column')
schema.head()
len(schema)
data.Professional.value_counts()
dta_name = data.Country.value_counts()
#%%
#2
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
plt.figure(figsize = (15,25))
world = {'left_lon': -180,'right_lon': 180, 'left_lat': -90, 'right_lat': 90 }
m = Basemap(projection='cyl',llcrnrlat=world['left_lat'],
            urcrnrlat=world['right_lat'],
            llcrnrlon=world['left_lon'], urcrnrlon=world['right_lon'],resolution='c')
#m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            #llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.50, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='burlywood',lake_color= 'lavender')
m.drawparallels(np.arange(-90.,91, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='lightblue') # draw a line around the map region
plt.title("Карта")
plt.show()
plt.figure(figsize = (85,65))
 #%%

#%%
url = 'http://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url)
points =  pd.read_html(response.content)[0]

points.columns = [['country', 'latitude', 'longitude', 'name']]

points = points.reindex(points.index.drop(0))
df = pd.DataFrame(data=points)

#%% find all names
#df = df[['latitude',  'longitude', 'mag', 'place']]
#df['place'].replace({re.compile('[0-9]*km [S|E|W|N]* of '):''}, regex=True, inplace = True)
#%%
plt.figure(figsize = (15,25))
world = {'left_lon': -180,'right_lon': 180, 'left_lat': -90, 'right_lat': 90 }
m = Basemap(projection='cyl',llcrnrlat=world['left_lat'],
            urcrnrlat=world['right_lat'],
            llcrnrlon=world['left_lon'], urcrnrlon=world['right_lon'],resolution='c')
#m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            #llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.50, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='burlywood',lake_color= 'lavender')
m.drawparallels(np.arange(-90.,91, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='lightblue') # draw a line around the map region

x1, y1 = m(df['longitude'], df['latitude'])
m.scatter(x1, y1, marker='o', color='red', s = 20, zorder=10) 


plt.title("Карта")
plt.show()
#%%
# Данные с координатами
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url)
table = pd.read_html(str(response.content))[0]

points = pd.DataFrame(table)
points.columns = points.iloc[0]
points = points.reindex(points.index.drop(0))

points.head(10)
dta_name.head()

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
    

dta_name = pd.DataFrame(dta_name)
dta_name.reset_index(inplace=True)

for i in dict.keys(): 
    dta_name["index"].replace(i, value=dict[i], inplace=True)

dta_name.set_index("index", inplace=True)
dta_name.head()

points = points.set_index('name')
#%% plot3
plt.figure(figsize = (15,25))
world = {'left_lon': -180,'right_lon': 180, 'left_lat': -90, 'right_lat': 90 }
m = Basemap(projection='cyl',llcrnrlat=world['left_lat'],
            urcrnrlat=world['right_lat'],
            llcrnrlon=world['left_lon'], urcrnrlon=world['right_lon'],resolution='c')
#m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            #llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.50, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='burlywood',lake_color= 'lavender')
m.drawparallels(np.arange(-90.,91, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='lightblue') # draw a line around the map region


df2 = pd.concat([points, dta_name],axis=1, join='inner')
df2 = df2.rename(columns = {'Country':'respondents'})
df2.head()
x1, y1 = m(df2['longitude'], df2['latitude'])

m.scatter(x1, y1, marker='o', color='red', s = df2['respondents']/50, zorder=10) 

plt.show()
#%%
import matplotlib as mpl
import seaborn as sns 
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 


path = "/Users/maria.ilinykh/Downloads/railways201208.csv"
datar = pd.read_csv(path)
print(datar)

path = "//Users/maria.ilinykh/Downloads/stations.csv"
datas = pd.read_csv(path)
print(datas)

rail = pd.DataFrame(datar)
stat = pd.DataFrame(datas)

print(datar.head())
print(datas.head())

datar['log Distance'] = datar['dist'].apply(np.log)
fig = plt.figure(figsize=(9, 7))
sns.distplot(datar['dist'], bins = 86,kde=True,
             kde_kws={"color": "g", "lw": 3, "label": "log Distance", "shade":True},
             hist_kws={"histtype": "stepfilled","alpha": 1, "color": "b"}) 
plt.show()

fig = plt.figure(figsize=(10, 7))
sns.distplot(datar['log Distance'], bins = 88,kde=True,
             kde_kws={"color": "g", "lw": 3, "label": "log Distance", "shade":True},
             hist_kws={"histtype": "stepfilled","alpha": 1, "color": "b"})
plt.show()
#%%
datar['commodity1'] = datar['commodity']

dict={1:'Coal', 2:'Oil', 3:'Ores', 4:'Metals',5:'Wood', 
      6:'Constructions', 7:'Fertilizers', 8:'Grains', 
      9:'Petrol', 10:'Other'}

for i in dict.keys():
    datar['commodity'].replace(i, value=dict[i], inplace=True )
    
datar = datar.rename(columns={'commodity':'Commodity type'}) 
datar = datar.set_index('commodity1')
datar = datar.sort_index(axis = 0)
#%%
fig = plt.figure(figsize=(10, 8))
sns.boxplot(x='Commodity type', y='log Distance', data=datar,linewidth=3.5)
plt.xticks(rotation='vertical')
plt.show()
#%%
datar = datar.set_index('Commodity type')
for i in datar.index.unique():
    datar.loc[i,'median'] = int(datar.loc[i,'weight'].median())

# создаем колонку с разделением на Light/Heavy
datar['Weight'] = datar['weight'] - datar['median']
datar['median'] = datar['median'].astype(int)

def compare(x):
    x = int(x)
    if x > 0:
        return('Heavy')
    elif x < 0:
        return('Light')
    else:
        return('Light')
         
datar['Weight'] = datar['Weight'].apply(compare)
#%%
fig = plt.figure(figsize=(9, 7))
sns.violinplot(x=datar.index, y='log Distance',
               hue='Weight', hue_order=['Light','Heavy'], split=True,
               data=datar,linewidth=3)
plt.xticks(rotation='vertical')
plt.legend(title='Weight',loc='lower right')
plt.show()
#%%
datar.dtypes
datar['weight'] = datar['weight'].astype(float)
datar['dist'] = datar['dist'].astype(float)

datar = datar[datar['amount'].notnull()]

datar['log(weight*dist)'] = np.log(datar['weight']*datar['dist'])
datar['log(amount)'] = np.log(datar['amount']) 

datar = datar[datar['log(amount)'].notnull()]
#%%
datar = datar.reset_index()
datar = datar.set_index('amount')
datar.drop(datar[datar.index == 0].index, inplace=True)

g = sns.jointplot(x='log(weight*dist)',y='log(amount)', data=datar, kind='reg')
g.fig.set_figwidth(8)
g.fig.set_figheight(7)
plt.show()

