## This is a mapboxGL map of the city of Liverpool (The map is work in progress)

The map itself is visible at:
https://johnardavies.github.io/City_map/#


### The data that the map is based on:


***The general food outlet information***
This is obtained by geocoding the list of Liverpool food outlets on the [Food Standards Agency website](https://ratings.food.gov.uk/default/en-GB)\
\
For the purposes of the map food outlets that are wholesale or not normal consumer retail are present in the Food_outlets_geo.geojson, but are filtered out in the map \
These being: outlets of the type" 'Mobile caterer','Distributors/Transporters','Manufacturers/packers','Hospitals/Childcare/Caring Premises','School/college/university' 
'Other catering premises','Hotel/bed & breakfast/guest house'\
\
Due to supermakets being a separate layer in the map they are included in Supermarkets_geo.geojson. This layer is created with the Liverpool_map.ipynb notebook

***The affordable food initatives (Food pantries, Free food initatives, Community cafes  information***
This has been obtained from the [Feeding Liverpool map](http://www.feedingliverpool.org/resources)\
The original excel file is Affordable_food_inititives_Liverpool.xlsx which is processed with Liverpool_map.ipynb notebook to produce the Affordable_food_initatives.geojson\

***The emergency food initatives (Emergency food parcel providers and Emergency meal providers)***
This has been obtained from Liverpool good food plan team. The original file is emergency_food_providers.xlsx which is processed with the Liverpool_map.ipynb notebook to produce the Emergency_food_suppliers.geojson\

***The walking distance layer***
This is created by calling the [MapboxGL isochrone API](https://docs.mapbox.com/help/tutorials/get-started-isochrone-api/) to calculate a 10 minutes walking isochrone \
These are produced by using jQuery AJAX in the map's javascript to make API  calls for respectively the coordinates of the  food support initatives (Emergency food and affordable food initatives)\
and for the supermarkets, creating two sets of isochrone layers one for the food support initatives and one for the supermarkets. In principle these calls can be made separately, stored and then imported as static layers

***The reception class obesity layer at the ward level***
This data has been obtained from Liverpool council

***The e-food deserts index layer***
This is an index measuring the degree to which areas have characteristics associated with food deserts. The index is produced by
 CDRC and was obtained from their [website](https://data.cdrc.ac.uk/dataset/e-food-desert-index#:~:text=The%20e%2Dfood%20deserts%20index,density%20of%20grocery%20retail%20facilities)

***The layers showing areas scoring in the bottom 20% and more than 10 minutes from either an emergency or an affordable food initative (This is shown by clicking the top checkbox)"
These are produced using the Further_analysis.ipynb notebook. There is a geojson for each layer above the checkbox \
The layers are income.geojson, population.geojson, education.geojson, morbidity.geojson, obesity.geojson, crowding.geojson, score.geojson.The last two being for the household overcrowding and e-food index respectively

***The layers showing the levels of Food bank and pantry usage***
These are produced in a separate analysis which is private owing to the data that it includes. The geojson that produces these at 3-4 digit postcode level is Foodbank_pantry_use.geojson

***The layer showing the connection between foodbank users and the postcodes that make use of them (This is shown by clicking the bottom checkbox***
This is created using a separate notebook as the data used to produce it is not public. This is the Foodbank_network.geojson.


***All other layer data***
This is taken from the [index of multiple deprivation](https://data-communities.opendata.arcgis.com/datasets/d4b79be994ac4820ad44e10ded313df3_0)


### The data processing that is used to generate the map layers

The processing of the food standards agency and Food banks data is done using the notebooks:\

**1. Liverpool_map.ipynb** This generates the geojson files for the layers (isochrone layer excepted) and the food outlet sites\
**2. Further_analysis.ipynb** This generates geojson for areas that are in the lowest 20% of layers data and more than 10 mins from an affordable food outlet
**3. The generation of the network layers that shows links between foodbanks and postcodes** This is done using a third notebook. It is currently  private due to this data not being public

The first two notebooks are run in sequence (Further_analysis.ipynb depends on the outputs of Liverpool_map.ipynb)  within a container using the Dockerfile in the map_data_processing folder which also contains the data in the Data folder.

They process the data and then output the files to the Out folder 

To build the container image for the data processing after cloning the repo, tagging it as map_processing
```
$ docker build --tag map_processing map_data_processing
```
To run the container on port 8009 (mapped to the container port 8009)
```
$ docker run -p 8009:8009 --init map_processing
```
To download the processed files for the map from the Out folder in the container
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
