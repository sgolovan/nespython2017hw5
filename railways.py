import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#initialization of sns with default parameters for styles, fonts, palette, etc.
sns.set()

#2.1
zp = zipfile.ZipFile("railways.zip")
railways = pd.read_csv(zp.open("railways201208.csv"), index_col = 0)
stations = pd.read_csv(zp.open("stations.csv"), index_col = 0)
print(railways.iloc[:5,:5])
print(stations.iloc[:5,:3])

#2.2
railways["log Distance"] = np.log(railways["dist"])
#Rice rule for number of bins
bins = int(2 * len(railways["log Distance"]) ** (1/3))

plt.figure(1)
sns.distplot(railways["dist"], bins = bins, axlabel = False,
             hist_kws = {"alpha" : 1},
             kde_kws = {"color" : "darkgreen", "alpha" : 0.3,
                        "label" : "Distance", "shade" : True})
plt.figure(2)
sns.distplot(railways["log Distance"], bins = bins, axlabel = False,
             hist_kws = {"alpha" : 1},
             kde_kws = {"color" : "darkgreen", "alpha" : 0.3,
                        "label" : "log Distance", "shade" : True})

#2.3
plt.figure(3)
#providing space for vertical labels on x, since they wouldn't fit
#with standard parameters
plt.gcf().subplots_adjust(bottom = 0.30)
sns.set(font = "Times New Roman")

commodityDict = {1 : "Coal",
                 2 : "Oil",
                 3 : "Ores",
                 4 : "Metals",
                 5 : "Wood",
                 6 : "Constructions",
                 7 : "Fertilizers",
                 8 : "Grains",
                 9 : "Petrol",
                 10 : "Other"
                 }
railways["Commodity type"] = railways["commodity"].replace(commodityDict)

b = sns.boxplot(x = "Commodity type", y = "log Distance",
                 data = railways.sort_values(by = ['commodity']))
#making labels vertical by rotating on 90 degrees
b.set_xticklabels(b.get_xticklabels(), rotation = 90)

#2.4
plt.figure(4)
plt.gcf().subplots_adjust(bottom = 0.30)

medians = railways[['commodity', 'weight']].groupby('commodity').median()
#merging railways with medians on column commodity in railways and index
#in medians groupby, resulting columns weight_x is indiviual weight,
#weight_y is median weight in group category
railways = pd.merge(railways, medians, left_on = 'commodity', right_index = True)
#adding categorization by heavy and light weight relative to median
railways["Weight"] = np.where(railways['weight_x'] >= railways['weight_y'],
                                     'Heavy', 'Light')

#violin plot with categorization by commodity type and weight category
v = sns.violinplot(x = "Commodity type", y = "log Distance", hue = 'Weight',
                    data = railways.sort_values(by = ['commodity']), split = True)
v.set_xticklabels(v.get_xticklabels(), rotation = 90)

#2.5
#replacing rows with nans where amount is less or equal to 0, since
#logarithm for these numbers non-existent
railways[railways["amount"] <= 0] = np.nan
railways.dropna()
#since log(xy) = log(x) + log(y), adding 
g = sns.jointplot(x = railways["log Distance"] + np.log(railways["weight_x"]),
                 y = np.log(railways["amount"]), kind = "reg",
                 marginal_kws=dict(
                     hist_kws = dict(edgecolor = 'k', linewidth = 0.2 ))
                  )
g.set_axis_labels(r"$\log(weight \cdot dist)$",
                  r"$\log(amount)$")
plt.show()
