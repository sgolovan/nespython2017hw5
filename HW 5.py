import pandas as pd
import requests
import zipfile
import numpy as np
import warnings

import seaborn as sns
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt

sns.set(style='whitegrid', rc={'grid.color' : '.9'}, font_scale=1.2)
warnings.filterwarnings('ignore')


'''
Task 1
'''

# Downloading data
r = requests.get('https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM')

with open('survey_results.zip', 'wb') as f:
    f.write(r.content)
    
with zipfile.ZipFile('survey_results.zip','r') as zf:
    zf.extractall('survey_results/')
    zf.close()
    
data = pd.read_csv('survey_results/survey_results_public.csv', index_col=0)
schema = pd.read_csv('survey_results/survey_results_schema.csv', index_col=0)

print('Total number of questions:', data.shape[1])
print('Total number of respondents:', data.shape[0])

# Getting number of respondents from each country
respondents_by_country = data.groupby('Country')['Country'].count().sort_values(ascending=False)

# Dictionry for replacing countries names
replaces = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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

# Replacing countries names
respondents_by_country.index = pd.DataFrame(respondents_by_country.index.tolist()).replace(replaces)[0].values

# Dowloading mid-coutry coordinates
countries = pd.read_html('https://developers.google.com/public-data/docs/canonical/countries_csv')[0]
countries.columns = countries.iloc[0]
countries = countries.iloc[1:,1:]
countries.index = countries['name']
countries.index.name = 'Country'
countries.drop('name', axis=1, inplace=True)
countries.dropna(inplace=True)
countries = countries.astype(float)

countries_coord = pd.concat([respondents_by_country, countries], axis=1).dropna()

# Plotting the map
plt.figure(figsize=(14,10))
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.scatter(countries_coord['longitude'], countries_coord['latitude'], 
          countries_coord['Country']/25, latlon=False, zorder=10, color='maroon')
m.drawmapboundary(linewidth=3, fill_color='paleturquoise')
m.fillcontinents(color='coral',alpha=0.75)
#m.bluemarble()
plt.title('Respondents distribution over the world')
plt.show()


'''
Task 2
'''

# Loading data
railways = pd.read_csv('railways201208.csv')
stations = pd.read_csv('stations.csv')

print(railways.iloc[:5,:5])
print(stations.iloc[:5,:5])

# dict for commodities codes
commodities = {1:'Coal', 
               2:'Oil', 
               3:'Ores', 
               4:'Metals', 
               5:'Wood', 
               6:'Constructions', 
               7:'Fertilizers', 
               8:'Grains', 
               9:'Petrol', 
               10:'Other'}


# Plotting histogram and pdf for distance and log-distance distributions
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(14,5))

ax1.set_title('Distance distribution')
sns.distplot(railways.dist, bins=100, ax=ax1)
sns.despine(left=True, ax=ax1)
ax1.set_xlabel('Distance')
ax1.set_ylabel('PDF')

ax2.set_title('Distance logarithm distribution')
sns.distplot(np.log(railways.dist), bins=100, ax=ax2)
sns.despine(left=True, ax=ax2)
ax2.set_xlabel('Distance logarithm')
ax2.set_ylabel('PDF')

plt.savefig('pdf.eps', format='eps', dpi=1000)
plt.show()


# Plotting boxplot for log-distance for each commodity type
plt.figure(figsize=(10,5))
sns.boxplot(x=railways['commodity'], y=np.log(railways['dist']), 
            width=0.75, linewidth=1)
sns.despine(left=True)
plt.xlabel('Commodity')
plt.ylabel('Distance logarithm')
plt.xticks(plt.xticks()[0], commodities.values(), rotation=30)
plt.show()


# Creating Weight columns, that tells if package if heavy or light
weight_medians = railways.groupby('commodity')['weight'].median()
railways['Weight'] = railways['weight'] > weight_medians[railways['commodity']].values
railways['Weight'].replace({True: 'Heavy', False: 'Light'}, inplace=True)

# Plotting violin plot for log-distance for each commodity type and weight category
plt.figure(figsize=(10,5))
sns.violinplot(x=railways['commodity'], y=np.log(railways['dist']), 
               hue=railways['Weight'], split=True)
sns.despine(left=True)
plt.xlabel('Commodity')
plt.ylabel('Distance logarithm')
plt.xticks(plt.xticks()[0], commodities.values(), rotation=30)
plt.show()


# Plotting regression of log (dist x weight) on log (amount paid), dropping
# packages with no amount, since they don't fit in log-based paradigma.
railways2 = railways[railways['amount'] > 0]
sns.jointplot(x=np.log(railways2['dist']*railways2['weight']), 
              y=np.log(railways2['amount']), 
              kind='reg', size=6)\
            .set_axis_labels('$\log(weight \circ dist)$', '$\log(amount)$')
sns.despine(left=True)
plt.show()