'''
This module holds all the functions built to pull date suggestions for stargazing.
'''

# necessary imports:
import pandas as pd
from weatherbit.api import Api
from datetime import date,datetime, timedelta
import requests

#set ups
    #weather set up
api_key = "a33d21f85ef140449e22bf1475de3f1c"
api = Api(api_key)
api.set_granularity('daily')
    #moon set up
moon_phases = pd.read_csv('https://raw.githubusercontent.com/mehiks11/StarGazing/master/data/moon_phases.csv').drop(columns=['Unnamed: 3','Unnamed: 4'])
moon_phases.Year = moon_phases.Year.astype(str)

moon_phases['Date'] = pd.to_datetime(moon_phases['Date'] + ' '+ (moon_phases['Year']))
moon_phases.drop(columns='Year',inplace=True)
moons = ['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']

# Weather Pulling Functions
def weather_report(city,state,num_days=14):
    '''
    This function returns a dataframe of weather conditions for a given number of days 
    '''
    loc = city + ',' + state
    forecast = api.get_forecast(city = loc)

    weather = pd.DataFrame(forecast.get_series(['temp','precip','rh','clouds'])).head(num_days)
    
    weather['temp'] = weather['temp'] * (9/5) + 32 #celcius to farenheit
    weather['precip_rank'] = weather.precip.rank().astype(int) #ratings for precipitation
    weather['rh_rank'] = weather.rh.rank().astype(int)/2 #ratings for precipitation
    weather['cloud_rank'] = weather.clouds.rank().astype(int)*100 #ratings for precipitation
    
    
    temp_ranks = []
    for temp in weather.temp:
        if temp<40:
            temp_ranks.append(10)
        if temp>40 and temp<50:
            temp_ranks.append(5)
        if temp>50 and temp<65:
            temp_ranks.append(3)
        if temp>65 and temp<70:
            temp_ranks.append(2)
        if temp>70:
            temp_ranks.append(1)

    weather['temp_ranks']= pd.Series(temp_ranks)
    weather['bad_rate'] = weather['temp_ranks'] + weather['precip'] + weather['precip_rank'] + weather['rh_rank']
    return weather.head(num_days)

#Moon Phase Functions
def before_after_moon(current):
    '''
    This function returns the moon phase before, and moon phase after a given current moon phase.
    '''
    if current == 'New Moon':
        before = moons[3]
        after = moons[1]
    if current == 'First Quarter':
        before = moons[0]
        after = moons[2]
    if current == 'Full Moon':
        before = moons[1]
        after = moons[3]
    if current == 'Last Quarter':
        before = moons[2]
        after = moons[0]
    return before, after

def get_moon_phases(num_days=14):
    '''
    This function returns a dataframe or moon_phases in a given number of days following today.
    '''
    today = date.today()
    dates = []

    for i in range(num_days):
        add = today + timedelta(days=i)
        dates.append(pd.to_datetime(add))

    #list start and end dates to make mask
    start_date= dates[0]
    end_date= dates[-1]

    #mask for between our dates!
    mask = (moon_phases['Date'] >= start_date) & (moon_phases['Date'] <= end_date)
    df = moon_phases.loc[mask].sort_values('Date')
    moons = ['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']

    #figure out what the first phase is for the time period
    first_phase, next_phase =before_after_moon(df.iloc[0].Phase)

    #make a list of the phases during each of the 14 days (today+following 14 days)
    phases= []
    counter = pd.to_datetime(date.today())
    x=0
    df_len = len(df.Date)

    while ((counter != df.iloc[0].Date) & (x < num_days)):
        phases.append(first_phase)
        counter = counter + timedelta(days=1)
        x+=1
        
    ran = num_days +1 -len(phases)
        
    if df_len == 1:
        for i in range(ran):
            phases.append(df.iloc[0].Phase)
            counter = counter + timedelta(days=1)
            x+=1

    if df_len>1:
        while ((counter != df.iloc[1].Date) & (x < num_days)):
            phases.append(df.iloc[0].Phase)
            counter = counter + timedelta(days=1)
            x+=1
    ran = num_days +1 -len(phases)
          
    if df_len == 2:
        for i in range(ran):
            phases.append(df.iloc[1].Phase)
            counter = counter + timedelta(days=1)
            x+=1
            
    if df_len >2:
        while ((counter != df.iloc[2].Date) & (x < num_days)):
            phases.append(df.iloc[1].Phase)
            counter = counter + timedelta(days=1)
            x+=1

    if x > num_days:
        final = pd.DataFrame(list(zip(dates, phases)),
                   columns =['Date', 'Phase'])

    ran = num_days + 1 - len(phases)

    if df_len >=3:
        for i in range(ran):
            phases.append(df.iloc[2].Phase)

    final = pd.DataFrame(list(zip(dates, phases)),
                   columns =['Date', 'Phase'])

    #add moon reverse ratings
    moons =[]
    for phase in final.Phase:
        if phase == 'First Quarter':
            moons.append(5)
        if phase == 'Full Moon':
            moons.append(10)
        if phase == 'Last Quarter':
            moons.append(5)
        if phase == 'New Moon':
            moons.append(0)
    final['moon'] = pd.Series(moons)
    
    return final


#Creating final conditions dataframe functions
def condition_df(city = 'greenville',state = 'sc', num_days=14):
    '''
    This function returns a dataframe with conditions (weather and moon phase) for stargazing.
    '''
    moon = get_moon_phases(num_days)
    weather = weather_report(city,state,num_days)
    df = pd.concat([moon, weather], axis=1).drop(columns = 'datetime')
    df['bad_rate'] = df['bad_rate']+df['moon']
    df['rank'] = df.bad_rate.rank()
    
    ranks_list = list(df['rank'])
    rh_list =list(df['rh'])
    
    for i in range(len(ranks_list)):
        if ranks_list[i] == ranks_list[i-1]:
            if rh_list[i]>rh_list[i+1]:
                ranks_list[i]=ranks_list[i] + 1 
            else:
                ranks_list[i+1]=ranks_list[i+1] + 1 
           
    df['rank'] = ranks_list    
    df['rank'] = df['rank'].astype(int)
    return df


#Final Suggestion function
def give_suggestions(city='greenville',state='sc',num_days=10,num_show=1):
    '''
    This function takes city,state, and num_days. It returns a dictionary of ranked days to go stargazing. 
    '''
    df = condition_df(city,state,num_days).sort_values(by='rank')
    
    #make a list of labels 
    ranking_days =list(range(1,num_days))
    #initialize a dictionary to store ranked dates
    ranks ={}
    conditions={}

    #add dates to dictionary with label
    for i in range(num_show1):
        ranks[ranking_days[i]] = str(list(df.Date)[i]).split()[0]
        
    return ranks

#location google search
def pull_locs(city,state):
    city= city.replace(' ','+')
    state= state.replace(' ','+')
    url = 'https://www.google.com/maps/search/'+city+'+'+state+'+'+'parks'
    return url