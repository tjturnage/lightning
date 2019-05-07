# -*- coding: utf-8 -*-
"""
Created on Mon May 28 10:35:29 2018

@author: Owner
"""

import numpy as np
import pandas as pd
import datetime, os, re

# Data obtained from ftp://ftp-restricted.ncdc.noaa.gov/data/lightning/
homeDir = 'C:\data\lightning'

D = []

# Go year-by-year



# Obtain list of decompressed files
files = os.listdir(homeDir+'\\processed')
#files = [f for f in files if (re.search('VAISALA.*txt',f) and re.search(str(y),f))]
#files = [f for f in files if (re.search('*txt',f) and re.search(str(y),f))]
#files = [f for f in files if (re.search('*txt',f)]
# Create the initial dataframe with the first file...
d = np.loadtxt(homeDir+'\\processed\\'+files[0])

# Create a list of datetime objects for the strikes and lat/lon data
dts = np.array([datetime.datetime(int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5])) for x in d[:,0:6]])
lat, lon, pol = d[:,-3], d[:,-2], d[:,-1]

# Create a bounding box
ix = np.where((lat>41)&(lat<48)&(lon<-81.5)&(lon>-91.1))[0]

# Generate a DataFrame
D = pd.DataFrame({'LAT':lat[ix], 'LON':lon[ix], 'POL':pol[ix]}, index=dts[ix])
print ('Initialized'),files[0]

# Move through the remaining files and append
for f in files[1:]:
    print ('Appending',f)
    # Load data    
    d = np.loadtxt(homeDir+'\\processed\\'+f)
    
    # Create a list of datetime objects for the strikes and lat/lon data
    dts = np.array([datetime.datetime(int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5])) for x in d[:,0:6]])
    lat, lon, pol = d[:,-3], d[:,-2], d[:,-1]
 
    #northLat = 47.72
    #southLat = 41.4
    #westLon = -91.0
    #eastLon = -81.75       
    # Create a bounding box
    ix = np.where((lat>41)&(lat<48)&(lon<-81.5)&(lon>-91.1))[0]
    
    # Generate a DataFrame
    d = pd.DataFrame({'LAT':lat[ix], 'LON':lon[ix], 'POL':pol[ix]}, index=dts[ix])
    
    # Append
    D = D.append(d)
    print ('Appended',f)
    
# Save the output
D.to_pickle(homeDir+'\\decompressed\\final.pck')
#print 'Pickled',f