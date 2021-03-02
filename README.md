## This is a mapboxGL map of the city of Liverpool (The map is work in progress)

The map itself is visible at:
https://johnardavies.github.io/City_map/#


The food standards agency data that has been mapped for Liverpool is available from:
https://ratings.food.gov.uk/default/en-GB


The index of multiple deprivation data that hae been mapped is available from
https://data-communities.opendata.arcgis.com/datasets/d4b79be994ac4820ad44e10ded313df3_0

**Data processing for map**

The processing of the food standards agency and Food banks data is done using the notebook
Liverpool_map.ipynb the files and the Dockerfile in the map_data_processing folder

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
