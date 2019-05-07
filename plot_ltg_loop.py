#import os, glob
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
#import matplotlib.cm
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature

homeDir = 'C:\\data\\lightning'
inputDir = homeDir + '\\pandasCSV\\'

def numStr(num):
    if num < 10:
        numStr = '0' + str(num)
    else:
        numStr = str(num)
    return numStr

def fixMH(MHType, MH):
    mhType = int(MHType)
    MH = int(MH)
    if (mhType == 1) & (MH > 23): 
        MH = MH - 24
    if (mhType == 2) & (MH > 12):
        MH = MH - 12
    return MH

def MHList(mhType,MHArgs):
    mhT = int(mhType)
    mhDur = int(MHArgs[0])
    mhStart = int(MHArgs[1][0])
    mhEnd = int(MHArgs[1][1])
    if (mhEnd < mhStart) & (mhT == 1):
            extEnd = mhEnd + 24
    elif (mhEnd < mhStart) & (mhT == 2):
            extEnd = mhEnd + 12
    else:
        extEnd = mhEnd
    mhRange = range(mhStart,extEnd)
    mhStartList = []
    mhEndList = []
    for i, mhs in enumerate(mhRange):
        mh0 = int(mhs)
        mh0Fix = fixMH(mhT,mh0)
        mh1 = int(mhs) + mhDur
        mh1Fix = fixMH(mhT,mh1)
        mhStartList.append(mh0Fix)
        mhEndList.append(mh1Fix)
    
    combined = zip(mhStartList,mhEndList)
    
    print (combined, mhDur)
    return combined, mhDur

def strikeSelector(yrs,mons,hrs,pol):

    # year range - have excluded 2014 due to questionable data
    yrselector = ((D.index.year >= int(yrs[0])) & (D.index.year <= int(yrs[1])) & (D.index.year != 2014))
    if (2014 >= int(yrs[0])) & (2014 <= int(yrs[1])):
        yrRange = yrs[1] - yrs[0]
    else:
        yrRange = yrs[1] - yrs[0] + 1

    # month range
    if mons[1] == mons[0]:
        hrselector = (int(mons[0]) == D.index.month)
        hrRange = 1          
    elif mons[1] >= mons[0]:
        monRange = mons[1] - mons[0] + 1
        monselector = ((int(mons[0]) <= D.index.month) & (D.index.month < int(mons[1])))       
    else:
        monRange = 12 - mons[0] + mons[1] + 1
        monselector = ((int(mons[0]) <= D.index.month) | (D.index.month <= int(mons[1])))
        
    # hour range
    if hrs[1] == hrs[0]:
        hrselector = (int(hrs[0]) == D.index.hour)
        hrRange = 1
    elif hrs[1] > hrs[0]:
        hrRange = hrs[1] - hrs[0] + 1
        hrselector = ((D.index.hour >= int(hrs[0])) & (D.index.hour < int(hrs[1])))
    else:
        hrselector = ((D.index.hour >= int(hrs[0])) | (D.index.hour < int(hrs[1])))
        hrRange = 24 - hrs[0] + hrs[1] + 1

    # polarity
    if polarity == "P":
        polselector = ((D['POL'] >= 0.0))
        polStr = "Positive strikes only\n"
    elif polarity == "N":
        polselector = ((D['POL'] <= 0.0))
        polStr = "Negative strikes only\n"
    else:
        polselector = (D['POL'] >= -10.0)
        polStr = "Positive and negative strikes\n"

    factor = yrRange * monRange * hrRange
    fullselector = (yrselector & hrselector & monselector & polselector)
    return fullselector, polStr, yrRange, factor


def ltgHisto(E,gridsize):
    ltg_lons = np.array(E['LON'])
    ltg_lats = np.array(E['LAT'])
    lons = np.arange(gridW, gridE, gridsize)
    lats = np.arange(gridS, gridN, gridsize)
    X, Y = np.meshgrid(lons, lats)
    H, lons, lats = np.histogram2d(ltg_lons, ltg_lats, bins=(lons, lats))
    H = H.T
    return H, X, Y

def setMap(X, Y):
    m = Basemap(resolution='h', # c, l, i, h, f or None
            projection='merc',
            llcrnrlon=gridWmap, llcrnrlat= gridSmap, urcrnrlon=gridEmap, urcrnrlat=gridNmap, area_thresh=400)
            #llcrnrlon=-90.8, llcrnrlat= 44.8, urcrnrlon=-83.40, urcrnrlat=47.6, area_thresh=400, ax=ax)
    m.drawmapboundary()
    m.drawcounties(linewidth=0.2)
    xs, ys = m(X, Y)
    return xs, ys


