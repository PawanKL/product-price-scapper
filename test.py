import pandas as pd
import time
from pprint import pprint
# time1 = time.time()
# print(time1)
# while True:
#     time2 =  time.time()
#     total_time =  (time2 - time1)
#     print(total_time)
    # if(total_time > 180):
    #     break
data = pd.read_csv('./hummart/categories.csv')
# data = data.drop([6], axis = 0)
# data.to_csv('./hummart/categories.csv', index=True)
pprint(data)
# print(len(data['Category'].unique()))
# data.info()
# data = data.drop('Unnamed: 0', 1)
# data.to_csv('ishopping_categories.csv')