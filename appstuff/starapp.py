#import necessary modules and functions
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from suggest import *
from weatherbit.api import Api
from datetime import date,datetime, timedelta

#set ups
    #weather set up
api_key = "a33d21f85ef140449e22bf1475de3f1c"
api = Api(api_key)
api.set_granularity('daily')


##### App Display
cover_img = Image.open('cover_img.jpg')
# st.title("Starry Nights")


#App UI
st.image(cover_img,width=700)
st.subheader("About This App:")
st.write("Hello world. I am an app that suggests days to go stargazing according to weather conditions, moon phases, and more! I will also show you some local places you can go to stargaze.")



st.write("**Enter your location and the number of days within which you'd like to go stargazing!**")
city = st.text_input("City:", '')
state = st.selectbox('State',('AL',
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
        'SC',
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

col1, col2, col3 = st.beta_columns([2,1,1])
with col1:
    num_days = st.text_input("I want to go stargazing within the next _ days:", '14')
with col1:
    num_show = st.text_input("Show me the top _ days to go stargazing:", '2')

if type(city)!=str:
    st.write("Sorry. Please enter a valid city name!")
elif type(num_days)!=int or type(num_show)!=int:
    st.write("Sorry. Please enter a valid number of days!")
elif num_show>num_days:
    st.write("Sorry. The number of days you want us to show you has to be less than or equal to the number of days you want to go in!")
elif num_show>num_days:
    st.write("Sorry. The number of days you want us to show you has to be less than or equal to the number of days you want to go in!")
elif num_days>14 or num_show>14:
    st.write("Sorry. Please enter 14 or fewer days.")

day_dict = give_suggestions(city,state,num_days,num_show)

