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
for i in range(8,30,1):
    category_name = data.iloc[i][1]
    url = data.iloc[i][2]
    driver.get(url)
    time.sleep(4)
    scroll_down(driver)
    product_names = []
    product_pages = []
    product_images = []
    product_prices = []
    discount_prices = []
    sites = []
    categories = []
    # sitemap = driver.find_element_by_css_selector(".products-grid.col-sm-12.products-grid--max-4-col-.first.last.odd")
    try:
        sitemap = driver.find_element_by_css_selector(".category-products-")
        products = sitemap.find_elements_by_tag_name("li")
    except:
        continue
    # print(products)
    # print(len(products))
    countProducts = 0
    for p in products:
        # if(countProducts == 200):
        #     break
        try:
            div_image = p.find_element_by_css_selector(".inner-grid")
            link = div_image.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            title = link.get_attribute("title")
            img = div_image.find_element_by_tag_name("img")
            src = img.get_attribute("src")
            div_product_info = div_image.find_element_by_css_selector(".product-info-.white")
            div_price_info = div_product_info.find_element_by_css_selector(".price-box")
            try:
                p_special_price = div_price_info.find_element_by_css_selector(".special-price")
                span_special_price = p_special_price.find_element_by_css_selector(".price")
                p_old_price = div_price_info.find_element_by_css_selector(".old-price")
                span_old_price = p_old_price.find_element_by_css_selector(".price")
                discount_prices.append(span_special_price.text)
                product_prices.append(span_old_price.text)
                product_pages.append(href)
                product_names.append(title)
                product_images.append(src)
                sites.append(site_name)
                categories.append(category_name) 
                countProducts+=1
            except:
                span_regular_price = div_price_info.find_element_by_css_selector(".regular-price")
                price = span_regular_price.find_element_by_css_selector(".price")
                product_pages.append(href)
                product_names.append(title)
                product_images.append(src)
                product_prices.append(price.text)
                discount_prices.append('None')
                sites.append(site_name)
                categories.append(category_name)  
                countProducts+=1
        except:
            pass
    df = pd.DataFrame({'Product Name': np.array(product_names), 'Product Page': np.array(product_pages), 'Product Image':np.array(product_images),
                    'Price': np.array(product_prices),'Discount Price': np.array(discount_prices), 'Category': np.array(categories), 'Site': np.array(sites) })
    filename = './ishopping/ishopping_' + category_name + '.csv'
    if(os.path.exists(filename)):
         df1 = pd.read_csv(filename, index_col=False)
         df1 = df1.append(df, ignore_index=True, sort=False)
         df1.to_csv(filename)
    else:
        df.to_csv(filename)
driver.quit()