# -----------------------------------------------------
monDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
hr = range(0,24)
hrDict = {0:' 8 PM', 1:' 9 PM', 2:'10 PM', 3:'11 PM', 4:' Mid ', 5:' 1 AM', \
          6:' 2 AM', 7:' 3 AM', 8:' 4 AM', 9:' 5 AM', 10:' 6 AM', 11:' 7 AM', 12:' 8 AM', \
          13:' 9 AM', 14:'10 AM', 15:'11 AM', 16:' Noon', 17:' 1 PM', 18:' 2 PM', \
          19:' 3 PM', 20:' 4 PM', 21:' 5 PM', 22:' 6 PM', 23:' 7 PM'}
DF = None
DF = pd.read_pickle('C:\\data\\lightning\\LPandUP.pkl')

gridBounds = [-87.0, -83.0, 41.5, 44.5]
gridW, gridE, gridS, gridN = gridBounds

mapBounds = [gridW - 0.1, gridE + 0.1, gridS - 0.1, gridN + 0.1]
gridWmap, gridEmap, gridSmap, gridNmap = mapBounds

AreaSelector = ((DF.LAT >= gridSmap) & (DF.LAT <= gridNmap) & (DF.LON >= gridWmap) & (DF.LON <= gridEmap))
D = DF[AreaSelector]


cdict = {'red':  ( (0.0,  1.0,  1.0),  # white (1,1,1)
                   (0.05,  0.9,  0.9) , # gray (0,1,0)
                   (0.3,  0.0,  0.0) ,  # green (0,1,0)
                   (0.4,  1.0,  1.0) ,  # yellow (1,1,0)
                   (0.5,  1.0,  1.0) ,  # orange (1,0.5,0)              
                   (0.7,  1.0,  1.0) ,  # red (1,0,0)  
                   (1.0,  1.0,  1.0) ), # magenta (1,0,1)
         'green':( (0.0,  1.0,  1.0),
                   (0.05,  0.9,  0.9) , # gray (0,1,0)
                   (0.3,  1.0,  1.0) ,  # green (0,1,0)
                   (0.4,  1.0,  1.0) ,  # yellow (1,1,0)
                   (0.5,  0.5,  0.5) ,  # orange (1,0.5,0) 
                   (0.7,  0.0,  0.0) ,  # red (1,0,0) 
                   (1.0,  0.0, 0.0) ),  # magenta (1,0,1)
         'blue': ( (0.0,  1.0,  1.0),
                   (0.05,  0.9,  0.9) , # gray (0,1,0)
                   (0.3,  0.0,  0.0) ,  # green (0,1,0)
                   (0.4,  0.0,  0.0) ,  # yellow (1,1,0)
                   (0.5,  0.0,  0.0) ,  # orange (1,0.5,0) 
                   (0.7,  0.0,  0.0) ,  # red (1,0,0) 
                   (1.0,  1.0, 1.0) ) } # magenta (1,0,1)
custom_map = LinearSegmentedColormap('custom_map', cdict)
plt.register_cmap(cmap=custom_map)

hrArgs = [4,[16,20]]
monArgs =[2,[3,5]]
hour, hrDur = MHList(1,hrArgs);
month, monDur = MHList(2,monArgs);
yrs = [1990,2017]
polarity = "both" # N, P, or both

for i,hr in enumerate(hour):
    for j,mon in enumerate(month):
        fig = plt.figure(figsize=(7, 10))
        ax = plt.subplot(1,1,1)
    
        figName = 'Density_' + numStr(mon[0])  + '-'  + numStr(mon[1]) + '_' + numStr(hr[0]) + '-' + numStr(hr[1]) +'.png'
        hrStr = hrDict[hr[0]] + " to " + hrDict[hr[1]]
        UTCStr = numStr(hr[0]) + " to " + numStr(hr[1])
        monStr = monDict[mon[0]] + " to " + monDict[mon[1]]
        fullStr = hrStr + "\n" + monStr
        print fullStr
        
        t = ax.text(0.65, 0.9, fullStr, fontsize=16, horizontalalignment='right', transform=ax.transAxes )
        t.set_bbox(dict(facecolor='white', alpha=1.0, edgecolor='black'))
        fullselector, polStr, yrRange, factor = strikeSelector(yrs,mon,hr,polarity);
        E= D[fullselector]
        H, X, Y= ltgHisto(E,0.01)
        H = (H / factor)
        xs, ys = setMap(X, Y);
        c = plt.pcolormesh(xs, ys, H, vmin=0.0, vmax=0.1, cmap=custom_map)
        xs, ys = setMap(X, Y);

        plt.savefig('C:/data/lightning/images/' + figName)
        plt.close(fig)




#Original Domain
#northLat = 49.0 # UP - 47.5
#southLat = 41.0 # UP - 44.9
#westLon = -90.75 # UP - -90.75
#eastLon = -81.75 # UP - -84.8
        
#fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(7, 10))

#numCols = int(len(hrs)/2)
#for i, ax in enumerate(axes.flat):







