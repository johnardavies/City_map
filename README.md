## This is a mapboxGL map of the city of Liverpool (The map is work in progress)

The map itself is visible at:
https://johnardavies.github.io/City_map/#


###The data that the map is based on:


***The general food outlet information***
This is obtained by geocoding the list of Liverpool food outlets on the [Food Standards Agency website](https://ratings.food.gov.uk/default/en-GB)

***The affordable food initatives (Food pantries, Free food initatives, Community cafes) information***
This has been obtained from the [Feeding Liverpool map](http://www.feedingliverpool.org/resources)

***The information on Foodbanks***
This has been obtained from Google searches and will be updated

***The walking distance layer***
This is created by calling the [MapboxGL isochrone API](https://docs.mapbox.com/help/tutorials/get-started-isochrone-api/)

***The reception class obesity layer at the ward level***
This data has been obtained from Liverpool council

***The e-food deserts index layer***
This is an index measuring the degree to which areas have characteristics associated with food deserts. The index is produced by
 CDRC and was obtained from their [website](https://data.cdrc.ac.uk/dataset/e-food-desert-index#:~:text=The%20e%2Dfood%20deserts%20index,density%20of%20grocery%20retail%20facilities)

***All other layer data***
This is taken from the [index of multiple deprivation](https://data-communities.opendata.arcgis.com/datasets/d4b79be994ac4820ad44e10ded313df3_0)


### Data processing for map

The processing of the food standards agency and Food banks data is done using the notebooks:\

**1. Liverpool_map.ipynb** This generates the geojson files for the layers (isochrone layer excepted) and the food outlet sites\
**2. Further_analysis.ipynb** This generates geojson for areas that are in the lowest 20% of layers data and more than 10 mins from an affordable food outlet

These are run within a container using the Dockerfile in the map_data_processing folder which also contains the data in the Data folder.
They process the data and then output the files to the Out folder 

To build the container image for the data processing after cloning the repo, tagging it as map_processing
```
$ docker build --tag map_processing map_data_processing
```
To run the container on port 8009 (mapped to the container port 8009)
```
$ docker run -p 8009:8009 --init map_processing
```
To download the processed files for the map
```
$ docker cp container_id:/notebooks/Data/Out Destination_location
```

### Viewing the map locally

To run the map locally
```
$ git clone https://github.com/johnardavies/City_map
```
and from inside the City_map folder in the same directory as the index file run the below, setting port_id to the port you want to see map on e.g. 8011
```
$  python -m http.server port_id
```
The map will then be visible on http://localhost:port_id e.g. http://localhost:8011
