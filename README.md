# lightning
Plot NLDN lightning strike data

Workflow:
    Obtain tarfiles from ftp://ftp-restricted.ncdc.noaa.gov/data/lightning/
    
    Stage tarfiles in a "homedir"

    run ltgTrim to refine area
        (this script decompresses files then writes selected strikes to YYYY.txt files)

    run useProcessedLtg to create DataFrame from trimmed lightning files
        (reads YYYY.txt files, appends them into a dataframe (D) and saves as pickle file)

    run plot_ltg_test extracts from dataframe to plot lightning density
