# Stargazing Suggestion App
Mehika Patel

## Abstract
The goal of this project was to use an automated data pipeline to create an application that is able to provide suggestions about time and locations to go stargazing to the user. The data was sourced from several sources, including moon phases data, google maps data, and weather data. I worked with streamlit to create an [application](https://share.streamlit.io/mehiks11/stargazing/appstuff/starapp.py). There will also be a more interactive map with light pollution data posted to go along with the location suggestions (posisbly with location suggestions integrated inside of the map) soon. 

## Application Basic Version: (more features to be integrated soon)
https://user-images.githubusercontent.com/77343298/123438060-5276d280-d59e-11eb-82d5-ce47f7e67cfe.mov



## Design
This project pulls several custom functions to pull and optimize the suggestion results, and display them to the user in a friendly fashion. The weather data is pulled using weatherbit's API, with moon phase data uploaded to kaggle [here](https://www.kaggle.com/mehiks/moon-phases). The project aims to use clear hierarchal function building to craft a easily moldable project, that can and will be built upon for better user interactivity in the future. 

## Notebook layout:
[This notebook](https://github.com/mehiks11/StarGazing/blob/master/appstuff/suggest.py) holds code for all the functions used by the main stargazing application. 
[This notebook](https://github.com/mehiks11/StarGazing/blob/master/appstuff/suggestplanning.ipynb) holds code for planning out the individual functions used by the app.
[This notebook](https://github.com/mehiks11/StarGazing/blob/master/appstuff/starapp.py) holds the code for the actual streamlit app.


## Data
The data pulled was mostly from weatherbit API, from a moonphase dataset I personally created, and location data pulled from a light pollution map, along with google search results.

## Algorithms
**Suggestion Building**
The biggest algorithm used here was the simple function created to rate and weight attributes of certain conditions in a location and time to suggest when and where to stargaze. The conditions are weighted according to how relatively important they are to the stargazing experience. For example, during a night with high cloud coverage, stargazing is less optimal than on a clearer, warmer night. 

## Tools
- Geopandas for mapping light pollution data
- Pandas & Numpy for data manipulation
- Beautifulsoup for location pulling
- Rasterio for working with tiff files for light pollution data
- streamlit for app production


## Communication
In addition to the slides presented, there is a streamlit [app](https://share.streamlit.io/mehiks11/stargazing/appstuff/starapp.py).
