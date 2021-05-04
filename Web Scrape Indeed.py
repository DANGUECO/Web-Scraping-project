#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def get_url(position, location):
    """Generate url from position and location"""
    # remember to replace so it results q= {] and l={}
    placeholder = 'https://nz.indeed.com/jobs?q={}&l={}'
    # Format correctly to use url for multiple jobs.
    url = placeholder.format(position, location)
    return url


# create a function for grabbing all the necessary information
def information(card):
    # fast way to get the title.
    title = card.h2.a.get('title')
    job_url = 'https://nz.indeed.com' + card.h2.a.get('href')
    location = card.find('div', 'recJobLoc').get('data-rc-loc')
    summary = card.find('div', 'summary').text.strip()
    postdate = card.find('span', 'date').text.strip()
    currentTime = datetime.today().strftime('%Y-%m-%d')

    # need to account for none type as some information maybe missing.
    try:
        company = card.find('span', 'company').text.strip()
    except AttributeError:
        company = ''

    try:
        salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        salary = ''

    record = (title, company, location, summary, postdate, currentTime, salary, job_url)
    return record


# NOTE:the code below is mainly used from Israels github at https://github.com/israel-dryer/Indeed-Job-Scraper

def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position, location)

    # extract the job data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')
        for card in cards:
            record = information(card)
            records.append(record)
        # keeps trying to find more pages until there is an error. If there is an error then there are no more pages.
        try:
            url = 'https://nz.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    # save the job data
    with open('dataAnalystJobPosting.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Creates a header Row
        writer.writerow(
            ['JobTitle', 'Company', 'Location', 'Summary', 'ExtractDate', 'Current Date', 'Salary', 'JobUrl'])
        # Adds the record and other information under the header.
        writer.writerows(records)


#  run the main program
# main(position and location here for swapping)
main('analyst', 'Wellington')


# In[2]:


job = pd.read_csv('dataAnalystJobPosting.csv')
job


# In[ ]:




