#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:53:51 2018

@author: nik
"""
# HA_5
#%%
import re
import requests
import zipfile
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#%% Task 1.1
#Code from HA_4 where I download results of survey
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
response = requests.get(url)

path = '/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/data/HA_4.zip'

response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)

zf = zipfile.ZipFile(path)
files = zf.namelist()

survey_results_schema = pd.read_csv(zf.open(files[-1]))
survey_results_schema.columns = [x.strip() for x in survey_results_schema.columns]

survey_results_public = pd.read_csv(zf.open(files[-2]))
survey_results_public.columns = [x.strip() for x in survey_results_public.columns]
#%%
print('Number of questions %d' %np.shape(survey_results_schema.iloc[:,1])[0], '\n',
      'Number of respondents %d' %np.shape(survey_results_public.iloc[:,0])[0])
#%% Task 1.2
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize = (40,50))
m = Basemap(projection='cyl',llcrnrlat=-80,urcrnrlat=70,
            llcrnrlon=-180,urcrnrlon=180,resolution='l')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='blanchedalmond',lake_color='paleturquoise')
m.drawparallels(np.arange(-90.,90, 10.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='paleturquoise') 
plt.title("Cylindrical Equal-Area Projection", fontsize=40)
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_1_2.pdf', bbox_inches='tight')
plt.show()
#%% Task 1.3
#Let's create DataFrame 'locations' from csv from the web-site
locations = pd.read_html('https://developers.google.com/public-data/docs/canonical/countries_csv')
temp = dict((locations[0][i][0],locations[0][i][1:]) for i in np.arange(0,4,1))
locations = pd.DataFrame(temp)
#%%
#Let's replace countries in column of 'surveys' which are named differently from 
#the countries in 'location' 
d = {
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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
    'Reunion (French)': 'Réunion',
    'Ivory Coast (Cote D\'Ivoire)': 'Côte d\'Ivoire',
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
survey_results_public['Country'].replace(d, inplace=True)
#%%
#Let's choose only countries with respondents from DataFrame survey_results_public.
#Then we will transform obtained object Series to Fataframe and make appropriate index and columns 
countries_with_respondents = survey_results_public['Country'].value_counts()
countries_with_respondents_df = countries_with_respondents.to_frame()
countries_with_respondents_df.reset_index(inplace=True)
countries_with_respondents_df.columns = ['country','counts']

locations.columns = ['short name', 'latitude', 'longitude', 'country']
#%%
#Let's create DataFrame 'locations_final' which will contain only countries
#with respondents participated in survey and that have coordinates of location
locations_final = locations.merge(countries_with_respondents_df, how='inner', on='country')
#%%
#Let's place our dots on map
plt.figure(figsize = (40,50))
m = Basemap(projection='cyl',llcrnrlat=-80,urcrnrlat=70,
            llcrnrlon=-180,urcrnrlon=180,resolution='l')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='blanchedalmond',lake_color='paleturquoise')
m.drawparallels(np.arange(-90.,90, 10.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='paleturquoise') 
plt.title("Participated countries", fontsize=40)

m.scatter(locations_final['longitude'].astype(float), locations_final['latitude'].astype(float), 
                          marker='o', edgecolor='black', linewidth = 2, color='r', s = 80, zorder=10)
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_1_3.pdf', bbox_inches='tight')
#%%
#Let's create column 'percentage' in 'location_final' which will have relative 
#amount of participants from particular country
locations_final['percentage'] = locations_final['counts']/sum(locations_final['counts'])

plt.figure(figsize = (40,50))
m = Basemap(projection='cyl',llcrnrlat=-40,urcrnrlat=65,
            llcrnrlon=-120,urcrnrlon=142,resolution='l')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='blanchedalmond',lake_color='paleturquoise')
m.drawparallels(np.arange(-90.,90, 10.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='paleturquoise') 
plt.title("Participated countries and number of participants", fontsize=40)

m.scatter(locations_final['longitude'].astype(float), locations_final['latitude'].astype(float), 
                          marker='o', edgecolor='black', linewidth = 2, color='r', s = locations_final['percentage']*5000, zorder=10)
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_1_4.pdf', bbox_inches='tight')

#%% Task 2.1

path_railways = '/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/data/railways/railways201208.csv'
path_stations = '/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/data/railways/stations.csv'

df_railways = pd.read_csv(path_railways, sep=',')
df_stations = pd.read_csv(path_stations, sep=',')
df_railways.iloc[:3,:5], df_stations.iloc[:3,:3]
#%%Task 2.2
#Let's build histogram via method of plt. 
#Also we will draw kernel estimate of distribution on the same via seaborn method sns
plt.figure(figsize=(15, 9))
plt.hist(df_railways['dist'], normed=1, bins=100, alpha=0.8)
sns.kdeplot(df_railways['dist'],label = 'Distance')
plt.ylabel('Frequency')
plt.xlabel('Distance in km')
plt.title('Гистограмма и ядерная оценка плотности \n для расстояния перевозки')
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_2_2_1.pdf', bbox_inches='tight')
plt.show()
#The same is for logarithm of Distance.
plt.figure(figsize=(15, 9))
df_railways['log_dist'] = df_railways['dist'].apply(lambda x: np.log(x))
plt.hist(df_railways['log_dist'], normed=1, bins=100, alpha=0.8)
sns.kdeplot(df_railways['log_dist'],label = 'Log(Distance)')
plt.xlabel('$log($Distance in km$)$')
plt.title('Гистограмма и ядерная оценка плотности \n для логарифма расстояния перевозки')
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_2_2_2.pdf', bbox_inches='tight')
#%% Task 2.3
labels = ['уголь', 'сырая нефть','руды\n металлические', 'металлургическая\n продукция', 
          'лесная\n продукция', 'строительные\n материалы', 'удобрения', 
          'зерно и \nпродукты перемола', 'продукты \nнефтепереработки', 'остальные \nгрузы']

df_railways['commodity_categ'] = \
            pd.Categorical.from_codes(df_railways['commodity']-1,categories =labels ) 
plt.figure(figsize=(15,9))
ax = sns.boxplot(data=df_railways, x='commodity_categ', y='log_dist', palette="Set3")
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.title('$log($расстояния$)$ в виде boxplot,\n категоризованный по'\
          'типам грузов')
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_2_3.pdf', bbox_inches='tight')
plt.show()
#%% Task 2.4
#Let's calculate medians of log_dist over the commodity and 
#then add corresponding column in our DataFrame df_railways
medians = df_railways.groupby('commodity_categ')['log_dist'].apply(np.median)
medians.name = 'medians'
df_railways = df_railways.join(medians, on=['commodity_categ'])
#Let's create column which will be filled in Category(Heavy, Light) 
#if value of 'log_dist' > 'median' across the corresponding commodity  
df_railways['Heavy or light'] = \
        np.where(df_railways['log_dist'] >= df_railways['medians'], 'Heavy', 'Light')
#Let's draw ourviolin graph where parametr hue will get information 
#about weight respectively to median        
plt.figure(figsize=(15, 9))
ax = sns.violinplot(x='commodity_categ', y='log_dist',
               hue='Heavy or light', split=True,
               linewidth=.5, data=df_railways, palette="Set3")
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
plt.title('Violinplot с распределениями расстояния перевозки,\n'
              'классифицированный по типам грузов')
plt.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_2_4.pdf', bbox_inches='tight')
#%% Task 2.5
x = df_railways['weight']*df_railways['dist']
df_railways['log_w_dist'] = x.apply(lambda x: np.log(x))
df_railways['log_amount'] = df_railways['amount'].apply(lambda x: np.log(x))
#Some values of 'amount' equal 0 that leads to -Infinity after logarithm 
#implementation. That's why we need to replace such values with nan and then drop them.
df_railways.replace(-np.inf, np.nan, inplace=True)
df_railways_na = df_railways.dropna(subset=['amount'])

plt.figure(figsize=(15, 9))
a = sns.jointplot(x='log_w_dist', y='log_amount',
              data=df_railways_na, kind='reg')
a.savefig('/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/HA5_2_5.pdf', bbox_inches='tight')
plt.show()
