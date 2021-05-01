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

# # Introduction
# This notebook analyses which parts of the city that have lower income levels are not within 10 minutes of affordable food initative provision.
# It is work in progress and should not be quoted. It requires the other notebook in the container to be run first.

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

# # Takes the food outlet locations, calculate 10 minute isochrone and convert to geojson

## Reads in the Liverpool boundary file
filename='Data/Out/Liverpool_boundary.geojson'
file = open(filename)
Liverpool_boundary = gpd.read_file(file)

# +
# Read in the affordable food initatives
filename = "Data/Out/Affordable_food_iniatives.geojson"

file = open(filename)
Affordable_food_outlets = gpd.read_file(file)

# +
# Read in Emergency_food_suppliers
filename = "Data/Out/Emergency_food_suppliers.geojson"

file = open(filename)
Emergency_food_suppliers = gpd.read_file(file)

# +
# Characteristics for API calls to calculate 10 minute walking time

urlBase = 'https://api.mapbox.com/isochrone/v1/mapbox/'
profile = 'walking/'
minutes = 10
mapboxglaccessToken = 'pk.eyJ1Ijoiam9obmFyZGF2aWVzIiwiYSI6ImNpeHRmZjhlYjAwMmUycW9qbHRvem0xa3gifQ.oQ9cnn8b5HATalxv9rppYg'


# Function to make calls to the mapbox isochrone apis
def isochrone_api(x):
   api_call=urlBase+profile +str(x['lon'])+','+str(x['lat'])+'?contours_minutes='+str(minutes)+'&polygons=true&access_token='+mapboxglaccessToken
   try:
    walk_dist=requests.get(api_call)
    walk_iso= walk_dist.json()['features'][0]
   except:
    walk_iso="call_failed"
   return walk_iso


# -

# Call the isochrone API for each of the food output locations
Affordable_food_outlets['walking_dist']=Affordable_food_outlets.apply(isochrone_api,axis=1)

Emergency_food_suppliers['walking_dist']=Emergency_food_suppliers.apply(isochrone_api,axis=1)

# Take the outputs and turn into json
travel_distances = FeatureCollection(Affordable_food_outlets['walking_dist'].values.tolist()+Emergency_food_suppliers['walking_dist'].values.tolist())

# Ensures geojson follows the right handed rule
travel_distances= rewind(travel_distances)

# Convert to geopandas data frame
travel_distances = gpd.GeoDataFrame.from_features(travel_distances["features"])

# Set projection
travel_distances= travel_distances.set_crs("EPSG:4326")

# Check it plots
ax =  Liverpool_boundary.plot(color='cyan', figsize=(6,13))
ax.axis('off') # Turns off the axis
plt.title("Areas within 10 minutes of affordable food initative provision")
travel_distances.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax);

# Export
with open('Data/Out/Isochrone.geojson', 'w') as f:
   dump(travel_distances, f)

# # Identify areas with higher levels of deprivation which have lower levels of access

# +
filename="Data/Out/Liverpool_lsoa.geojson"
    
file = open(filename)
Lsoa_multdep = gpd.read_file(file)
# -

Lsoa_multdep.plot()

# List the variables
list(Lsoa_multdep)

# Select the areas in the city in the lowest income quintile
Lower_income=Lsoa_multdep[Lsoa_multdep['Income Domain numerator_rank']==5]

ax = Liverpool_boundary.plot(color='cyan', figsize=(6,13))
ax.axis('off') # Turns off the axis
plt.title("Areas in lowest income quintle")
Lower_income.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax);

#Lower income levels within 10 minutes of affordable food initative provision
lower_income_withaccess = gpd.overlay(Lower_income, travel_distances, how='intersection')
ax = Liverpool_boundary.plot(color='cyan', figsize=(6,13))
ax.axis('off') # Turns off the axis
plt.title("Areas in lowest income quintle within 10 minutes of affordable food initatives")
lower_income_withaccess.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax);

