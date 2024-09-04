import requests
import time
import re

"""Used to get the maximum value page number in list of urls to extract"""
def get_maximum(html_string):
    # get the tag
    final_list_tag = re.search(r'<li class="pager-last last">.*?<\/li>', html_string)

    # check it exists
    if (not final_list_tag):
        print("final_list_tag not working in get_maximum function")
        exit()

    # get the maximum number from the url link
    max_number = re.search(r'href="\/site-map\?page=([\d]+)', final_list_tag.group())

    # check it exists
    if (not max_number):
        print("max_number not working in get_maximum function")
        exit()

    # return this maximum number
    return int(max_number.group(1))

## GET THE PAGES TO VISIT ------------------------------------------------------------------------------

URL = "https://www.oldlistings.com.au/site-map?state=VIC"
HEADER = {'User-Agent': "University of Melbourne MAST30034 (mtpawlus32@gmail.com)"}
TIME_HALT = 10

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

## GET ALL THE URLS FROM PAGES -------------------------------------------------------------------------

print("begin stage 2:\n")

DOMAIN_NAME = "https://www.oldlistings.com.au"
SURBURB_HOME_PATTERN = r'<a href="(\/real-estate\/VIC\/[^\/]+\/\d{4}\/rent\/)">'

with open("../data/landing/suburbs.txt", "w") as out_file:
    for page_url in page_url_list:
        # print current url
        print(page_url)

        # get the url for the page
        page_response = requests.get(page_url, headers=HEADER)

        # check that it exists
        if (first_response.status_code != 200):
            print(f"error response. exit code:{first_response.status_code}")
            exit()

        # get the current page text
        html_text = page_response.text

        # find the urls matching the pattern and create their absolute path
        out_urls = re.findall(SURBURB_HOME_PATTERN, html_text)
        out_urls = [DOMAIN_NAME + out_url + '\n' for out_url in out_urls]

        # make sure they are unique
        out_urls = sorted(list(set(out_urls)))

        # output the file
        out_file.writelines(out_urls)

        # let the sever reset
        time.sleep(TIME_HALT)