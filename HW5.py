# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:39:39 2018

@author: Alexander
"""
#%%
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import requests
import zipfile
import io
import matplotlib.pylab as plt
import seaborn as sns
#%%
"""
Task 1
"""
#%%
"""
Task 1.1
"""

url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
zip = requests.get(url)
my_zip = zipfile.ZipFile(io.BytesIO(zip.content)) 
my_zip.namelist() 
data_answers = my_zip.open('survey_results_public.csv') 
data_questions =my_zip.open('survey_results_schema.csv')
answers = pd.read_csv(data_answers, header=0)
questions = pd.read_csv(data_questions, header=0)

questions.shape #154 - вопросов в опросе
answers.shape #51392 - участников всего

#Если имеются в виду именно профессиональные разработчики:
answers.groupby('Professional').Professional.count()
#Сгруппировали и посчитали все ответы в Professional
#Professional
#None of these                                             914
#Professional developer                                  36131
#Professional non-developer who sometimes writes code     5140
#Student                                                  8224
#Used to be a professional developer                       983

#Ответ: 36131 разработчиков приняло участие в опросе.
#%%
"""
Task 1.2
"""
plt.figure(figsize = (20,15))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='green',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,180.,60.))
m.drawmapboundary(fill_color='aqua') # draw a line around the map region
plt.title("Cylindrical Equal-Area Projection")
plt.show()
#%%
"""
Task 1.3
"""
url1 = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url1)
coordinates = pd.read_html(str(response.content))[0]
coordinates.columns = coordinates.iloc[0]
coordinates = coordinates.iloc[1:]
coordinates = coordinates.dropna()
coordinates = coordinates[['latitude','longitude','name']]

y,x = m(coordinates['latitude'],coordinates['longitude'])
plt.figure(figsize = (20,15))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='green',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,180.,60.))
m.drawmapboundary(fill_color='aqua') # draw a line around the map region
plt.title("Countries' centers coordinates")
m.scatter(x, y, marker='o', color='b', s = 10, zorder=10, edgecolors = 'black')
plt.show()


#%%
"""
Task 1.4
"""
Country = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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

Population = answers.groupby('Country').Country.count()
Population_d = pd.DataFrame(Population)
Population_d.rename(columns={'Country':'Population'},inplace = True)
Population_d = Population_d.reset_index() #Перемещаем страны из индекса в столбец
Population_d.replace({"Country": Country})
Population_d = Population_d.set_index('Country')
coordinates.rename(columns={'name':'Country'}, inplace = True)
coordinates = coordinates.set_index('Country')
merge = pd.merge(coordinates, Population_d, right_index = True, left_index = True) #right_index = True)
#merge = merge.sort_values(groupby(Population),ascending = False)
merge = merge.sort_values(by='Population',ascending = False)


#m.fillcontinents(color='green',lake_color='aqua')
#m.drawparallels(np.arange(-90.,90, 30.))
#m.drawmeridians(np.arange(-180.,180.,60.))
#m.drawmapboundary(fill_color='aqua') # draw a line around the map region
#plt.title("Countries' centers coordinates")

plt.figure(figsize = (20,15))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) #antialiased - отвечает за прозрачность линий
#color = цвет континентов, lake_color = цвет озер
m.fillcontinents(color='green',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')

y,x = m(merge['latitude'],merge['longitude'])
#m.scatter(x, y, merge['Population'], marker='o', color='b', zorder=10, edgecolors = 'black') Шары дохера большие выходят
m.scatter(x, y, merge['Population']/10, marker='o', color='b', zorder=10, edgecolors = 'black')
plt.show()
#%%
"""
Task 2
"""
#%%
"""
Task 2.1
"""
path = "/Users/Alexander/railways.zip"
zip_file = zipfile.ZipFile(path)
files = zip_file.namelist()
ways = pd.read_csv(zip_file.open(files[0]))
stat = pd.read_csv(zip_file.open(files[1]))
ways.head(7)

#%% 
"""
Task 2.2
"""
log_dist = np.log(ways.dist)
ways['log_dist']=log_dist #приписали логарифм путей к фрейму
sns.distplot(ways.dist, axlabel='', color='tomato', kde_kws={'label':'Distance'}, hist_kws={'histtype': 'bar'}, bins=100)
plt.show()
sns.distplot(ways.log_dist, axlabel='', color='orange', kde_kws={'label':'log Distance'}, hist_kws={'histtype': 'bar'}, bins=100)


#%%
"""
Task 2.3
"""
log_dist = np.log(ways.dist)
ways['log_dist']=log_dist
ways.commodity=ways.commodity.astype('float64')
dictionary = {1: 'Coal', 2: 'CrudeOil', 3: 'IronOre', 4: 'MetalProducts', 5: 'Forest', 6: 'Construction', 7: 'Fertilizers', 8: 'Corns', 9: 'RefineryOil', 10: 'Other'}
ways['Commodities'] = list(map(lambda x: dictionary[x], ways.commodity))
plt.figure(figsize = (15,7))
Dropkick_Murphys = sns.boxplot(x=ways.Commodities, y = ways.log_dist)
Dropkick_Murphys.set_xticklabels(Dropkick_Murphys.get_xticklabels(), rotation=90)
plt.xlabel('')
plt.ylabel('log_dist')
plt.show()
Dropkick_Murphys1 = sns.boxplot(x=ways.Commodities, y = ways.dist)
Dropkick_Murphys1.set_xticklabels(Dropkick_Murphys.get_xticklabels(), rotation=90)
plt.xlabel('')
plt.ylabel('Dist')
plt.show()
#%%
"""
Task 2.4
"""
#Теперь смотрим,больше или меньше груз, чем медианное значение
median = ways.groupby('Commodities')['weight'].median()
Weight_dict = {}
for i in range(len(median)):
    Weight_dict[median.index[i]] = median[i]
ways['Weight'] = list(map(lambda x, y: ('Light' if y < Weight_dict[x] else 'Heavy'), ways.Commodities, ways.weight))
ways = ways.sort_values(by=['commodity', 'Weight'], ascending=(True, False))
plt.figure(figsize=(13, 13))
Estas_Tone = sns.violinplot(x='Commodities', y='log_dist', hue='Weight', split=True, data=ways, palette='muted')
Estas_Tone.set_xticklabels(Estas_Tone.get_xticklabels(), rotation=90)
plt.xlabel('')
plt.ylabel('log_dist')
plt.show()
#%%
"""
Task 2.5
"""
railways = ways[['amount', 'weight', 'dist']][ways['amount'] > 0]
railways['log_amount'] = np.log(ways.amount)
railways['log_way_dist'] = np.log(ways.weight*ways.dist)

df5 = pd.DataFrame.sample(railways, 2000)

plt.figure(figsize=(15,8))
sns.jointplot(x='log_way_dist', y='log_amount', data=df5, kind='reg')
plt.ylabel('log_Amount')
plt.xlabel('log_Weight + log_Distance')
plt.show()