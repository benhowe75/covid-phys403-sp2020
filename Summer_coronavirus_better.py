# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:04:02 2020

@author: benho
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

#%%
# get all the user input at once
def get_string():
    place = input("Enter name of location: ")
    location = input("Type '1' for a country or '2' for a U.S. state.  ")
    stat = input("Type '1' for confirmed cases or '2' for deaths.  ")
    double = [int(stat),int(location),place]
    return(double)

#%%
start = get_string() # run the function above
                    # note that the order of inputs is switched

#%%
# create a timestamp to append to exported files and images
import time
datestr = time.strftime("%Y%m%d")

#%%
# using the two inputs pick which of the four databases we will use
def get_path(double):
    x = double[0]
    y = double[1]
    if x == 1 and y == 1:
        filepath = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        return(filepath)
    elif x == 1 and y == 2:
        filepath = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
        return(filepath)
    elif x == 2 and y == 1:
        filepath = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        return(filepath)
    elif x == 2 and y == 2:
        filepath = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
        return(filepath)
    else:
        print("Fubar")
#%%
my_path = get_path(start)
my_df = pd.read_csv(my_path)

#%%
# these loops are needed b/c databases have different # of 
# leading columns to get rid of
place = start[2]
def get_data(stuff):
    if stuff[1] == 1: # for countries only 4 columns are removed
        junk = my_df.loc[my_df['Country/Region'] == place]
        junk = junk.iloc[:,4:]
    elif stuff[1] == 2: # for states it's either 11 or 12 columns
        junk = my_df.loc[my_df['Province_State'] == place]
        if start[0] == 1:
            junk = junk.iloc[:,11:]
        elif start[0] == 2:
            junk = junk.iloc[:,12:]
        else:
            exit()
    else:
        exit()
    junk.loc[place,:] = junk.sum(axis = 0) #this aggregates multiple rows into one sum row
    junked = junk.iloc[-1,:] # drop all except the sums
    return(junked)

#%%
# this is where I actually retrieve the data
my_data = get_data(start)

#%%
# a lot of code just to get a plot label, but I can't find a quicker way
def make_labels(stuff):
    if stuff[0] == 1:
        label = "Confirmed cases"
        return(label)
    elif stuff[0] == 2:
        label = "Deaths"
        return(label)
    else:
        label = ""

#%%
N = len(my_data)
days = [i for i in range(1,N+1)] # create x values for plot
label = make_labels(start) # generate plot title

#%%
plt.title("Coronavirus %s" %label)
plt.scatter(days,my_data,s=10)
plt.legend(['%s' %place])
plt.xlabel('# days since Jan 22')
plt.ylabel('# of cases')
plt.grid()
plt.savefig("%s_plot_%s.png" %(place,datestr),dpi=(300), bbox_inches='tight')
plt.show

#%%
def get_new_cases(series):
    new = np.zeros(len(series))
    for i in range(len(series)-1):
        new[i+1] = series.iloc[i+1] - series.iloc[i]
    return(new)
#%%
# I need this for the next part b/c of divide by zero
def weird_division(n, d):
    return n / d if d else 0
#%%
def get_rate(series):
    ep = np.zeros(len(series))
    for i in range(len(series)-1):
        ep[i+1] = weird_division(series.iloc[i+1],series.iloc[i])
    return(ep)
#%%
def add_columns(series):
    stuff = pd.Series.to_frame(series)
    stuff.loc[:,'Rate'] = get_rate(series)
    stuff.loc[:,'New'] = get_new_cases(series)
    return(stuff)
#%%
data_out = add_columns(my_data)
export = data_out.to_csv("%s_data_%s.csv" %(place, datestr))