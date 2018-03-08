
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile, io

#1.1
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
zip = requests.get(url)
unzip = zipfile.ZipFile(io.BytesIO(zip.content))

pu = unzip.open('survey_results_public.csv')
pub = pd.read_csv(pu,  header = 0)
publ = pub.copy()
publ = publ.set_index('Respondent')


sch =unzip.open('survey_results_schema.csv')
sche = pd.read_csv(sch, header = 0)
schem = sche.copy()
schem = schem.set_index('Column')

publ.iloc[:,:1].head()
schem.head()

print(len(publ),'вопросов')

print(publ.Professional.value_counts()['Professional developer'],' разработчиков')

#1.2
plt.figure(figsize = (10,15))
map1 = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='c')
map1.drawcoastlines()
map1.drawcountries(linewidth=0.3, antialiased = False) 
map1.fillcontinents(color='coral',lake_color='aqua')
map1.drawmapboundary(fill_color='aqua') 
plt.show()

#1.3
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url)
tab = pd.read_html(str(response.content))[0]
tab = pd.DataFrame(tab)

tabl = tab.copy()
tabl.columns = tabl.iloc[0]
tabl= tabl.reindex(tabl.index.drop(0))

tabl['latitude'] = tabl['latitude'].astype(float)
tabl['longitude'] = tabl['longitude'].astype(float)
tabl = tabl.set_index('name')

country = publ.Country.value_counts()

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
    
country = pd.DataFrame(country)
country.reset_index(inplace=True)

for i in dict.keys(): 
    country["index"].replace(i, value=dict[i], inplace=True)

country.set_index("index", inplace=True)

plt.figure(figsize = (20,40))
map2= Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='c')
map2.drawcoastlines()
map2.drawcountries(linewidth=0.3, antialiased = False) 
map2.fillcontinents(color='coral',lake_color='aqua')
map2.drawmapboundary(fill_color='aqua')
x, y = map2(tabl['longitude'], tabl['latitude'])
map2.scatter(x, y, marker='o', color='r', s = 10, zorder=10, edgecolors = 'black')
plt.show() 

# 1.4
new14 = pd.concat([tabl,country],axis=1, join='inner')
new14 = new14.rename(columns = {'Country':'respondents'})

plt.figure(figsize = (20,40))
map3 = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,resolution='c')
map3.drawcoastlines()
map3.drawcountries(linewidth=0.3, antialiased = False)
map3.fillcontinents(color='coral',lake_color='aqua')
map3.drawmapboundary(fill_color='aqua')
x, y = map3(new14['longitude'], new14['latitude'])
map3.scatter(x, y, marker='o', color='r', s = new14['respondents']/20, zorder=10, edgecolors = 'black')
plt.show()

#%%
import numpy as np
import seaborn as sns 

sns.set_palette('muted') 

#2.1
zip = zipfile.ZipFile('railways.zip')
data1 = pd.read_csv(zip.open('railways201208.csv'))
data2 = pd.read_csv(zip.open('stations.csv'))


data1 = pd.DataFrame(data1)
data2 = pd.DataFrame(data2)
print(data1.head())
print(data2.head())

#2.2
data1['log Distance'] = data1['dist'].apply(lambda x: np.log(x))
          
plt.figure(figsize=(10, 7))
sns.distplot(data1['dist'], bins = 150,kde=True,kde_kws={"color": "g","lw": 3, "label": "log Distance", "shade":True},hist_kws={"histtype": "stepfilled","alpha": 1}) 
plt.show()

plt.figure(figsize=(10, 7))
sns.distplot(data1['log Distance'], bins = 150,kde=True,kde_kws={"color": "g", "lw": 3, "label": "log Distance", "shade":True},hist_kws={"histtype": "stepfilled","alpha": 1})
plt.show()

#2.3   
dict={1:'Coal', 2:'Oil', 3:'Ores', 4:'Metals',5:'Wood', 6:'Constructions', 7:'Fertilizers', 8:'Grains', 9:'Petrol', 10:'Other'}

for i in dict.keys():
    data1['commodity'].replace(i, value=dict[i], inplace=True )
    
data1 = data1.rename(columns={'commodity':'Commodity type'}) 

#
plt.figure(figsize=(10, 7))
sns.boxplot(x='Commodity type', y='log Distance', data=data1,linewidth=3)
plt.xticks(rotation='vertical')
plt.show()

#2.4
data1 = data1.set_index('Commodity type')
data11 = data1.copy()

for i in data11.index.unique():
    data11.loc[i,'median'] = int(data11.loc[i,'weight'].median())
data11['Weight'] = data11['weight'] - data11['median']

def tails(x):
    x = int(x)
    if x > 0:
        return('Heavy')
    else:
        return('Light')        
data11['Weight'] = data11['Weight'].apply(tails)

plt.figure(figsize=(10, 7))
sns.violinplot(x=data11.index, y='log Distance',hue='Weight', hue_order=['Light','Heavy'], split=True,data=data11,linewidth=3)
plt.xticks(rotation='vertical')
plt.legend(title='Weight',loc='lower right')
plt.show()

#2.5

data11['log(weight * dist)'] = np.log(data11['weight']) + np.log(data11['dist'])
data11['log(amount)'] = np.log(data11['amount']) 

data11 = data11.reset_index()
data11 = data11.set_index('amount')
data11.drop(data11[data11.index == 0].index, inplace=True)


g = sns.jointplot(x='log(weight*dist)',y='log(amount)', data=data11, kind='reg')
g.fig.set_figwidth(8)
g.fig.set_figheight(8)
g.savefig('pic5.svg',bbox_inches = 'tight')
plt.show()

