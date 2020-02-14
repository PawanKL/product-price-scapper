import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sched
import time
import pandas as pd
import numpy as np
from pymongo import MongoClient

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
print(client.list_database_names())

db = client.hci_database
print(db.list_collection_names())
print(db.list_collections())
# products = db.Products
# products.drop()
# data = pd.read_csv('./ishopping/ishopping_Mobile Phones.csv')

# for index, row in data.iterrows():
#     Product = {
#     'ProductName': row['Product Name'],
#     'ProductPage': row['Product Page'],
#     'ProductImage': row['Product Image'],
#     'Price': row['Price'],
#     'DiscountPrice': row['Discount Price'],
#     'Category': row['Category'],
#     'Site': row['Site'],
#     }
#     products.insert_one(Product)
# print(products.find_one())
# print(products.count())
# docs = products.find(limit=20)
# for doc in docs:
#     print(doc)
