import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
data  = pd.read_csv('ishopping_categories.csv')
# links = np.array(data[])
category_name = data.iloc[1][1]
link = data.iloc[1][2]
def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    return driver
def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(4)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
driver = getDriver()
driver.get(link)
time.sleep(4)
scroll_down(driver)
product_names = []
product_pages = []
product_images = []
product_prices = []
sites = []
categories = []
# sitemap = driver.find_elements_by_class_name("products-grid.col-sm-12.products-grid--max-4-col-.first.last.odd")[0]
sitemap = driver.find_element_by_css_selector(".products-grid.col-sm-12.products-grid--max-4-col-.first.last.odd")
# sitemap = driver.find_elements_by_tag_name("ul")[100]
products = sitemap.find_elements_by_tag_name("li")
print(products)
print(len(products))
for p in products:
    try:
        div_image = p.find_element_by_css_selector(".inner-grid")
        link = div_image.find_element_by_tag_name("a")
        href = link.get_attribute("href")
        title = link.get_attribute("title")
        img = div_image.find_element_by_tag_name("img")
        src = img.get_attribute("src")
        div_product_info = div_image.find_element_by_css_selector(".product-info-.white")
        div_price_info = div_product_info.find_element_by_css_selector(".price-box")
        span_regular_price = div_price_info.find_element_by_css_selector(".regular-price")
        price = span_regular_price.find_element_by_css_selector(".price")
        product_pages.append(href)
        product_names.append(title)
        product_images.append(src)
        product_prices.append(price.text)
        sites.append('ishopping')
        categories.append(category_name)  
    except:
        print('Not Found..!! ') 
df = pd.DataFrame({'Product Name': np.array(product_names), 'Product Page': np.array(product_pages), 'Product Image':np.array(product_images),
                'Price': np.array(product_prices), 'Category': np.array(categories), 'Site': np.array(sites) })
filename = './ishopping/ishopping_' + category_name + '.csv'
df.to_csv(filename)
driver.quit()