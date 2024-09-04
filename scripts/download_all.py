import requests
import re
import os
import time

#### TO DO --------------------------------------------------------

# used to test
def test_recent_enough(response_page):
    return True

# used to test if the location is close enough to melbourne (exclude places like bendigo)
def test_location(suburb_url):
    # good use the postal code or something with RE
    return True

#### DOWNLOADING FUNCTION ------------------------------------------------------

# DO NOT CHANGE
HEADER = {'User-Agent': "University of Melbourne MAST30034"}
SUBURB_URL = "https://www.oldlistings.com.au/real-estate/VIC/Williamstown+North/3016/rent/"
DST_SUFFIX = "../data/landing/"

SUBRUB_SEARCH = r'.*\/VIC\/([^\/]+)\/\d{4}' # used to extract the suburb from the url
MAXIMUM = 5000 # the maximum amount of pages to get per suburb (13 hours, don't get here)
TIME_HALT = 10.2 # the seconds at which to request each page (more than 10 just in case)

""""Starts at the suburb_url, then append /i onto it continuously until error code status occurs, saving all html page files
NOTE:
    - Will create a directory even for empty files
    - Assumes /1 works
    - Will automatically sleep"""
def get_suburb_files(suburb_url):
    # get the suburb name formatted correctly
    suburb_name = re.search(SUBRUB_SEARCH, suburb_url).group(1)
    suburb_name = re.sub(r'\+', ' ', suburb_name) # replace '+' with ' ' all occurences

    # if not close enough to melbourne, delete
    if (not test_location(SUBURB_URL)):
        print("not interest this location")
        return

    # create the output directory path
    if (not os.path.exists(DST_SUFFIX + suburb_name)):
        os.mkdir(DST_SUFFIX + suburb_name)

    # go through each consecutive page until get an error
    for i in range(1, MAXIMUM+1):
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

SUBURB_FILE = "../data/landing/suburbs.txt"

with open(SUBURB_FILE, "r") as suburb_file:
    # get all the urls
    suburb_urls = suburb_file.readlines()

    # remove the newlines
    suburb_urls = list(map(lambda x: x.strip(), suburb_urls))

    for suburb_url in suburb_urls:
        get_suburb_files(suburb_url)

time.sleep(10)