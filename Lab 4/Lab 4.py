#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# This lab will practice the exercises in the demo document of the `pandas` package. We will also look at some geospatial techniques applied in Python and discuss the differences between spatial analysis in Python and R.

# ## Data import and cleaning (included in the demo):

# In[11]:


import pandas
import numpy as np


# In[12]:


data = pandas.read_csv('data/CAINC1__ALL_STATES_1969_2017.csv', encoding='latin-1', 
                      skipfooter=3, engine='python')
data.isna().sum() # so no na values in the numpy / pandas sense
data1 = data.replace("(NA)", 0)
data1['1969'] = data1['1969'].astype(int)
small = data[data.LineCode.isin( [2, 3] )]
for year in range(1969, 2018):
    small = small[small[str(year)] != "(NA)"] #drop all records with NA

convert_dict = dict([(str(year), int) for year in range (1969, 2018)])
small = small.astype(convert_dict)
geofips = pandas.unique(small.GeoFIPS)
small['GeoFIPS'] = [fips.replace("\"", "").strip() for fips in small.GeoFIPS]
geofips = pandas.unique(small.GeoFIPS)
pc_inc = small[small.LineCode==3]


# # Pandas

# __Exercise: \newline
# Identify the area with the lowest per-capita income each year.__

# In[13]:


min_ids = pc_inc.iloc[:, 8:].idxmin() 
for y, min_id in enumerate(min_ids):
    year = y + 1969
    name = pc_inc.loc[min_id].GeoName
    pci = pc_inc.loc[min_id, str(year)]
    print(year, pci, name)


# __Exercise: 
# As a percentage of the minimum per-captia income, calculate the relative income gap between the extremes of the income distribution each year.
# Identify the year with the maximum relative income gap.__

# In[14]:


max_ids = pc_inc.iloc[:, 8:].idxmax() 
idxs = zip(min_ids, max_ids)
ratio = 0.0
ratios = []
for y, ids in enumerate(idxs):
    min_id, max_id = ids
    year = y + 1969
    name = pc_inc.loc[min_id].GeoName
    pci_min = pc_inc.loc[min_id, str(year)]
    pci_max = pc_inc.loc[max_id, str(year)]
    r = pci_max / pci_min
    ratios.append(r)
    if r > ratio:
        ratio = r
        max_year = year
print("Maximum relative gap: {} occurred in {}".format(ratio, max_year))
res_df = pandas.DataFrame({'year': range(1969, 2018), 'ratio': ratios})
res_df


# # Visualization
# This section will explore spatial data visualization functions within Python.

# In[15]:


get_ipython().run_line_magic('matplotlib', 'inline')

import geopandas
import seaborn
import contextily
import matplotlib.pyplot as plt
import pandas

db = geopandas.read_file('/Users/ryan/Desktop/UChicago/SOCI 30253/Final_Project_CA_Aviation/geo_export_7550259c-c552-465b-add9-d4ec4ffcee81.shp')


# In[16]:


seaborn.jointplot('aptpo', 
                  'opspo', 
                  db, 
                  kind='kde')


# # Discussions
# This section discusses differences in data analytics in R and Python.

# ## Data Storage
# 

# ## Spatial Data Storage

# ## Other Differences

# This is the end of Lab 4.
