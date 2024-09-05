import requests
import time
import re
import pandas as pd

### TO DO -------------------------------------------------------------------------------------------------
# - basically use some kind of API to filter out suburbs that are too far from melbourne. For example, some way 
#   of selecting Carlton and Fitzroy out of Carlton, Fitzroy and Bendigo South. This is located at stage 3 in
#   test location
#   - This set is necessary, as currently, there are 3500 site locations in victoria, but there are only 
#     apparently 340 suburbs in melbourne. So 3500 sites will take 10 hours to open every url, while 340
#     will only take an hour (much more doable)      
#   - Once done, can delete "exit() at stage 4"
### --------------------------------------------------------------------------------------------------------

### 1. GET THE PAGES TO VISIT ------------------------------------------------------------------------------
# - get all the pages of the form https://www.oldlistings.com.au/site-map?state=VIC(&page=x) so that
#   next step, all the suburb urls can be harvested
### ---------------------------------------------------------------------------------------------------------

print("Stage 1: creating pages to visit\n")

"""Used to get the maximum value page number in list of urls to extract"""
def get_maximum(html_string):
    # get the tag
    final_list_tag = re.search(r'<li class="pager-last last">.*?<\/li>', html_string)

    # check it exists
    if (not final_list_tag):
        print("final_list_tag not working in get_maximum function")
        exit()

    # get the maximum number from the url link
    max_number = re.search(r'href=[\'\"]\/site-map\?page=([\d]+)', final_list_tag.group())

    # check it exists
    if (not max_number):
        print("max_number not working in get_maximum function")
        exit()

    # return this maximum number
    return int(max_number.group(1))

URL = "https://www.oldlistings.com.au/site-map?state=VIC"
HEADER = {'User-Agent': "University of Melbourne MAST30034"}
TIME_HALT = 10.2

# get the first page
first_response = requests.get(URL, headers=HEADER)
if (first_response.status_code != 200):
    print(f"error response. exit code:{first_response.status_code}")
    exit()

# wait for the sever to reset
time.sleep(TIME_HALT)

# get the text of first page
first_html_text = first_response.text

# get the last page number
last_page = get_maximum(first_html_text)

# get all the urls to visit
page_url_list = [URL + '&page=' + str(page_num) for page_num in range(1, last_page+1)]
page_url_list.insert(0, URL)

print(page_url_list)


## 2. GET ALL THE URLS FROM PAGES -------------------------------------------------------------------------
# - go through each page of the form https://www.oldlistings.com.au/site-map?state=VIC(&page=x) and harvest
#   all the suburbs in victoria of the form https://www.oldlistings.com.au/real-estate/VIC/[suburb]/[postcode]/rent/
### -----------------------------------------------------------------------------------------------------

print("Stage 2: collecting URLS\n")

DOMAIN_NAME = "https://www.oldlistings.com.au"
SURBURB_HOME_PATTERN = r'<a href=[\'\"](\/real-estate\/VIC\/[^\/]+\/\d{4}\/rent\/)[\'\"]>'

out_urls = []

# getting all the urls
for page_url in page_url_list:
    # print current url
    print(page_url)

    # get the url for the page
    page_response = requests.get(page_url, headers=HEADER)

    # check that it exists
    if (page_response.status_code != 200):
        print(f"error response. exit code:{page_response.status_code}")
        exit()

    # get the current page text
    html_text = page_response.text

    # find the urls matching the pattern and create their absolute path
    curr_out_urls = re.findall(SURBURB_HOME_PATTERN, html_text)
    curr_out_urls = [DOMAIN_NAME + out_url for out_url in curr_out_urls]

    # make sure they are unique
    curr_out_urls = sorted(list(set(curr_out_urls)))

    # add to the list
    out_urls.extend(curr_out_urls)

    # let the sever reset
    time.sleep(TIME_HALT)


