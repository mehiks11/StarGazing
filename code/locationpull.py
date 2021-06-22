'''
This is one of 5 custom functions created to run this application.

It focuses on pulling location options for stargazing. It pulls relevant nearby parks by webscraping google search and pulls their hours and address.

'''

from bs4 import BeautifulSoup
import requests

def pull_locs(city,state):
    '''
    This function simply returns a link to a google page with information on locations to go to stargaze.
    '''
    city= city.replace(' ','+')
    state= state.replace(' ','+')
    url = 'https://www.google.com/maps/search/'+city+'+'+state+'+'+'parks'
    return url

'''
This code will eventually be able to pull information directly from google search. However, for now, the function will return a google link to locations nearby.
'''
