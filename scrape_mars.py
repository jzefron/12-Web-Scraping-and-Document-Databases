#!/usr/bin/env python
# coding: utf-8




# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd



conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

def scrape():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    results =soup.find_all('div',class_="slide")
    articles = []
    for article in results:
    # print(article)
        d = article.find('div',class_= 'content_title')
        #print(d)
        headline = d.find('a').text
        headline = headline.replace('\n',"")
        #print('he' + headline)
        desc = article.find('div', class_='rollover_description_inner').text
        desc= desc.replace('\n',"")
        articles.append({'headline':headline, 'description':desc})
    #articles has the mars headlines

    #now doing image load
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    base_url = 'https://www.jpl.nasa.gov/'
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(pic_url)
    el = browser.find_link_by_partial_text('FULL IMAGE')
    featured_image_url =base_url + el['data-fancybox-href']

    #Finding mars weather

    twit_url = 'https://twitter.com/marswxreport'
    tweponse = requests.get(twit_url)
    # Create BeautifulSoup object; parse with 'lxml'
    twoup = BeautifulSoup(tweponse.text, 'html.parser')

    feed = twoup.find('div',class_='js-tweet-text-container')#,class_='TwetTextSize')
    mars_weather  = feed.find('p').text
     

    #getting facts
    facts_url = 'https://space-facts.com/mars/'
    fact_tables = pd.read_html(facts_url)

    tab = fact_tables[0]
    tab = tab.rename(columns={0:'Feature',1:'Fact'})
    #tab = tab.set_index('Feature')
    tab.to_html().replace('\n','')



    hemi_images = {
        'Hemisphere':'Cerberus','url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
        'Hemisphere':'Schiaparelli','url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
        'Hemisphere':'Syrtis Major','url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
        'Hemisphere':'Valles Marineris','url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
    }




