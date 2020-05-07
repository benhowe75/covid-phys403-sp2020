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
import time
datestr = time.strftime("%Y%m%d")
print(datestr)

#%%
# This is for countries that occupy multiple rows
def get_country(placename):
    place = df.loc[df['Country/Region'] == placename]
    place = place.iloc[:,4:]
    place.loc[placename,:] = place.sum(axis = 0)
    placed = place.iloc[-1,:]
    return(placed)

#%%
# This is for U.S. states
def get_state(placename):
    place = df_us[df_us['Province_State'] == placename]
    place = place.iloc[:,11:]
    place.loc[placename,:] = place.sum(axis = 0)
    placed = place.iloc[-1,:]
    return(placed)

#%%
# This is where I actually run the program
belgium = get_country('Belgium')
brazil = get_country('Brazil')
canada = get_country('Canada')
texas = get_state('Texas')
conn = get_state('Connecticut')
mass = get_state('Massachusetts')
ny = get_state('New York')
america = get_country('US')

#%%
# I need this for the next part b/c of divide by zero
def weird_division(n, d):
    return n / d if d else 0
#%%
def get_eps(placed):
    ep = np.zeros(len(placed))
    for i in range(len(placed)-1):
        ep[i+1] = weird_division(placed.iloc[i+1],placed.iloc[i])
        #eps = pd.Series(ep)
    #print(eps)
    return(ep)
    
#%%
def get_new_cases(placed):
    new = np.zeros(len(placed))
    for i in range(len(placed)-1):
        new[i+1] = placed.iloc[i+1] - placed.iloc[i]
        #news = pd.Series(new)
    #print(news)
    return(new)
  
#%%
plt.scatter(days,belgium,s=10)
plt.scatter(days,brazil,s=10)
plt.scatter(days,canada,s=10)
#plt.scatter(days,america,s=10)
plt.scatter(days,conn,s=10)
plt.scatter(days,mass,s=10)
#plt.scatter(days,ny,s=10)
#plt.scatter(days,texas,s=10)
plt.legend(['Belgium','Brazil','Canada','Connecticut','Massachusetts','New York'])
plt.xlabel('# days since Jan 22')
plt.ylabel('total # of cases')
plt.grid()
plt.savefig("places_%s.png" %datestr,dpi=(300), bbox_inches='tight')
plt.show

#%%
def add_columns(series):
    stuff = pd.Series.to_frame(series)
    stuff.loc[:,'Eps'] = get_eps(series)
    stuff.loc[:,'New'] = get_new_cases(series)
    return(stuff)
#%%
a = add_columns(belgium)
b = add_columns(brazil)
c = add_columns(canada)
d = add_columns(america)
e = add_columns(conn)
f = add_columns(mass)
g = add_columns(ny)
h = add_columns(texas)

#%%
covid_df = pd.concat([a,b,c,d,e,f,g,h], axis = 1)
#%%
export = covid_df.to_csv("COVID_data_%s.csv" %datestr)