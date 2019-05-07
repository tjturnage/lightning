import os, tarfile, re

homeDir = 'C:/data/lightning'
decompDir = homeDir + '/decompressed/'
flagDecomp = "yes"

northLat = 47.72
southLat = 41.4
westLon = -91.0
eastLon = -81.75

"""
44.2,-87.45
44.2, -86.6
42.3
"""
UP = (-90.54, -82.3, +45.842, +47.72)
LP = (-86.88, -82.3, +41.4, +45.842)

southLower = 41.4
latBreak = 45.842
northUpper = 47.72
westLower = -86.88
westUpper = -91.0
eastLon = -81.75


for y in range(2006,2008):
#for y in range(2000,2001):
  
    yr = str(y)

    #-------------------------
    if flagDecomp == "yes":
    	 # Obtain list of compressed files
        files = os.listdir(homeDir+'\\raw')
        files = [f for f in files if (re.search('tar.gz',f) and re.search(str(y),f))]
    
    
     	  #For each compressed file with monthly data...
        for f in files:
     
             # Decompress the monthly file...
             print "Decompressing: " + str(f)
             tfile = tarfile.open(homeDir+'\\raw\\'+f, 'r:gz')
             tfile.extractall(homeDir+'\\decompressed')
    #-------------------------

    files2 = []
    os.chdir(decompDir)
    files2 = os.listdir(homeDir+'\\decompressed')
 

        #files = [f for f in files if (re.search('9603.*txt',f) and re.search(str(y),f))]
    files2 = [g for g in files2 if (re.search('VAISALA.*txt',g) and re.search(str(y),g))]
    
    with open(homeDir + '\\processed\\' + str(y) + ".txt", "wb") as outfile:
            for g in files2:
                print "working on: " + str(g)
                with open(g, "rb") as infile:
                    data = infile.readlines()
                    for line in data:
                        splitLine = line.strip().split(' ')
                        lat = float(splitLine[6])
                        lon = float(splitLine[7])
                        pol = str(splitLine[9])
                        if pol == "N":
                            polInt = -1
                        else:
                            polInt = 1
                        if (((lat > southLower) and (lat < latBreak) and (lon > -87.45) and (lon < eastLon)) or \
                        ((lat >= latBreak) and (lat < northUpper) and (lon > westUpper) and (lon < eastLon))):
                        #if (((lat > southLat) and (lat < latBreak) and (lon > westLower) and (lon < eastLon)) or \
                        #((lat >= latBreak) and (lat < southLat) and (lon > westUpper) and (lon < eastLon))):
                            first = " ".join(splitLine[0:8])
                            finalLine = str(first) + " " + str(polInt) + "\n"
                            print finalLine
                            outfile.write(finalLine)
