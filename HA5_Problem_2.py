import pandas as pd
import zipfile
import matplotlib.pylab as plt
import seaborn as sns
import math
import warnings
warnings.filterwarnings("ignore")


#Task_1
zf = zipfile.ZipFile('railways.zip')
zn = zf.namelist()
railway = zf.open(zn[0])
station = zf.open(zn[1])
dfRailway = pd.read_csv(railway)
dfStation = pd.read_csv(station)

print(dfRailway[dfRailway.columns.values[:5]].head())
print(dfStation[dfStation.columns.values[:3]].head())


#Task_2
plt.figure(figsize=(8, 4))
sns.distplot(dfRailway.dist, bins=100, color='b', kde_kws={'color': 'g', 'shade': True, 'label': 'Distance'})
plt.legend(loc='best')
plt.xlabel('')
plt.tight_layout()
#plt.savefig('task_21.svg')
plt.show()

dfLog = pd.DataFrame(list(map(math.log, dfRailway.dist)), columns=['km'])

plt.figure(figsize=(8, 4))
sns.distplot(dfLog.km, bins=100, color='b', kde_kws={'color': 'g', 'shade': True, 'label': 'log Distance'})
plt.legend(loc='best')
plt.xlabel('')
plt.tight_layout()
#plt.savefig('task_22.svg')
plt.show()


#Task_3
setComm = {1: 'Coal', 2: 'Oil', 3: 'Ores', 4: 'Metals',
           5: 'Wood', 6: 'Constructions', 7: 'Fertilizers',
           8: 'Grains', 9: 'Petrol', 10: 'Other'}
dfLog['Commodity'] = list(map(lambda x: setComm[x], dfRailway.commodity))
dfLog['Ind'] = dfRailway['commodity']
dfLog['Weight'] = dfRailway['weight']
dfLog = dfLog.sort_values(by='Ind')

plt.figure(figsize=(8, 4))
sns.boxplot(x=dfLog.Commodity, y=dfLog.km)
plt.xlabel('Commodity type', fontsize=12)
plt.ylabel('log Distance', fontsize=12)
plt.xticks(rotation='vertical')
plt.tight_layout()
#plt.savefig('task_3.svg')
plt.show()


#Task_4
med = dfLog.groupby('Commodity')['Weight'].median()
setWeight = {}
for i in range(len(med)):
    setWeight[med.index[i]] = med[i]
dfLog['binWeight'] = list(map(lambda x, y: ('Heavy' if y > setWeight[x] else 'Light'), dfLog.Commodity, dfLog.Weight))
dfLog = dfLog.sort_values(by=['Ind', 'binWeight'], ascending=(True, False))

plt.figure(figsize=(8, 4))
sns.violinplot(x='Commodity', y='km', hue='binWeight', split=True, data=dfLog, palette='muted')
plt.xlabel('Commodity type', fontsize=12)
plt.ylabel('log Distance', fontsize=12)
plt.xticks(rotation='vertical')
plt.tight_layout()
#plt.savefig('task_4.svg')
plt.show()


#Task_5
dfLog2 = dfRailway[['amount', 'weight', 'dist']][dfRailway['amount'] > 0]
dfLog2['logA'] = list(map(math.log, dfLog2['amount']))
dfLog2['logWD'] = list(map(math.log, dfLog2['weight'] * dfLog2['dist']))

df2000 = dfLog2.sample(2000)

plt.figure(figsize=(8,4))
sns.jointplot(x='logWD', y='logA', data=df2000, kind='reg', scatter_kws={'alpha': 0.8}, annot_kws={'loc': 'upper right'})
plt.ylabel('log(Amount)', fontsize=12)
plt.xlabel('log(Weight * Distance)', fontsize=12)
plt.savefig('task_5(2000).svg')
plt.show()
