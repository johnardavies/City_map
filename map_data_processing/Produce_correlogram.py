# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd #importing the Pandas Library as 'pd'
import numpy as np

#Imports spatial libraries
from keplergl import KeplerGl #importing KeplerGl
import geopandas as gpd #importing geopandas as 'gpd'
from shapely.geometry import Point
from shapely.geometry import box
import shapely.wkt
from geopy.geocoders import Nominatim # Imports the geopy for the geocoding
import geojson
from geojson import Point, Feature, FeatureCollection, dump
from geojson_rewind import rewind
import json



import xml.etree.ElementTree as ET
import requests
import matplotlib.pyplot as plt


from time import time
# -

# ls Data/Out/

# # Read in the files

# +
## Reads in the Liverpool boundary file
filename='Data/Out/Liverpool_lsoa.geojson'
Liverpool_lsoa = gpd.read_file(open(filename))

filename2='Data/Out/Affordable_food_iniatives.geojson'
Affordable_food_initatives = gpd.read_file(open(filename2))

filename3='Data/Out/Emergency_food_suppliers.geojson'
Emergency_food_suppliers = gpd.read_file(open(filename3))

filename4='Data/Out/Food_outlets_geo.geojson'
Food_outlets = gpd.read_file(open(filename4))

filename5='Data/Out/Supermarkets_geo.geojson'
Supermarkets = gpd.read_file(open(filename5))

# -

Liverpool_lsoa.head(n=5)

# # Ensure that the projection of everything is consistent

Liverpool_lsoa['geometry'] = Liverpool_lsoa['geometry'].set_crs("EPSG:4326")

Affordable_food_iniatives = Affordable_food_iniatives.set_crs("EPSG:4326")

# +
Emergency_food_suppliers=Emergency_food_suppliers.set_crs("EPSG:4326")

Food_outlets=Food_outlets.set_crs("EPSG:4326")


Supermarkets=Supermarkets.set_crs("EPSG:4326")
# -

# !pip install seaborn

Liverpool_lsoa["LSOA11CD"].value_counts()

Liverpool_lsoa["LSOA name (2011)_x"].value_counts()

# +
# Split the initatives down into the different kinds of initatives
# -

# # Count the number of food banks, pantries etc by lower super output areas

list(Liverpool_lsoa)


class Spatial_count:
    
  def __init__(self, spatial_polygon, spatial_points):
    
       self.spatial_polygon = spatial_polygon
       self.spatial_points=spatial_points
        
  #Counts the number of points falling within a given geography  
  def tablecount(self):

        # Does the spatial join
        dfsjoin = gpd.sjoin(self.spatial_polygon,self.spatial_points)
        
        # Creates a flag for the counts
        dfsjoin['flag']=1
 
        # Does a pivot table on the LSOA areas i.e. counts how many meetups by category (meetupcat) each geography has meetup groups for 
   
        dfpivot =dfsjoin[["LSOA11CD","flag"]].groupby(['LSOA11CD']).sum() #count().unstack(fill_value=0).stack()
    
      
  
        # Resets the index
        dfpivot=dfpivot.reset_index()
        

        return dfpivot
  

# +
#Pantrys['Category']='Pantry'
#Community_cafes['Category']='Community_cafes'
#Free_food_inititives['Category']='Free_food_inititives'
# Food_parcel['Category']='Food_parcels'
#  Meal_providers['Category']='Meal_providers'

Pub/bar/nightclub
Takeaway/sandwich shop
Restaurant/Cafe/Canteen

# -

import seaborn as sns

test

# +
food_sites=[Affordable_food_iniatives,Emergency_food_suppliers, Supermarkets , Food_outlets ]

Liverpool_lsoa_extra=Liverpool_lsoa

for i, elem in enumerate(food_sites): 
       # Drop the Liverpool column this is a hack (remove later by using a different dataset to get the points within Liverpool)
       try:
        del elem['LSOA11CD']
       except:
         print("No such column")
       spatial_join=Spatial_count(Liverpool_lsoa_extra,elem)
       count_table=spatial_join.tablecount()
       # Rename the count 
       count_table=count_table.rename(columns={"flag":str(i)+"_count"})
      # Merge the counts with the Liverpool lower super output area data 
       print(count_table)
       Liverpool_lsoa_extra=Liverpool_lsoa_extra.merge(count_table, how='left',left_on=['LSOA11CD'],  right_on=['LSOA11CD'])
venue_counts=['0_count','1_count','2_count', '3_count'] 

Liverpool_lsoa_extra[venue_counts]=Liverpool_lsoa_extra[venue_counts].fillna(0)

# -

# # Convert counts to density

Liverpool_lsoa_extra['area'] = Liverpool_lsoa_extra.geometry.area

for elem in venue_counts:
    Liverpool_lsoa_extra[elem+"_density"]= Liverpool_lsoa_extra[elem]/Liverpool_lsoa_extra['area']

# # Visualises the correlelogram

# +
# Selects the variables that we want to be on the correelogram

correlogram_vars=['0_count_density','1_count_density','2_count_density', '3_count_density', 'Income Domain numerator', 'Houses without central heating indicator','Total population: mid 2015 (excluding prisoners)']
                                               

# -

correlogram_data=Liverpool_lsoa_extra[correlogram_vars]

# +
#Calculates coocurrence which is a symmetric matrix, with the diagonal being the % of respondents reporting the category
results=correlogram_data.corr()

#Creates a mask to hide the upper triangle excluding the diagonal by having k=1
matrix = np.triu(results, k=1)

#Plots the heatmap with seaborn
fig, ax = plt.subplots(figsize=(12,12))  
sns.heatmap(results, annot=True,ax=ax, mask=matrix,  cmap ='RdBu_r', vmax=0.5, square=True, cbar=False)
ax.set_title('Correlation between different activities')
