
# coding: utf-8

# In[1]:

#HA5
import pandas as pd
import re
import requests
import zipfile
import os
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[2]:

#Problem 1
#1
path = '../data/'
os.makedirs(path, exist_ok=True)
link = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
filepath = path +'data.zip'
if not os.path.isfile(filepath):
    response = requests.get(link)
    with open(filepath, "wb") as file:
        file.write(response.content)
zf = zipfile.ZipFile(filepath)
print(zf.namelist())
data=pd.read_csv(zf.open('survey_results_public.csv'),sep=',', index_col=list(range(1)), na_values=['.'],header=0)
schema=pd.read_csv(zf.open('survey_results_schema.csv'),sep=',', index_col=list(range(1)), na_values=['.'],header=0)


# In[3]:

print(data.iloc[:,:1].head())


# In[4]:

print(schema.head())


# In[5]:

print(data.shape)


# In[6]:

#2
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='grey',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
plt.savefig('1.png',bbox_inches='tight') 
plt.show()


# In[7]:

url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
data1=urllib.request.urlopen(url).read()
soup = BeautifulSoup(data1, 'html.parser')
list2=[]
header=[]
for tr in soup.find_all('tr'):
    list1=[]
    for td in tr.find_all('td'):
        text=td.text
        list1.append(text)
    for th in tr.find_all('th'):
        text=th.text
        list1.append(text)
    list2.append(list1)
data1 = pd.DataFrame(list2)
data1.columns=data1.iloc[0]
data1 =data1.iloc[1:]
data1 =data1.drop('country', 1)


# In[8]:

#2
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='grey',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
x=pd.to_numeric(data1['longitude'], errors='coerce').dropna()
y=pd.to_numeric(data1['latitude'], errors='coerce').dropna()
m.scatter(x, y, s = 5, zorder=10, color='r')
plt.savefig('2.png',bbox_inches='tight') 
plt.show()


# In[9]:

dict1={'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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
for i in range(len(data1['name'])):
    if data1['name'].iloc[i] in dict1.values():
        for k, v in dict1.items():
            if v == data1['name'].iloc[i]:
                data1['name'].ix[i+1]=k      
data1=data1.set_index('name', drop=True)
task22 = data.groupby(['Country'])['Professional'].agg([pd.Series.count])
task22.sort_values(by='count', ascending=False, inplace=True)
task22.columns=['Country']
result2=task22.merge(data1,how='inner',left_index=True,right_index=True)


# In[10]:

#4 
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='grey',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
x=pd.to_numeric(result2['longitude'], errors='coerce')
y=pd.to_numeric(result2['latitude'], errors='coerce')
s1=result2['Country']
m.scatter(x, y, s=s1/50, zorder=10, color='r')
plt.savefig('3.png',bbox_inches='tight') 
plt.show()


# In[11]:

#Problem 2
#1
zf2 = zipfile.ZipFile('railways.zip')
print(zf2.namelist())
railways=pd.read_csv(zf2.open('railways201208.csv'),sep=',', na_values=['.'],header=0)
stations=pd.read_csv(zf2.open('stations.csv'),sep=',', na_values=['.'],header=0)


# In[12]:

print(railways.iloc[:,:5].head())


# In[13]:

print(stations.iloc[:,:3].head())


# In[14]:

#2
plt.figure(figsize=(8, 4))
sns.set_context('notebook')
sns.distplot(np.log(railways['dist']),bins=100, kde_kws={"color": "g",'shade': False, "lw": 1, "label": '$\mathrm{log\ Distance}$'},
            hist_kws=dict(color="blue", linewidth=0))
plt.legend()
plt.xlabel('')
plt.savefig('4.png',bbox_inches='tight') 
plt.show()


# In[15]:

plt.figure(figsize=(8, 4))
sns.distplot((railways['dist']),bins=100, kde_kws={"color": "g",'shade': False, "lw": 1, "label": '$\mathrm{Distance}$'},
            hist_kws=dict(color="blue", linewidth=0))
plt.legend()
plt.xlabel('')
plt.savefig('5.png',bbox_inches='tight')
plt.show()


# In[16]:

#3
railways['commoditycat']=railways['commodity'].astype('category')
railways['commoditycat']=railways['commoditycat'].cat.rename_categories(["Coal","Oil","Ores","Metals","Wood","Constructions","Fertilizers","Grains","Petrol","Other" ])


# In[17]:

railways['log_dist']=np.log(railways['dist'])
plt.figure(figsize=(8, 6))
sns.boxplot(x='commoditycat', y='log_dist', data=railways)
plt.xticks(rotation=90)
plt.xlabel('$\mathrm{Commodity\ type}$')
plt.ylabel('$\mathrm{log\ Distance}$')
plt.savefig('6.png',bbox_inches='tight')
plt.show()


# In[18]:

#4
railways['Weight']=railways['commoditycat']
railways['Weight']=railways['Weight'].cat.rename_categories(list(railways.groupby(['commoditycat'])['weight'].median()))
railways['Weight']=(railways['weight']>railways['Weight'].astype(float))
railways['Weight']=railways['Weight'].astype("category").cat.rename_categories(['Light','Heavy'])
plt.figure(figsize=(8, 6))
sns.violinplot(x='commoditycat', y='log_dist', data=railways,
                hue='Weight', split=True,  hue_order=['Light','Heavy'] ,
               linewidth=1.5)
plt.xticks(rotation='vertical')
plt.xlabel('$\mathrm{Commodity\ type}$')
plt.ylabel('$\mathrm{log\ Distance}$')
plt.ylim(0.5, 10.2)
plt.savefig('7.png',bbox_inches='tight')
plt.show()


# In[19]:

railways['amount'].describe()


# In[20]:

#5
railways['log_amount']=np.log(railways['amount'])
sample1 = railways[pd.qcut(railways['log_amount'],
                    [0, .001,1], labels=False) == 1]                                       
sample2=sample1.sample(2000)
plt.figure(figsize=(10, 10))

sns.jointplot(np.log(sample2['weight']*sample2['dist']), (sample2['log_amount']),
              size=6, kind='reg',x_jitter=.05, marginal_kws={'hist_kws': {'edgecolor': "black"}})
plt.xlabel('$\mathrm{log(}\it{weight\cdot dist)}$')
plt.ylabel('$\mathrm{log(}\it{amount)}$')
plt.savefig('8.png',bbox_inches='tight')
plt.show()

