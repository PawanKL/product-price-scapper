import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
data  = pd.read_csv('hummart_categories.csv')
site_name = 'Hum Mart'
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
for i in range(16):
    category_name = data.iloc[i][2]
    print(category_name)
    url = data.iloc[i][3]
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
    sitemap = driver.find_element_by_css_selector(".products.wrapper.grid.columns4.products-grid")
    try:
        # sitemap = driver.find_element_by_css_selector(".category-products-")
        ols = driver.find_elements_by_tag_name('ol')[0]
        products = ols.find_elements_by_tag_name("li")
    except:
        continue
    # # print(products)
    print(len(products))
    for p in products:
        try:
            div_info = p.find_element_by_css_selector(".product-item-info")
            div_link_info = div_info.find_element_by_css_selector(".product.photo.product-item-photo")
            link = div_link_info.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            image = div_link_info.find_element_by_tag_name("img")
            src = image.get_attribute("src")
            prod_name = image.get_attribute("alt")
            div_product_detail = p.find_element_by_css_selector(".product.details.product-item-details")
            # print("div_product_detail")
            # print(div_product_detail)
            div_product_detail1 = div_product_detail.find_element_by_css_selector(".express-mobile-hide")
            # print("div_product_detail1")
            # print(div_product_detail1)
            div_product_detail2 = div_product_detail1.find_element_by_css_selector(".price-box.price-final_price")
            # print("div_product_detail2")
            # print(div_product_detail2)
            # span_price = div_product_detail2.find_element_by_css_seletor(".price-container.price-final_price.tax.weee")
            span_price = div_product_detail2.find_element_by_tag_name("span")
            # print(span_price)
            span_price1 = span_price.find_element_by_css_selector(".price-wrapper ")
            # print(span_price1)
            # span_price2 = span_price1.find_element_by_css_selector(".price")
            price = span_price1.get_attribute('data-price-amount')
            # print(price)
            product_names.append(prod_name)
            product_pages.append(href)
            product_images.append(src)
            print(price)
            product_prices.append(int(price))
            discount_prices.append(-1)
            categories.append(category_name)
            sites.append(site_name)
        except:
            pass
    df = pd.DataFrame({'Product Name': np.array(product_names), 'Product Page': np.array(product_pages), 'Product Image':np.array(product_images),
                    'Price': np.array(product_prices),'Discount Price': np.array(discount_prices), 'Category': np.array(categories), 'Site': np.array(sites) })
    filename = './hummart/hummart_' + category_name + '.csv'
    if(os.path.exists(filename)):
         df1 = pd.read_csv(filename, index_col=False)
         df1 = df1.append(df, ignore_index=True, sort=False)
         df1.to_csv(filename)
    else:
        df.to_csv(filename)
driver.quit()