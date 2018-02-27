import pandas as pd
import zipfile
import requests
import io
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math


#%%
#Task_1

url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
res = requests.get(url)
zf = zipfile.ZipFile(io.BytesIO(res.content))
dataFile = zf.open('survey_results_public.csv')
schemaFile =zf.open('survey_results_schema.csv')
dfData = pd.read_csv(dataFile)
dfSchema = pd.read_csv(schemaFile)

data = dfData[['Respondent', 'Professional']]
developer = data.groupby(['Professional'])['Respondent'].count()

schema = dfSchema[['Column', 'Question']]
question = schema['Question'].count()

print('В опросе было', question, 'вопроса.')
print('В опросе приняли участие', developer['Professional developer'], 'разработчик.')

data = data.set_index('Respondent')
schema = schema.set_index('Column')

print(data.head(), schema.head(), sep='\n\n')


#%%
#Task2
plt.figure(figsize = (18,25))

#Europe:  
#m = Basemap(projection='cyl',llcrnrlat=35,urcrnrlat=72, llcrnrlon=-11,urcrnrlon=50,resolution='c')

m = Basemap(projection='cyl', resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
#plt.savefig('fig_task_2.svg')
plt.show()


#%%
#Task_3
url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
response = requests.get(url)
country = pd.read_html(str(response.content))[0]
dfCountry = pd.DataFrame(country)
dfCountry.columns = list(dfCountry.loc[0])
dfCountry = dfCountry.loc[1:]
dfCountry = dfCountry[['latitude', 'longitude', 'name']]
dfCountry.rename(columns={'name': 'Country'}, inplace=True)
dfCountry = dfCountry.set_index('Country')

plt.figure(figsize = (18,25))

#Europe:  
#m = Basemap(projection='cyl',llcrnrlat=35,urcrnrlat=72, llcrnrlon=-11,urcrnrlon=50,resolution='c')

m = Basemap(projection='cyl', resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
x, y = m(dfCountry['longitude'], dfCountry['latitude'])
m.scatter(x, y, marker='o', color='r', s = 15, zorder=10, edgecolors = 'black')
#plt.savefig('fig_task_3.svg')
plt.show()


#%%
#Task_4
setCountry = {
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
 
population = dfData.groupby(['Country'])['Country'].count()
dfPop = pd.DataFrame(population)
dfPop.rename(columns={'Country': 'population'}, inplace=True)
dfPop = dfPop.reset_index()
dfPop['Country'] = list(map(lambda x: (setCountry[x] if x in setCountry else x), dfPop.Country))
dfPop = dfPop.set_index('Country')

dfMerge = pd.merge(dfCountry, dfPop, right_index=True, left_index=True)
dfMerge = dfMerge.sort_values(by='population', ascending=False)
dfMerge['logPop'] = list(map(math.log2 ,dfMerge['population']))
dfMerge['logPop'] = (dfMerge['logPop'] + 0.1) * 50

plt.figure(figsize = (18,25))

#Europe:  
#m = Basemap(projection='cyl',llcrnrlat=35,urcrnrlat=72, llcrnrlon=-11,urcrnrlon=50,resolution='c')

m = Basemap(projection='cyl', resolution='c')
m.drawcoastlines()
m.drawcountries(linewidth=0.25, antialiased = False)
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
x, y= m(dfMerge['longitude'], dfMerge['latitude'])

#Сглаженные логарифмом:
#m.scatter(x, y, dfMerge['logPop'], marker='o', color='r', zorder=10, edgecolors = 'black')

#Несглаженные логарифмом:  
m.scatter(x, y, dfMerge['population']/5, marker='o', color='r', zorder=10, edgecolors = 'black')

#plt.savefig('fig_task_4(4).svg')
plt.show()
