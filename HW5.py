#HW4 Serbin Alexander
#Set up the environment.

import requests
import zipfile
import re
import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context('notebook')
pd.set_option('float_format', '{:6.2f}'.format)

# Ignore warnings. This is a temporary bug that should disappear in future versions of the libraries used here.
import warnings
warnings.filterwarnings("ignore")



#%%
#Problem 1
#1
#Загрузите файл с данными опроса по адресу https://drive.google.com (используя пакет requests).

url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
path = 'Desktop/developer_survey_2017.zip'

response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)
    

#%%
#прочитайте данные из двух файлов внутри полученного архива в разные наборы данных pandas
#(survey_results_public.csv с ответами и survey_results_schema.csv с вопросами).

zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)

public = pd.read_csv(zf.open(files[-2]))
schema = pd.read_csv(zf.open(files[-1]))
public.columns = [x.strip() for x in public.columns]
schema.columns = [x.strip() for x in schema.columns]
public.columns

#%%
#Сколько вопросов было в опросе?
schema.head()
print(schema.shape[0])
#%%
#Сколько разработчиков приняло участие в нем?
public.iloc[:,:2].head()
print(public.shape[0])

#%%
#2
from mpl_toolkits.basemap import Basemap
plt.figure(figsize = (25,40))

map1 = Basemap(projection = 'cyl', llcrnrlat = -90, urcrnrlat = 90, llcrnrlon = -180, urcrnrlon = 180, resolution = 'c')
map1.drawcoastlines()
map1.drawcountries(linewidth = 0.25, antialiased = False)
map1.fillcontinents(color = 'coral',lake_color = 'aqua')
map1.drawmapboundary(fill_color = 'aqua')

plt.show()

#%%
#3
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
cr = pd.read_html(url, index_col = 0)[0]
cr = cr.drop(cr[(cr[1] == 'latitude')].index)
cr[1] = cr[1].astype(float)
cr[2] = cr[2].astype(float)

plt.figure(figsize = (25,40))

map2 = Basemap(projection='cyl',llcrnrlat = -90, urcrnrlat = 90, llcrnrlon = -180, urcrnrlon = 180, resolution='c')
map2.drawcoastlines()
map2.drawcountries(linewidth = 0.25, antialiased = False)
map2.fillcontinents(color = 'coral',lake_color = 'aqua')
map2.drawmapboundary(fill_color = 'aqua')

#%%
#4
cr = cr[-90 <= cr[1]]
cr = cr[cr[1] <= 90]
cr = cr[-180 <= cr[2]]
cr = cr[cr[2] <= 180]

x1 = map2(cr[2])
y1 = map2(cr[1])

map2.scatter(x1, y1, color = 'red', s = 100, zorder=10)
for i in range(cr.shape[0]):
    plt.text(x1.iloc[i] - 6, y1.iloc[i] - 2, cr.iloc[i][3], fontsize = 10)
  
plt.show()

#%%
#Problem 2

#1
path = 'Desktop/railways.zip'
zf = zipfile.ZipFile(path)

zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)

rail = pd.read_csv(zf.open(files[-2]))
station = pd.read_csv(zf.open(files[-1]))
rail.columns = [x.strip() for x in rail.columns]
station.columns = [x.strip() for x in station.columns]
station[:10]

#%%
#2

sns.distplot(rail['dist'])
plt.show()

#%%
rail['lgdist'] = np.log(rail['dist'])
sns.distplot(rail['lgdist'])
plt.show()

#%%
#3
data = pd.DataFrame()
data['Coal'] = rail[rail['commodity'] == 1]['log_dist']
for i in range(2,11):
    data = pd.concat([data, rail[rail['commodity'] == i]['log_dist']], axis = 0, ignore_index = True)
    data.rename(columns = {'Coal' : 'Coal' , 0 : i}, inplace = True)

ax = plt.axes()
sns.boxplot(data, ax = ax)
ax.set_xlabel('Commodity type')
ax.set_ylabel('log Distance',  family = 'cursive')
ax.set_xticklabels( ['Coal', 'Oil', 'Ores', 'Metals', 'Wood', 'Constructions', 'Fertilizers' , 'Grains' , 'Petrol', 'Others'], rotation = 90 )
plt.show()

