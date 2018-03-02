

import pandas as pd
import numpy as np
import gc
pd.set_option('display.max_columns', 200)
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
sns.set()
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
import re
import urllib.request
import os


# In[6]:


url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
dirname = '../data/'
path = dirname + 'file.zip'

os.makedirs(dirname, exist_ok=True)
if not os.path.isfile(path):
    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)


zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)



survey_results = pd.read_csv( zf.open(files[5]))
survey_results.head()


survey_results.shape


survey_schema =pd.read_csv( zf.open(files[6]))
survey_schema.head()

survey_results.Country



from bs4 import BeautifulSoup
    
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser') #class object creation

tables = soup.find( 'table' )


tables = soup.find( 'table' )
T = []
line = []

for row in tables.findAll("tr"):
    cells = row.findAll("td")
    line = []
    for i in range(len(cells)):
        line.append(cells[i].text)
    T.append(line)
    
T = pd.DataFrame(T)


# In[14]:


T = T.iloc[1:]


# In[15]:


T.columns = ['country' , 'latitude','longitude' , 'name']


T.head()



T = T[T.country != 'UM']





T = T.reset_index(drop= True)




T.loc[ : , 'longitude'] = T.loc[:, 'longitude'].astype(float)



T.loc[ : , 'latitude'] = T.loc[:, 'latitude'].astype(float)




plt.figure(figsize = (18,25))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='coral',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua') 
plt.title("World map")
plt.show()





x1, y1 = T['longitude'], T['latitude']


plt.figure(figsize = (18,25))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 

m.fillcontinents(color='coral',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua') 

m.scatter(x1, y1, marker='o', color='g', s = 100, zorder=10) 

plt.title("World map")
plt.show()



countries_dict = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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



T.name = T.name.replace(countries_dict)




T['Country'] =  T.name




survey_results.head(1)



survey_results_groupby_country = survey_results.groupby('Country', as_index = False).count()[['Country', 'Respondent']]




T_new = pd.merge(T, survey_results_groupby_country , on= 'Country')



x1, y1 = T_new['longitude'], T_new['latitude']
number_of_resp = np.sqrt(T_new['Respondent'])

plt.figure(figsize = (18,25))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False) 
m.fillcontinents(color='coral',lake_color='aqua')
m.drawparallels(np.arange(-90.,90, 30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua') 

m.scatter(x1, y1, marker='o', color='g', s = number_of_resp  , zorder=10)

plt.title("World map")
plt.show()






# Задача 2





zf = zipfile.ZipFile('./railways.zip')
files = zf.namelist()

print(files)




railways = pd.read_csv( zf.open(files[0]))

stations  = pd.read_csv( zf.open(files[1]))


railways.head()




stations.head()

# 2. Изобразите гистограмму и ядерную оценку плотности для расстояния перевозки и его
логарифма. 



plt.figure( figsize = (8,8))
plt.hist (railways.dist , bins = 100, normed= True)
sns.kdeplot(  railways.dist ,   label ='KDE')
plt.title( 'Гистограмма и ядерная оценка плотности для расстояния перевозки ' )
plt.xlabel('Расстояние')
plt.show()



plt.figure( figsize = (8,8))
plt.hist ( np.log(railways.dist  ) , bins = 100, normed= True)
sns.kdeplot( np.log(railways.dist  ) , label ='KDE' )
plt.title( 'Гистограмма и ядерная оценка плотности для логарифма расстояния перевозки ' )
plt.xlabel('Логарифм расстояния')
plt.show()

#3. Изобразите логарифм расстояния в виде boxplot, категоризованный по типам грузов
#(поле commodity). Прокомментируйте результат. 
# In[38]:


commodity_dict = {  1 : 'Coal',
                    2 : 'Oil',
                    3 : 'Ores',
                    4 : 'Metals',
                    5 : 'Wood',
                    6 : 'Constructions',
                    7 : 'Fertilizers',
                    8 : 'Grains',
                    9 : 'Petrol',
                    10 : 'Other'}




commodity_dict.values()



railways.commodity = railways.commodity.replace(commodity_dict)



railways['log_dist'] = np.log(railways.dist  )


plt.figure( figsize = (14,8))
sns.boxplot(x="commodity", y="log_dist", data=railways, order = commodity_dict.values())

plt.title( 'boxplot логарифма расстояния перевозки ' )

plt.show()

4. Для каждого типа грузов вычислите медиану массы перевозимого груза и изобразите
violinplot с распределениями расстояния перевозки, классифицированный по типам
грузов, в котором слева и справа были бы распределения грузов относительно небольшой
и большой массы соответственно. Пример на рисунке 6



medians_of_weight =   pd.DataFrame(railways.groupby( 'commodity').median()['weight']).reset_index()


medians_of_weight.columns = ['commodity' ,'median_weight']


railways = pd.merge(  railways, medians_of_weight , on = 'commodity' )


railways ['light_or_heavy_bin'] =  (railways.weight> railways.median_weight)*1


light_heavy_dict = {  0: 'Light' , 1: 'Heavy' }


railways ['light_or_heavy_bin'] = railways ['light_or_heavy_bin'].replace(light_heavy_dict )


railways.head()




plt.figure( figsize = (14,8))
sns.violinplot(x="commodity", y="log_dist", hue="light_or_heavy_bin",
                    data=railways, palette="muted", split=True, order=commodity_dict.values())


plt.title( 'violinplot логарифма расстояния перевозки ' )

plt.show()


plt.figure( figsize = (14,8))
sns.violinplot(x="commodity", y="dist", hue="light_or_heavy_bin",
                    data=railways, palette="muted", split=True, order=commodity_dict.values())


plt.title( 'violinplot расстояния перевозки ' )

plt.show()

#5. Изобразите диаграмму рассеивания (scatterplot), для которой по горизонтали будет
#логарифм произведения расстояния на массу груза, а по вертикали логарифм провозной
#платы. Прокомментируйте результат. Что вы сделали с наблюдениями, для которых про-
#возная плата равна нулю? Почему? Пример приведен для подвыборки из 2000 наблюдений
#на рисунке 7


railways.head(1)


railways['log_of_weight_dist_poduct']    = np.log(railways.weight * railways.dist)



railways['log_of_amount'] = np.log(railways['amount'] +1 )



# если прибавить единицу



plt.figure( figsize = (16,16))
sns.jointplot(x="log_of_weight_dist_poduct", y="log_of_amount", data=railways, kind="reg")
plt.show()


#Если убрать нулевые значения




plt.figure( figsize = (16,16))
sns.jointplot(x="log_of_weight_dist_poduct", y="log_of_amount", data=railways[railways.log_of_amount>0   ], kind="reg")
plt.show()






