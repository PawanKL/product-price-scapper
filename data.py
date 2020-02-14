import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
# os.path.join()
# driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
url = 'https://www.ishopping.pk/electronics.html'
# print(driver)
def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    return driver
driver = getDriver()
driver.get(url)
time.sleep(1)
print(driver)