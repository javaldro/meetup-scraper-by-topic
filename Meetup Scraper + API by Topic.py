#Importing packages
import pycurl
from StringIO import StringIO
import json
import csv
import pandas as pd
from tqdm import tqdm
from pandas.io.json import json_normalize
import requests
from bs4 import BeautifulSoup

# Input a topic name from https://www.meetup.com/topics/ . This example will conitnue with musical theatre
topic = "musical-theatre" ### your topic here
# Put your password / api key using https://secure.meetup.com/meetup_api/key/ . This will not work without it
password =  ### your api key here

# Creating a link based on your topic of interest
url = "https://www.meetup.com/topics/" + topic + "/all/"
# Finding all of the meetups associated with this topic
response = requests.get(url, params={"search_api_views_fulltext": ""})
soup = BeautifulSoup(response.text)
links_messy = soup.find_all('li', attrs={'class':'gridList-item'})

# Create a clean list of links
group_name_list = []
for i in range(0,len(links_messy)):
    selector = links_messy[i].select('a')[0]
    link = selector['href']
    group_name = link.split("/")[3]
    group_name_list.append(group_name)

# Create an empty list to dump list of jsons in
json_list = []
# Iterate over each group name
for name in tqdm(group_name_list):
    # Create link for group
    api_link = "https://api.meetup.com/" + name + "?&sign=true&photo-host=public"
    # Pycurl call
    buffer = StringIO()
    c = pycurl.Curl()  
    c.setopt(c.URL, api_link)
    c.setopt(c.USERPWD, password)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    # Convert output into a json, then append it to a list of jsons
    body = buffer.getvalue()
    group_json = json.loads(body)
    json_list.append(group_json)

# Create a pandas dataframe with all of the data from  the json_list
meetup_dataset = json_normalize(json_list)

# Converting pandas dataframe into a csv2 file for further use 
filename =  topic + '-Meetup-Dataset.csv'
meetup_dataset.to_csv(filename, encoding='utf-8')