# +
#Lower income levels not within 10 minutes of affordable food initative provision

lower_income_withoutaccess = gpd.overlay(Lower_income, travel_distances, how='difference')

ax = Liverpool_boundary.plot(color='cyan', figsize=(6,13))
ax.axis('off') # Turns the axis off
lower_income_withoutaccess.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax)
plt.title("Areas in lowest income quintiles not within 10 minutes of affordable food initative provision")


# +
# Plots the lowest income quintile areas and those areas not within 10 minutes of affordable provision side by side

plt.figure(1, figsize=(14,26))
ax1 = plt.subplot(221)
Liverpool_boundary.plot(color='cyan', figsize=(6,13), ax=ax1)
ax1.axis('off') # Turns the axis off
Lower_income.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax1)
plt.title("Lowest income quintle areas")

ax2 = plt.subplot(222)
Liverpool_boundary.plot(color='cyan',figsize=(6,13), ax=ax2)
ax2.axis('off') # Turns off the axis
ax2.set_title("Lowest income quinitles not within 10 minutes of affordable food initative provision")
lower_income_withoutaccess.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax2);
# -

# # Create a geojson that for each layer in the map has those that are in the lowest decile and not within 10 minutes

# +
the_variables=['Total population: mid 2015 (excluding prisoners)_rank',
 'Dependent Children aged 0-15: mid 2015 (excluding prisoners)_rank',
 'Population aged 16-59: mid 2015 (excluding prisoners)_rank',
 'Older population aged 60 and over: mid 2015 (excluding prisoners)_rank',
# 'Working age population 18-59/64: for use with Employment Deprivation Domain (excluding prisoners)_rank',
 'Income Domain numerator_rank',
 'Income Deprivation Affecting Children Index (IDACI) numerator_rank',
 'Income Deprivation Affecting Older People Index (IDAOPI) numerator_rank',
 'Employment Domain numerator_rank',
 'Staying on in education post 16 indicator_rank',
 'Entry to higher education indicator_rank',
 'Adult skills and English language proficiency indicator_rank',
 'Years of potential life lost indicator_rank',
 'Comparative illness and disability ratio indicator_rank',
 'Acute morbidity indicator_rank',
 'Mood and anxiety disorders indicator_rank',
 'Road distance to a post office indicator (km)_rank',
 'Road distance to a primary school indicator (km)_rank',
 'Road distance to general store or supermarket indicator (km)_rank',
 'Road distance to a GP surgery indicator (km)_rank',
 'Household overcrowding indicator_rank',
 'Homelessness indicator (rate per 1000 households)_rank',
 'Owner-occupation affordability (component of housing affordability indicator)_rank',
 'Private rental affordability (component of housing affordability indicator)_rank',
 'Housing affordability indicator_rank',
 'Housing in poor condition indicator_rank',
 'Houses without central heating indicator_rank',
 'Road traffic accidents indicator_rank',
 'Nitrogen dioxide (component of air quality indicator)_rank',
 'Benzene (component of air quality indicator)_rank',
 'Sulphur dioxide (component of air quality indicator)_rank',
 'Particulates (component of air quality indicator)_rank',
 'Air quality indicator_rank',
 'Score_rank']

the_variables_short={'population':'Total population: mid 2015 (excluding prisoners)_rank','education':'Staying on in education post 16 indicator_rank',
'crowding':'Household overcrowding indicator_rank','income':'Income Domain numerator_rank','score':'Score_rank','morbidity': 'Acute morbidity indicator_rank'}

# +
from shapely.ops import orient # version >=1.7a2



def areas_not_close(x):
    not_access=gpd.overlay(x, travel_distances, how='difference')
    # Dissolve the contiguous polygons
    not_access=gpd.geoseries.GeoSeries([geom for geom in not_access.unary_union.geoms]).__geo_interface__
    # Converts to a geopandas dataframe
    not_access = gpd.GeoDataFrame.from_features(not_access)
    # Serts the orientation
    not_access.geometry = not_access.geometry.apply(orient, args=(-1,))
    return not_access

