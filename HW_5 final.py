
# ## Задача 1




import requests
import zipfile
import os

import numpy as np
import pandas as pd



url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
dirname = ''
path = dirname + 'stack_overflow.zip'


response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)




zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)



files[6]


public = pd.read_csv(zf.open(files[5]), header=0)



public.head()



schema = pd.read_csv(zf.open(files[6]), header=0)



schema.head()


# Сколько вопросов было в опросе? 


schema.shape


# 154 вопросов было в опросе

# Сколько разработчиков приняло участие в нем?


public.shape


# 51392 разработчиков приняло участие в нем

# ## 2



import mpl_toolkits
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



#нарисуем карту мира


plt.figure(figsize = (18,25))
world_map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90, llcrnrlon=-180,urcrnrlon=180,resolution='c')
world_map.drawcoastlines()
world_map.drawcountries(linewidth=0.25, antialiased = False) 
world_map.fillcontinents(color='coral',lake_color='aqua')
world_map.drawparallels(np.arange(-90.,90, 30.))
world_map.drawmeridians(np.arange(-180.,181.,60.))
world_map.drawmapboundary(fill_color='aqua') 
plt.show()


# ## 3

# загрузим таблицу при помощи BeautifulSoup


from bs4 import BeautifulSoup
import urllib.request
import os
    
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

countries_data = soup.find( 'table' )
countries_table = []
line = []

for row in countries_data.findAll("tr"):
    cells = row.findAll("td")
    line = []
    for i in range(len(cells)):
        line.append(cells[i].text)
    countries_table.append(line)
    
countries_table = pd.DataFrame(countries_table)

column_names = []
for row in countries_data.findAll("th"):
    column_names.append(row.text )
    
countries_table.columns = column_names 
countries_table = countries_table[countries_table.country != 'UM']
countries_table  = countries_table [  pd.isnull(countries_table.country  ) ==False ].reset_index(drop = True)

countries_table [  'longitude'] = countries_table [ 'longitude'].astype(float)
countries_table [ 'latitude'] = countries_table ['latitude'].astype(float)



countries_table.head()


plt.figure(figsize = (18,25))
world_map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,  llcrnrlon=-180,urcrnrlon=180,resolution='c')
world_map.drawcoastlines()
world_map.drawcountries(linewidth=0.25, antialiased = False) 
world_map.fillcontinents(color='coral',lake_color='aqua')
world_map.drawparallels(np.arange(-90.,90, 30.))
world_map.drawmeridians(np.arange(-180.,181.,60.))
world_map.drawmapboundary(fill_color='aqua') 
world_map.scatter(countries_table['longitude'],countries_table['latitude'], marker='o', color='r', s = 100, zorder=10) 
plt.show()

# ## 4






dict_for_replace = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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
countries_table.name = countries_table.name.replace(dict_for_replace)
countries_table['Country'] = countries_table.name


public_count_respondents = public.groupby('Country', as_index = False).count()[['Country', 'Respondent']]



merged_tables = pd.merge(countries_table, public_count_respondents, on= 'Country')


plt.figure(figsize = (18,25))
world_map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,  llcrnrlon=-180,urcrnrlon=180,resolution='c')
world_map.drawcoastlines()
world_map.drawcountries(linewidth=0.25, antialiased = False) 
world_map.fillcontinents(color='coral',lake_color='aqua')
world_map.drawparallels(np.arange(-90.,90, 30.))
world_map.drawmeridians(np.arange(-180.,181.,60.))
world_map.drawmapboundary(fill_color='aqua')
world_map.scatter(merged_tables['longitude'], merged_tables['latitude'] , marker='o', color='r', s =  (merged_tables['Respondent'])/20, zorder=10)
plt.show()


# ## Задание 2

# ## 1


path2 = 'railways.zip'



zf = zipfile.ZipFile(path2)
railways_file = zf.namelist()
print (railways_file)


railways =  pd.read_csv(zf.open(railways_file[0]), header=0)


railways.head()


stations = pd.read_csv (zf.open(railways_file[1]), header = 0)



stations.head()


railways['dist'][0]


# ## 2



plt.hist(railways['dist'], bins = 50)
plt.show()




plt.hist(np.log(railways['dist']), bins = 50)
plt.show()




import seaborn as sns



sns.kdeplot(railways['dist'], label = 'Distance',)
plt.hist(railways['dist'], bins = 100, normed = True, color = 'lightblue')
plt.show()





sns.kdeplot(np.log(railways['dist']), label = 'log Distance',)
plt.hist(np.log(railways['dist']), bins = 100, normed = True, color = 'lightblue')
plt.show()



railways['log_dist'] =  np.log(railways['dist'])


# ## 3



dictionary = {1 :'Coal', 
              2:'Oil', 
              3: 'Ores',
              4: 'Metals',
              5: 'Wood',
              6:'Constructions',
              7: 'Fertilizers',
              8: 'Grains',
              9: 'Petrol',
              10: 'Other'}

dictionary.values()


railways["commodity"] = railways["commodity"].replace(dictionary)





railways.head()




#ordering = railways.groupby('commodity').mean()['weight'].sort_values(ascending = True).index




list(dictionary.values())





plt.figure(figsize = (12,6))
sns.boxplot(x = "commodity", y = 'log_dist', data = railways, order = list(dictionary.values()))
plt.show()


# ## 4




l = pd.DataFrame(railways.groupby('commodity').mean()['weight']).reset_index() 
l





weight_table =  pd.merge(railways, l,on=['commodity'])
weight_table.head()





k = (weight_table.weight_x > weight_table.weight_y)*1
k





weight_table["weight_y"]= k





dict2 = {0: "Light",
         1: "Heavy"}




weight_table["weight_y"] = k.replace(dict2) 
weight_table.head()





plt.figure(figsize = (12,6))
stat = sns.violinplot(x="commodity", y="log_dist", hue="weight_y", data=weight_table, palette="muted", split=True, hue_order = ["Light", "Heavy"], order = list(dictionary.values()))
plt.show()


# ## 5




import seaborn as sns
sns.set(style="white", color_codes=True)




railways['log(weight*dist)'] = np.log(railways['dist']* railways['weight']+1)
railways['log(amount)'] = np.log(railways['amount']+1)




plt.figure(figsize = (20,20))
sns.jointplot('log(weight*dist)','log(amount)', data = railways[railways['log(amount)']> 0], kind="reg")
plt.show()