### 3. FILTERING LOCATION ------------------------------------------------------------------------------
# - Create a data frame which has:
#   - URL
#   - suburb name
#   - postcode
# - Filter out URLS that are too far from melbourne <---------- TO DO
### -----------------------------------------------------------------------------------------------------

print("Stage 3: filtering by location\n")

SUBRUB_INFO_SEARCH = r'.*\/VIC\/([^\/]+)\/(\d{4})' # used to extract the suburb and postcode

"""used to test if the location is close enough to melbourne (exclude places like bendigo)"""
"""input should be a row of this data frame, and output should be boolean value, whether to include in dataframe or not"""
def test_location(suburb_url):
    # could use the postal code or something with RE
    return True

# create the data frame with attributes
suburbs_all_df = pd.DataFrame(out_urls, columns=["URL"])
suburbs_all_df["suburb name"] = suburbs_all_df["URL"].apply(lambda x: re.search(SUBRUB_INFO_SEARCH, x).group(1))
suburbs_all_df["suburb name"] = suburbs_all_df["suburb name"].apply(lambda x: re.sub(r'\+', ' ', x))    # replace '+' with ' '
suburbs_all_df["postcode"] = suburbs_all_df["URL"].apply(lambda x: re.search(SUBRUB_INFO_SEARCH, x).group(2))

# apply the location filter
location_filter = suburbs_all_df.apply(test_location, axis="columns")
suburbs_df = suburbs_all_df[location_filter]
suburbs_df = suburbs_df.reset_index()

## 4. COUNT NUMBER OF OCCURENCES -------------------------------------------------------------------------
# - count the number of pages that is associated with each suburb. For example, williamstown may have 300
#   rental properties ever, and as 50 listings are shown per page, will have 6 pages, hence count will be 6
#   - Note: count will be 0 if the page doesn't exist, or negative if there was a problem with the URL request (say forbidden)
### -----------------------------------------------------------------------------------------------------

# DETELE ONCE CREATED FUNCTION FOR LOCATION
exit()

print("Stage 4: counting the number of pages per suburb\n")


"""will look for pages that have at least one second page"""
def page_pattern(suburb_url):
    # ensure that using the relative url (as how appears in website)
    suburb_relative_url = suburb_url[len(DOMAIN_NAME):]

    # get the pattern
    pattern = r'<a href=[\'\"]' + re.escape(suburb_relative_url) + r'(\d+)[\'\"]'

    return pattern


""""Will return the number of pages that exist for the suburb as an integer
NOTE: 
    - will return a negative value for a bad response
    - will basically look at the url with the highest page ending"""
def get_count(suburb_url):
    # get the response
    response = requests.get(suburb_url, headers=HEADER)

    # ensure handled when the response fails
    if (response.status_code == 404):
        # page doesn't exist so zero count
        return 0
    
    elif (response.status_code != 200):
        # return the negative of the response.status_code
        return -1 * response.status_code

    # get the text
    html_text = response.text

    # get all the urls and numbers within urls matching
    url_number_matches = re.findall(page_pattern(suburb_url), html_text)

    # if only match, then there is only the main suburb page
    if (len(url_number_matches) == 0):
        return 1

    # otherwise, can extract the numbers
    url_number_matches = [int(url_number_match) for url_number_match in url_number_matches]

    # get the maximum url_number
    count = max(url_number_matches)

    # return this count
    return count


# EXECUTE

# get the counts for each url
counts = []
for suburb_url in suburbs_df["URL"].values:
    print(f"({time.time()}) ", end="")
    print(suburb_url)

    # get the start time
    start_time = time.time()

    # append the count for the url
    count = get_count(suburb_url)
    counts.append(count)
    #print(count)

    # get the time it took for this loop
    iteration_time = time.time() - start_time

    # sleep for the exact amount of time required
    time.sleep(TIME_HALT - iteration_time)

# add count information
suburbs_df["counts"] = counts

# save the file
suburbs_df.to_csv("../data/landing/suburbs.csv", index=False)