access_layer=[]

# Gets the distance data for the data that is at the lower super output area level
for x in the_variables_short.keys():
         print(x)  
         geom= areas_not_close(Lsoa_multdep[Lsoa_multdep[the_variables_short[x]]==5])
         geom= geom.set_crs("EPSG:4326")
         # Print to check it's producing sensible results
         geom.plot()
         access_layer.append(geom)
         geom.to_file("Data/Out/"+x+".geojson", driver='GeoJSON')
        
 


# -

# # Handles the data at the ward level

# +
filename = "Data/Out/Liverpool_wards.geojson"

file = open(filename)
Ward_level_data = gpd.read_file(file)
# -

# Add just the ward level obesity data on its own
geom= areas_not_close(Ward_level_data[Ward_level_data['Ward_Reception_Overweight_Obese_rank']==5])
# Print to check it's producing sensible results
geom= geom.set_crs("EPSG:4326")
geom.plot()
# access_layer.append(geom) Don't add this in as it has a different geometry
geom.to_file("Data/Out/Obesity.geojson", driver='GeoJSON')
                

# # Get the intersection and union of the shape files that are both in the lowest quintile and more than 10 minutes from an affordable food initative

# +
# Calculates both the union and the intersection of the the areas that have less than
for i,x in enumerate(access_layer):
          if i==1:
             access_layer[i].set_crs('epsg:4326', inplace=True)
             access_layer[i+1].set_crs('epsg:4326', inplace=True)
             past_intersect=gpd.overlay(access_layer[i], access_layer[i+1], how='intersection')
             past_intersect.set_crs('epsg:4326', inplace=True)
             past_union=gpd.overlay(access_layer[i], access_layer[i+1], how='union')
             past_union.set_crs('epsg:4326', inplace=True)
          elif i >1 and i <(len(access_layer)-1):
             access_layer[i].set_crs("EPSG:4326")
             access_layer[i+1].set_crs("EPSG:4326") 
             past_intersect.set_crs("EPSG:4326")
             past_intersect=gpd.overlay(past_intersect, access_layer[i+1], how='intersection')
             past_union=gpd.overlay(access_layer[i], access_layer[i+1], how='union')
             past_intersect.plot()
             past_union.plot()

past_intersect.plot()
# -

past_intersect.set_crs('epsg:4326', inplace=True)
past_union.set_crs('epsg:4326', inplace=True)
ax = Liverpool_boundary.plot(color='cyan', figsize=(6,13))
ax.axis('off') # Turns the axis off
past_intersect.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax)
past_union.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax)
plt.title("Areas in lowest income quintiles not within 10 minutes of affordable food initative provision - Union and intersection")

plt.figure(1, figsize=(14,26))
ax1 = plt.subplot(221)
ax = Liverpool_boundary.plot(color='cyan', figsize=(6,13), ax=ax1)
ax.axis('off') # Turns the axis off
past_intersect.plot(alpha=0.5, edgecolor='k', cmap='tab10',ax=ax1)
plt.title("Areas in lowest income quintiles not within 10 minutes of affordable food initative provision - Union and intersection")

# +
ax=Liverpool_boundary.plot(color='cyan', figsize=(6,13))
past_union=gpd.overlay(past_union, Liverpool_boundary, how='intersection')


# Dissolve the contiguous polygons
past_union=gpd.geoseries.GeoSeries([geom for geom in past_union.unary_union.geoms]).__geo_interface__
past_union = gpd.GeoDataFrame.from_features(past_union)
# Sets the orientation
past_union.geometry = past_union.geometry.apply(orient, args=(-1,))
# Sets the projection
past_union.set_crs('epsg:4326', inplace=True)

past_union.plot(alpha=0.5, edgecolor='k', cmap='tab10', ax=ax) 
ax.axis('off') # Turns the axis off
plt.title("Areas in lowest income quintiles not within 10 minutes of affordable food initative provision - Union and intersection")
