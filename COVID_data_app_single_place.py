# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 19:50:17 2020

@author: benho
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
filepath = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(filepath)
filepath_us = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
df_us = pd.read_csv(filepath_us)

#%%
N = len(df.columns) - 4
days = [i for i in range(1,N+1)]

#%%
# This is for countries that occupy multiple rows
def get_country(country): # enter country like 'Morocco'
    bosh = df.loc[df['Country/Region'] == country]
    bosh = bosh.T
    bosh.loc[:,'Total'] = bosh.sum(axis=1)
    bosh = bosh.Total[4:]
    bosh = pd.DataFrame(bosh)
    bosh['Total'] = pd.to_numeric(bosh['Total'])
    bosh.columns = [country]
    return bosh
#%% test case
#canada = get_big_country('Canada')
#%%
# This is for U.S. states
def get_state(state): # enter state like 'Maryland'
    bosh = df_us.loc[df_us['Province_State'] == state]
    bosh = bosh.T
    bosh.loc[:,'Total'] = bosh.sum(axis=1)
    bosh = bosh.Total[11:]
    bosh = pd.DataFrame(bosh)
    bosh['Total'] = pd.to_numeric(bosh['Total'])
    bosh.columns = [state]
    return bosh
#%% test case
#oregon = get_state('Oregon')
#%%
# This is where I actually run the program
place = input("Type name of place: ")
def get_place(place):
    placetype = input("Type 1 for country, 2 for U.S. state.")
    if placetype == "1":
        country = get_country(place)
        return(country)
    elif placetype == "2":
        state = get_state(place)
        return(state)
    else:
        exit()
#%%
# 
covid_df = get_place(place)
#%%
plt.scatter(days,covid_df,s=10) # s=10 uses small markers
plt.legend([place])
plt.xlabel('# days since Jan 22')
plt.ylabel('total # of cases')
plt.grid()
#plt.savefig("5-places.png",dpi=(300), bbox_inches='tight')
plt.show

#%%
# I need this for the next part b/c of divide by zero
def weird_division(n, d):
    return n / d if d else 0

#%%
# function to add column of Ep to each location df
def add_ep(place):
    stuff = []
    for i in range(len(place)-1):
        ratio = weird_division(place.iloc[i+1,0],place.iloc[i,0])
        stuff.append(ratio)
    stuff[:0] = [0] # need to add zero at begiining to make same length
    place['Ep'] = stuff
    return(place)
#%%
# get new cases
def new_cases(place):
    stuff = []
    for i in range(len(place)-1):
        newcases = place.iloc[i+1,0]-place.iloc[i,0]
        stuff.append(newcases)
    stuff[:0]=[0]
    place['New_cases'] = stuff
    return place
#%%
# add the Ep and newcases columns to existing df and create index
covid_df = add_ep(covid_df)
covid_df = new_cases(covid_df)
covid_df = covid_df.reset_index()

#%%
export = covid_df.to_csv("COVID_data_%s.csv" %place)
#%%
