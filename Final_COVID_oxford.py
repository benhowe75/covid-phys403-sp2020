# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 19:50:17 2020

@author: benho
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
df = pd.read_csv("https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv")

#%%
import time
datestr = time.strftime("%Y%m%d")
print(datestr)
#%%
def get_oxford(country):
    stuff = df.loc[df['CountryName'] == country]
    stuff = stuff.iloc[:,[0,30,32]]
    return(stuff)

#%%
belgium = get_oxford('Belgium')
#brazil = get_oxford('Brazil')
canada = get_oxford('Canada')
mexico = get_oxford('Mexico')
usa = get_oxford('United States')


#%%
# I need this for the next part b/c of divide by zero
def weird_division(n, d):
    return n / d if d else 0

#%%
def add_egf(place):
    stuff = []
    for i in range(len(place)-1):
        ratio = weird_division(place.iloc[i+1,2],place.iloc[i,2])
        stuff.append(ratio)
    stuff[:0] = [0] # need to add zero at begiining to make same length
    place['egf'] = stuff
    return(place)

#%%
belgium = add_egf(belgium)
belgium = belgium.reset_index(drop=True)
canada = add_egf(canada)
canada = canada.reset_index(drop=True)
mexico = add_egf(mexico)
mexico = mexico.reset_index(drop=True)
usa = add_egf(usa)
usa = usa.reset_index(drop=True)

#%%
days = [i for i in range(df['Date'].nunique())]

plt.figure()

plt.plot(days,belgium.iloc[:,3])
#plt.plot(days,brazil.iloc[:,3])
plt.plot(days,canada.iloc[:,3])
plt.plot(days,mexico.iloc[:,3])
plt.plot(days,usa.iloc[:,3])

plt.show()

#%%
# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.plot(days,belgium.egf, color="red", marker="o")
# set x-axis label
ax.set_xlabel("days",fontsize=14)
# set y-axis label
ax.set_ylabel("Confirmed Cases",color="red",fontsize=14)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(days, belgium.StringencyIndex,color="blue",marker="o")
ax2.set_ylabel("Stringency Index",color="blue",fontsize=14)
plt.show()
# save the plot as a file
#fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
#            format='jpeg',
#            dpi=100,
#            bbox_inches='tight')
#%%
combined = pd.concat([belgium,canada,mexico,usa],axis=1)
#combined.to_csv("stringency_%s.csv" %datestr)
