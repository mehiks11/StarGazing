#import necessary modules and functions
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from suggest import *
from weatherbit.api import Api
from datetime import date,datetime, timedelta
import requests

##app format setups:

first = 'First Best Day:'
second = 'Second Best Day:'
third = 'Third Best Day:'
fourth = 'Fourth Best Day:'
fifth = 'Fifth Best Day:'
sixth = 'Sixth Best Day:'
seventh = 'Seventh Best Day:'
eigth = 'Eigth Best Day:'
ninth = 'Ninth Best Day:'
tenth = 'Tenth Best Day:'
eleventh = 'Eleventh Best Day:'
twelth = 'Twelth Best Day:'
thirteenth = 'Thirteenth Best Day:'
fourteenth = 'Fourteenth Best Day:'

day_labels = [first,second,third,fourth,fifth,sixth,seventh,eigth,ninth,tenth,eleventh,twelth,thirteenth,fourteenth]




#set ups
    #weather set up
api_key = "a33d21f85ef140449e22bf1475de3f1c"
api = Api(api_key)
api.set_granularity('daily')


##### App Display
url = 'https://github.com/mehiks11/StarGazing/blob/master/appstuff/cover_img.jpg?raw=true'
cover_img = Image.open(requests.get(url,stream=True).raw)
# st.title("Starry Nights")

#App UI
st.image(cover_img,width=700)
st.subheader("About This App:")
st.write("Hello world. I am an app that suggests days to go stargazing according to weather conditions, moon phases, and more! I will also show you some local places you can go to stargaze.")


with st.form(key='my_form'):
    st.write("**Enter your location and the number of days within which you'd like to go stargazing!**")
    city1 = st.text_input("City:", '')
    state1 = st.selectbox('State',('SC',
            'AL',
            'AK',
            'AS',
            'AZ',
            'AR',
            'CA',
            'CO',
            'CT',
            'DE',
            'DC',
            'FL',
            'GA',
            'HI',
            'ID',
            'IL',
            'IN',
            'IA',
            'KS',
            'KY',
            'LA',
            'ME',
            'MD',
            'MA',
            'MI',
            'MN',
            'MS',
            'MO',
            'MT',
            'NE',
            'NV',
            'NH',
            'NJ',
            'NM',
            'NY',
            'NC',
            'ND',
            'OH',
            'OK',
            'OR',
            'PA',
            'PR',
            'RI',
            'SD',
            'TN',
            'TX',
            'UT',
            'VT',
            'VA',
            'WA',
            'WV',
            'WI',
            'WY'))
    num_days1 = st.number_input("I want to go stargazing within the next _ days:", min_value=2,max_value=14)
    num_show1 = st.number_input("Show me the top _ days to go stargazing:", min_value=2,max_value=14)
    submit_button = st.form_submit_button(label='Let\'s Stargaze!')

if submit_button:
    # for x in range(num_show1):
    #     st.write(f'**{day_labels[x]** {suggestions[x+1]}')

    if type(city1)!=str:
        st.write("Sorry. Please enter a valid city name!")
    elif num_show1>num_days1:
        st.write("Sorry. The number of days you want us to show you has to be less than or equal to the number of days you want to go in!")
    elif num_show1+2==num_days1:
        st.write("Sorry. Please choose at least 2 days more than what you'd like to show. ")
    else:
        suggestions = give_suggestions(city=city1,state=state1,num_days=num_days1,num_show=num_show1)
        for x in range(num_show1):
            st.write(f'**{day_labels[x]}** {suggestions[x+1]}')


if submit_button:
    url = pull_locs(city1,state1)
    st.write('Click here for places open near you to go!')
    st.write(url)



