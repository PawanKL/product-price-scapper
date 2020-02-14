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
def addProducts(data, products):
    for index, row in data.iterrows():
        Product = {
        'ProductName': row['Product Name'],
        'ProductPage': row['Product Page'],
        'ProductImage': row['Product Image'],
        'Price': row['Price'],
        'DiscountPrice': row['Discount Price'],
        'Category': row['Category'],
        'Site': row['Site'],
        }
        products.insert_one(Product)

# Build Connection
client = MongoClient('mongodb://localhost:27017/')
# List of Databases
print(client.list_database_names())
# Get DataBase
db = client.hci_database
# List Of Collections
print(db.list_collection_names())
products = db.Products
# path = './ishopping/ishopping_Formal Shoes.csv'
# data = pd.read_csv(path)
# addProducts(data, products)
# total_products = products.find().count()
# print('Total Products: ', total_products)
# print(products.find({}, {'Price':1, '_id':0}).count())
n=m=0
a=b=0
prices = []
discount_prices = []
mongoose_ids = []
for price in products.find({}, {'Price':1,'DiscountPrice': 1, '_id':1}):
    str_price = str(price['Price'])
    str_discount_price = str(price['DiscountPrice'])
    mongoose_ids.append(price['_id'])
    if(str_price != ''):
        np1 = str(str_price.split(' ')[1])
        n+=1
        if(',' in np1):
            first = np1.split(',')[0]
            second = np1.split(',')[1]
            newPrice = int(first + second)
            # print(first + ' ' + second)
            # print(newPrice)
            prices.append(newPrice)
    else:
        m+=1
        prices.append(-1)
    if(str_discount_price != 'None'):
        np1 = str(str_discount_price.split(' ')[1])
        a+=1
        if(',' in np1):
            first = np1.split(',')[0]
            second = np1.split(',')[1]
            newPrice = int(first + second)
            # print(first + ' ' + second)
            # print(newPrice)
            discount_prices.append(newPrice)
    else:
        b+=1
        discount_prices.append(-1)
print('n = ', n)
print('m = ', m)
print('a = ', a)
print('b = ', b)
print(len(mongoose_ids))
print(len(prices))
print(len(discount_prices))
# print(str(prices[0]) + "+" + str(prices[1]) + " = " + str(prices[0] + prices[1]))
# print(prices)
# print(discount_prices)
# print(products.find_one({},{'Price': 1,'DiscountPrice': 1, "_id": 0}))

# for i in range(len(mongoose_ids)-1):
#     products.update_one({"_id": mongoose_ids[i]}, {"$set":{"Price":prices[i],"DiscountPrice": discount_prices[i]}})
# pprint(products.find_one())
# print(products.count())
# i = 1
# for prod in products.find({}):
#     print(str(prod['Price']) + " i = " + str(i))
#     i+=1