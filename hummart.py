import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
data  = pd.read_csv('ishopping_categories.csv')
site_name = 'ishopping'
def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    # options.add_argument("--kiosk")
    driver = webdriver.Chrome()
    return driver
def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    time1 = time.time()
    while True:
        time2 = time.time()
        total_time =  (time2 - time1)
        if(total_time > 180):
            break
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
driver = getDriver()
url = 'https://hummart.com/'
driver.get(url)
time.sleep(5)
links = []
categories = []
nav = driver.find_element_by_css_selector('.navigation.sw-megamenu')
ul = nav.find_elements_by_tag_name('ul')[0]
li = ul.find_elements_by_tag_name('li')
for l in li:
    anchor_tag = l.find_elements_by_tag_name('a')[0]
    span = l.find_elements_by_tag_name('span')[0]
    cat = span.text
    href = anchor_tag.get_attribute('href')
    links.append(href)
    categories.append(cat)
print(links)
sites = []
for i in range(len(links)):
    sites.append('Hum Mart') 
data = pd.DataFrame()
data['Category'] = np.array(categories)
data['Link'] = np.array(links)
data['Site'] = np.array(sites)
data = data.drop([6], axis=0)
data.reset_index(inplace =  True)
data.to_csv('./hummart/categories.csv')
driver.quit()