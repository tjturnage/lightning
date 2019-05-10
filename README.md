This utilizes strike data from tarfiles available at ftp://ftp-restricted.ncdc.noaa.gov/data/lightning/

Step 1.  Stage tarfiles in a "homedir"

Step 2. Run ltgDecompressTrim.py to extract data for lat/lon area of interest area
        (this script decompresses files then writes selected strikes to YYYY.txt files)

Step 3. Run useProcessedLtg to create DataFrame from trimmed lightning files
        (reads YYYY.txt files, appends them into a dataframe (D) and saves as pickle file)

Step 4. Run plot_ltg_test to extract data from created DataFrame and plot lightning density
