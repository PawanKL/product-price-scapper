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
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
# Build Connection
client = MongoClient('mongodb://localhost:27017/')
# List of Databases
print('List Of Databases')
print(client.list_database_names())
# Get DataBase
print('hci database')
db = client['hci_database']
# List Of Collections hci_database
print('List Of Collections hci_database')
print(db.list_collection_names())
# Products Collection
products = db.Products
# Number of Products
print('Total Number Of Products: ', products.estimated_document_count())
# Database for the web app
print('price app database')
db1 = client['priceapp']
# List Of Collections priceapp
print('List Of Collections priceapp')
print(db1.list_collection_names())
# Products Collection
products1 = db1['Products']
print('Total Number Of Products: ', products1.estimated_document_count())
# Categories Collection
categories = db1['Categories']
print('Total Number Of Categories: ', categories.estimated_document_count())


# path = './shophive/done/'
# filenames = find_csv_filenames(path)
# for f in filenames:
#     newPath = path + f
#     data = pd.read_csv(newPath)
#     addProducts(data, products)
#     total_products = products.find().count()
#     print('Total Products: ', total_products)
# print(products.find({}, {'Price':1, '_id':0}).count())
# total_products = products.find().count()
# print('Total Products: ', total_products)
# pprint(products.find_one({' _id': '5dc1cef3741791c08c67d774'}))
# products.find_one('_id': '5dc1cef3741791c08c67d774')
# cluster =  products.find()
# pprint(cluster[7324])
# for prod in products.find():
#     print(prod)
# cts = 0
# for cat in products.find({}, {'ProductName': 1, 'Category': 1,'Site': 1, '_id': 0,}).distinct('Category'):   
#     pprint(cat)
#     cts+=1
# print(cts)
# cts = 0
# for cat in products.find({}, {'ProductName': 1,'Price': 1, 'Category': 1,'Site': 1, '_id': 0,}, skip = 4000, limit = 5):   
#     pprint(cat)
    # cts+=1
# print(cts)
def makeData(products, products1):
    i = 1
    for prod in products.find({}):
        Product = {
            'ProductId': i,
            'ProductName':   prod['ProductName'],
            'ProductPage':   prod['ProductPage'],
            'ProductImage':  prod['ProductImage'],
            'Price':         prod['Price'],
            'DiscountPrice': prod['DiscountPrice'],
            'Category':      prod['Category'],
            'Site':          prod['Site'],
            }
        i+=1
        products1.insert_one(Product)
# makeData(products, products1)
# print(products1.estimated_document_count())
# pprint(products1.find_one({'ProductId': 1}))
# cats = products1.distinct('Category')
# print(categories)
# i = 1
# for cat in cats:
#     image = products1.find_one({'Category': cat}, {'_id':  0, 'ProductImage': 1})
#     Category = {
#         'CategoryId': i,
#         'CategoryName': cat,
#         'CategoryImage': image['ProductImage'],
#     }
#     categories.insert_one(Category)
#     i+=1
# for cat in categories.find({},limit = 5):
#     pprint(cat)
# categories.drop()