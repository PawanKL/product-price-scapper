import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
data  = pd.read_csv('shophive_categories.csv')
site_name = 'Shophive'
class Page:
    def __init__(self):
        self.product_names = []
        self.product_pages = []
        self.product_images = []
        self.product_prices = []
        self.discount_prices = []
        self.sites = []
        self.categories = []
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
def next_page(driver, category, site):
    remaining_pages =  True
    p = Page()
    while remaining_pages:
        try:
            uls = driver.find_element_by_css_selector('.products-grid')
            lis = uls.find_elements_by_tag_name('li')
            # print('product grid')
            count = 0
            for li in lis:
                if(count >= 20):
                    break
                try:
                    anchor = li.find_element_by_tag_name('a')
                    href =  anchor.get_attribute('href')
                    title = anchor.get_attribute('title')
                    img = li.find_element_by_tag_name('img')
                    img_link = img.get_attribute('src')
                    try:
                        div_price = li.find_element_by_css_selector('.price-box')
                        span_regular_price =  div_price.find_element_by_css_selector('.regular-price')
                        span_price = span_regular_price.find_element_by_css_selector('.price')
                        price = span_price.text
                        dist_price = 'None'
                        p.product_names.append(title)
                        p.product_pages.append(href)
                        p.product_images.append(img_link)
                        p.product_prices.append(price)
                        p.discount_prices.append(dist_price)
                        p.categories.append(category)
                        p.sites.append(site)
                        count+=1
                    except:
                        pass
                    try:
                        div_price = li.find_element_by_css_selector('.price-box')
                        span_price =  div_price.find_element_by_css_selector('.price.old-price')
                        price = span_price.text
                        span_discount_price = div_price.find_element_by_css_selector('.price.special-price')
                        dist_price = span_discount_price.text
                        p.product_names.append(title)
                        p.product_pages.append(href)
                        count+=1
                        p.product_images.append(img_link)
                        p.product_prices.append(price)
                        p.discount_prices.append(dist_price)
                        p.categories.append(category)
                        p.sites.append(site)
                        count+=1
                    except:
                        pass
                except:
                    continue
        except:
            pass
        try:
            uls = driver.find_element_by_css_selector('.products-list')
            lis = uls.find_elements_by_tag_name('li')
            # print('product list')
            count = 0
            for li in lis:
                if(count >=20):
                    break
                try:
                    div_left = li.find_element_by_css_selector('.list-left')
                    anchor = div_left.find_element_by_tag_name('a')
                    href =  anchor.get_attribute('href')
                    title = anchor.get_attribute('title')
                    img = li.find_element_by_tag_name('img')
                    img_link = img.get_attribute('src')
                    try:
                        div_right = li.find_element_by_css_selector('.list-right')
                        div_price = div_right.find_element_by_css_selector('.price-box')
                        span_regular_price =  div_price.find_element_by_css_selector('.regular-price')
                        span_price = span_regular_price.find_element_by_css_selector('.price')
                        price = span_price.text
                        dist_price = 'None'
                        p.product_names.append(title)
                        p.product_pages.append(href)
                        p.product_images.append(img_link)
                        p.product_prices.append(price)
                        p.discount_prices.append(dist_price)
                        p.categories.append(category)
                        p.sites.append(site)
                        count+=1
                    except:
                        pass
                    try:
                        div_price = li.find_element_by_css_selector('.price-box')
                        span_price =  div_price.find_element_by_css_selector('.price.old-price')
                        price = span_price.text
                        span_discount_price = div_price.find_element_by_css_selector('.price.special-price')
                        dist_price = span_discount_price.text
                        p.product_names.append(title)
                        p.product_pages.append(href)
                        p.product_images.append(img_link)
                        p.product_prices.append(price)
                        p.discount_prices.append(dist_price)
                        p.categories.append(category)
                        p.sites.append(site)
                        count+=1
                    except:
                        pass
                except:
                    continue
        except:
            pass
        try:
            page = driver.find_element_by_css_selector('.next.i-next')
            page.click()
            time.sleep(5)
        except:
            remaining_pages =  False
    return p
driver = getDriver()
for i in [14]:
    category_name = data.iloc[i][0]
    print(category_name)
    url = data.iloc[i][1]
    driver.get(url)
    time.sleep(4)
    page_data = next_page(driver, category_name, site_name)
    print("Total Products Scraped: ", len(page_data.product_names))
    # print(page_data.product_names)
    df = pd.DataFrame({'Product Name': np.array(page_data.product_names), 'Product Page': np.array(page_data.product_pages), 'Product Image':np.array(page_data.product_images),
                    'Price': np.array(page_data.product_prices),'Discount Price': np.array(page_data.discount_prices), 'Category': np.array(page_data.categories),
                     'Site': np.array(page_data.sites) })
    filename = './shophive/shophive_' + category_name + '.csv'
    if(os.path.exists(filename)):
         df1 = pd.read_csv(filename, index_col=False)
         df1 = df1.append(df, ignore_index=True, sort=False)
         df1.to_csv(filename)
    else:
        df.to_csv(filename)
driver.quit()