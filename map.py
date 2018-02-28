import pandas as pd
import requests
import zipfile
import io
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

centers = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
survey = "https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM"
data = "survey_results_public.csv"
schema = "survey_results_schema.csv"
survey = requests.get(survey)
zp = zipfile.ZipFile(io.BytesIO(survey.content))
data = pd.read_csv(zp.open(data), index_col = 0)
schema = pd.read_csv(zp.open(schema), index_col = 0)

#1.1
print(data.iloc[:, :1].head())
print(schema.head())
respondents = len(data.index)
questions = len(schema.index)
print("Number of respondents:", respondents)
print("Number of questions:", questions)

#1.2
plt.figure(1)
#I'm good with default initialization parameters,
#since default projection is Cylindrical Equidistant Cylindrical Projection,
#condition on cylindrical projection is satisfied
#additionally I increased resolution to 'low'
#since with default crude too many islands aren't showed
m = Basemap(resolution = 'l')
m.drawcoastlines()
#country borders
m.drawcountries()
#i selected brown - earth, blue - water, yellow - centers,
#because it makes more easy to see centers on the map
m.fillcontinents(color='brown', lake_color='blue')
#fill water surface outside of continents
m.drawmapboundary(fill_color='blue')

#1.3
plt.figure(2)
#reading tables to list
centers = pd.read_html(centers)
#since there is only 1 table read first element in the list
centers = centers[0].dropna()
#drop first row - strings which supposed to be headers
centers = centers.reindex(centers.index.drop(0))
#reset index
centers = centers.reset_index(drop = True)
#assign own headers
centers.columns = ["id", "latitude", "longitude", "Country"]
centers.latitude = centers.latitude.apply(float)
centers.longitude = centers.longitude.apply(float)

m = Basemap(resolution = 'l')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='brown', lake_color='blue')
m.drawmapboundary(fill_color='blue')
#computing map projected coordinates
lons, lats = m(centers.longitude, centers.latitude)
#areas for country centers
s = np.full(len(lons), 10)
#set drawing order of centers to high value to see them on top of other layers for sure
m.scatter(lons, lats, s, color = "yellow", zorder = 10)

#1.4
plt.figure(3)
countryDict = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
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
surveyCountries = data.groupby('Country').size()
surveyCountries = surveyCountries.reset_index()
#adjust country names
surveyCountries["Country"] = surveyCountries["Country"].replace(countryDict)
merged = pd.merge(surveyCountries, centers, on = "Country")

m = Basemap(resolution = 'l')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='brown',lake_color='blue')
m.drawmapboundary(fill_color='blue')
lons, lats = m(merged.longitude, merged.latitude)
#adjust center sizes of countries proportionally to programmers in that country,
#but with size which wouldn't make map obscure
m.scatter(lons, lats, s = merged[0]/merged[0].sum() * 1000, color = "yellow", zorder = 10)
plt.show()

