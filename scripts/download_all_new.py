import requests
import re
import os
import time
import pandas as pd

#### TO DO -----------------------------------------------------------------------------------------------

# used to test if page has records recent enough
def test_recent_enough(response_page):
    return True

#### CONTSTANTS -----------------------------------------------------------------------------------------------

# DO NOT CHANGE
HEADER = {'User-Agent': "University of Melbourne MAST30034"}
SUBURB_URL = "https://www.oldlistings.com.au/real-estate/VIC/Williamstown+North/3016/rent/"
DST_SUFFIX = "../data/landing/"

SUBRUB_SEARCH = r'.*\/VIC\/([^\/]+)\/\d{4}' # used to extract the suburb from the url
TIME_HALT = 10.2 # the seconds at which to request each page (more than 10 just in case)

#### FUNCTIONS -----------------------------------------------------------------------------------------------

""""Starts at the suburb_url, then append /i onto it continuously until error code status occurs, saving all html page files
NOTE:
    - Will create a directory even for empty files
    - Assumes /1 works
    - Will automatically sleep (space between requests)"""
def get_suburb_files(suburb_row):
    # get the suburb name formatted correctly
    suburb_url = suburb_row["URL"]
    suburb_name = suburb_row["suburb name"]
    maximum = suburb_row["count"]

    # create the output directory path
    if (not os.path.exists(DST_SUFFIX + suburb_name)):
        os.mkdir(DST_SUFFIX + suburb_name)

    # go through each consecutive page until get an error
    for i in range(1, maximum+1):
        # record the start time
        start_time = time.time()

        # get the current URL
        curr_url = suburb_url + str(i)
        print(curr_url)

        # open the html
        response = requests.get(curr_url, headers=HEADER)

        # check to see if this page doesn't exist (gotten all the stuff)
        if (response.status_code != 200):
            print(f"error: response status code {response.status_code}, stopped at {i}")
            time.sleep(TIME_HALT - (time.time() - start_time))   # still need to rest
            return

        # check to see if the page features rentals that are recent enough
        if (test_recent_enough(response) == False):
            print(f"condition did not hold ... breaking")
            return
        
        # formatted '../data/raw/[suburb]/page_[number].html'
        dst_out = DST_SUFFIX + suburb_name + '/' + 'page_' + str(i) + '.html'

        # write the content to the file
        with open(dst_out, "wb+") as out:
            out.write(response.content)

        # get the execution time
        iteration_time = time.time() - start_time 

        # subtract from time halt to optimize
        time.sleep(TIME_HALT - iteration_time)


### EXECUTION -----------------------------------------------------------

SUBURB_CSV = "../data/landing/suburbs.csv"

suburbs_df = pd.read_csv(SUBURB_CSV)

# for each suburb, write all the subfiles
for i, suburb_row in suburbs_df.iterrows():
    get_suburb_files(suburb_row)

# just to ensure everything works
time.sleep(10)