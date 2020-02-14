import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
# os.path.join()
# driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
# print(driver)
def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    return driver
driver = getDriver()
for i in range(10,21):
    url = 'https://www.ishopping.pk/catalog/seo_sitemap/category?p='
    url = url + str(i)
    driver.get(url)
    links = []
    names = []
    time.sleep(3)
    sitemap = driver.find_element_by_class_name("sitemap")
    categories = sitemap.find_elements_by_tag_name("li")
    print('Scraping:' + url)
    for c in categories:
        link = c.find_element_by_tag_name("a")
        href = link.get_attribute("href")
        text = link.get_attribute("text")
        links.append(href)
        names.append(text)  
    category_link  = np.array(links)
    category_names = np.array(names)
    df = pd.DataFrame({'Category': category_names, 'Link': category_link})
    df1 = pd.read_csv('ishopping_categories.csv', index_col=False)
    df1 = df1.append(df, ignore_index=True, sort=False)
    print('Total Length: ' + str(len(df1)))
    print('Total Pages Scraped: ' + str(len(df1) // 50))
    df1.to_csv('ishopping_categories.csv', index=False)
    time.sleep(5)
driver.quit()