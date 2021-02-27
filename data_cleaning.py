# this file will upload the data and perfrom data cleaning on it

import numpy as np      		# linear algebra
import pandas as pd     		# data processing, file I/O
import matplotlib.pyplot as plt     	# show he graphs
import seaborn as sns               	# to plot the graphs
from collections import Counter


exdf = pd.read_csv("2018-2010_export.csv")
imdf = pd.read_csv("2018-2010_import.csv")

# basic data review of export
print(exdf.head())
print(exdf.tail())
print(exdf.info())
print(exdf.describe())
print(exdf.columns)
print(exdf['Commodity'])

# basic data review of import
print(imdf.head())
print(imdf.tail())
print(imdf.info())
print(imdf.describe())
print(imdf.columns)
print(imdf['Commodity'])

# sum of null values column wise
print(exdf.isnull().sum())
print(imdf.isnull().sum())

# 0 in value column
print(exdf[exdf.value==0].head())
print(imdf[imdf.value==0].head())

# unspecified country
print(exdf[exdf.country == 'UNSPECIFIED'].head())
print(imdf[imdf.country == 'UNSPECIFIED'].head())



# replace the missing values in value column with their mean groupby the commodity
#export data
exdf['value'].fillna(exdf.groupby('Commodity')['value'].transform('mean'), inplace=True)
#import data
imdf['value'].fillna(imdf.groupby('Commodity')['value'].transform('mean'), inplace=True)

# total export value
print('total amount export', exdf['value'].sum())

# checking null values again
print(exdf['value'].isnull().sum())
print(imdf['value'].isnull().sum())


# yearly export
yearly_export = exdf.groupby('year')['value'].sum()         # sum of value columns on the basis of year
print(yearly_export)
print(type(yearly_export))
# plot the graph
sns.lineplot(x=yearly_export.index, y=yearly_export)
plt.title('Total export from 2010-2018')
plt.show()

yearly_import = imdf.groupby('year')['value'].sum()
sns.lineplot(x=yearly_import.index, y=yearly_import)
plt.title('total import from year 2010-2018')
plt.show()


# to find the importer list
yr_unique = exdf['year'].unique()
print(yr_unique)
print(yr_unique[1])
importer_list = []
for i in yr_unique:
    importer_list.extend(exdf[exdf['year'] == i][['country', 'value']].groupby(['country']).sum().sort_values(by='value',
                        ascending=False).iloc[0:3, :].index)
print("this is importer list -->\n", importer_list)

""" some decoding part of above for loop """
"""
exdf[exdf['year'] == i] -->> this line is used to choose the year
[['country', 'value']] -->> this to choose the country and value for selected year
groupby(['country']) -->> groupby with country
sum()  -->> with groupby via 'country', sum the value
sort_values(by='value', ascending=False) -->> sort by values and not in ascending order
.iloc[0:3, :].index -->> selecting the index
"""
print(exdf[exdf['year'] == 2011][['country', 'value']].groupby('country').sum())
print(exdf[exdf['year'] == 2011][['country', 'value']].groupby('country').sum().sort_values(by='value', ascending=False).iloc[0:3, :].index)

yr_unique2 = imdf['year'].unique()
print(yr_unique)
print(yr_unique[1])
exporter_list = []
for i in yr_unique2:
    exporter_list.extend(imdf[imdf['year'] == i][['country', 'value']].groupby(['country']).sum().sort_values(by='value',
                        ascending=False).iloc[0:3, :].index)
print(exporter_list)

favor_importer = Counter(importer_list).most_common(3)
print(favor_importer)

for country, count in favor_importer:
    importer = exdf[exdf['country'] == country][['year', 'value', 'country']].groupby(['year']).sum()

print(importer)

print(importer.index)

sns.lineplot(x=importer.index, y=importer['value'])
plt.show()

# top 10 trade partners
trade_partner = exdf[['country', 'value']].groupby('country').sum().sort_values(by='value', ascending=False)
plt.figure(figsize=(15, 6))
sns.barplot(trade_partner.index, trade_partner.value, palette='Blues_d')
plt.show()

# most commodities exported
trade_commodities = exdf[['Commodity','value']].groupby(['Commodity']).sum().sort_values(by = 'value', ascending=False).head(10)
print(trade_commodities)
