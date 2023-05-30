# -------------------------------------------------------------------------
# Name:        Evaporation from water body
# Purpose:     This madule calculate evaporation from rivers and reserviors
#
# Author:      Elham Soleimanian
#
# Created:     2/9/2020
# -------------------------------------------------------------------------
# Import Libraries
import os
os.environ["PROJ_LIB"] = r'C:\Users\Elham Soleimanian\Anaconda3\envs\PCRASTER\Scripts'
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt 
# import matplotlib.path as mpath
import pandas as pd 
#---------------------------------------------------------------------
# Plot the earth planet 
plt.figure(figsize=(10,10))
m = Basemap(projection='ortho',lat_0=45,lon_0=-100,resolution='l')
# m = Basemap(projection='ortho',resolution='l', lat_0=50, lon_0=-100)
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents(color='coral',lake_color='aqua')
m.bluemarble(scale=0.5)
#draw lat/lon grid lines every 30 degrees.
m.drawmeridians(np.arange(0,360,30))
m.drawparallels(np.arange(-90,90,30))
#---------------------------------------------------------------------
#Plot Specific Country
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h',
            width=8E6, height=8E6, 
            lat_0=32, lon_0=53,)
m.etopo(scale=0.5, alpha=5)
#---------------------------------------------------------------------
# Import Specific city 
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='l',
            width=8E6, height=8E6, 
            lat_0=37.6, lon_0=45.2,)
m.etopo(scale=0.5, alpha=5)
#---------------------------------------------------------------------
# Map (long, lat) to (x, y) for plotting
# Import long & lat of Urmia Lake 
x, y = m(45.31,37.7)
plt.plot(x, y, 'ok', markersize=10)
plt.text(x, y, ' Urmia', fontsize=20);
#--------------------------------------------------------------------
# Ploting Data on Map 
# Import Data 
Dams = pd.read_csv('D:\My Code New\DataBank\DamsLocation.csv')
# FoodConsumer = pd.read_csv('D:\My Code New\DataBank\DamsLocation.csv')
# EnergyConsumer = pd.read_csv('D:\My Code New\DataBank\DamsLocation.csv')
#--------------------------------------------------------------------
# Extract the data we're interested in Dams
latD = Dams['latd'].values
lonD = Dams['longd'].values
Storage = Dams['storage'].values
area = Dams['area_total_km2'].values
#--------------------------------------------------------------------
# Extract the data we're interested in FoodConsumer
# latF = Dams['latd'].values
# lonF = Dams['longd'].values
# Location = Dams['location'].values
# # Extract the data we're interested in FoodConsumer
# latE = Dams['latd'].values
# lonE = Dams['longd'].values
# Location = Dams['location'].values
# ------------------------------------------------------------------
# set up the map projection, scatter the data, and then create a colorbar and legend
# 1. Draw the map background
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=47,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')
#------------------------------------------------------------------
# scatter  data, with color reflecting 
# for Dams
m.scatter(lonD, latD, latlon=True,
            c=Storage, s=area,
          cmap='Purples', alpha=25)
# for FoodConsumer 
# m.scatter(lonF, latF, latlon=True,
#           # c=np.log10(Storage), s=area,
#           cmap='Purples', alpha=25)
# # for EnergyConsumer
# m.scatter(lonE, latE, latlon=True,
#           # c=np.log10(Storage), s=area,
#           cmap='Purples', alpha=25)
# -----------------------------------------------------------------
#create colorbar and legend
#50,250 are the different storage 
plt.colorbar(label=r'${\rm Storage}$')
plt.clim(50, 250)

# make legend with dummy points
# 50,100,150 are the different area 
for a in [50, 100, 150]:
    plt.scatter([], [], c='r', alpha=1, s=a,
                label=str(a) + ' m$^2$')
plt.legend(scatterpoints=1, frameon=False,
            labelspacing=1, loc='lower left');