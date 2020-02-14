import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
from pymongo import MongoClient
from pprint import pprint

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
# filename = "ishopping_Musical Instruments.csv"
path = './shophive/'
save_path = './shophive/done/'
filenames = find_csv_filenames(path)
print(filenames)
for f in filenames:
    newPath = path + f
    data = pd.read_csv(newPath)
    # data.sort_values('Product Name', inplace = True)
    # data.drop_duplicates(subset = 'Product Name', keep = False, inplace =  True)
    np_prices = np.array(data['Price'])
    print(len(np_prices))
    np_discount_prices = np.array(data['Discount Price'])
    prices = []
    discount_prices = []
    n=m=a=b=0
    for i in range(len(np_prices)):
        # print(np_prices[i])
        str_price = np_prices[i]
        str_discount_price = np_discount_prices[i]
        if((str_price != '') & (str_price != 'Call for Price')):
            np1 = str_price.split(' ')[1]
            n+=1
            if(',' in np1):
                first = np1.split(',')[0]
                second = np1.split(',')[1]
                newPrice = int(first + second)
                # print(first + ' ' + second)
                prices.append(newPrice)
            else:
                newPrice = int(np1)
                prices.append(newPrice)   
        else:
            m+=1
            prices.append(-1)
        if((str_discount_price != 'None') & (str_discount_price != 'Call for Price')):
            np1 = str_discount_price.split(' ')[1]
            a+=1
            if(',' in np1):
                first = np1.split(',')[0]
                second = np1.split(',')[1]
                newPrice = int(first + second)
                # print(first + ' ' + second)
                # print(newPrice)
                discount_prices.append(newPrice)
            else:
                newPrice = int(np1)
                discount_prices.append(newPrice) 
        else:
            b+=1
            discount_prices.append(-1)
    # print(len(np.array(prices)))
    del data['Price']
    del data['Discount Price']
    data['Price'] = np.array(prices)
    data['Discount Price'] = np.array(discount_prices)
    npath = save_path + f
    data.to_csv(npath, index=False)
    del data
    del np_prices
    del np_discount_prices
    del prices
    del discount_prices
