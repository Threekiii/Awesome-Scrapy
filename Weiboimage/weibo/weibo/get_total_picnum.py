import requests
import os
import random
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('39.107.98.219', 27017)
    db_name = 'weibo'
    db = client[db_name]
    collection_name_list = ['faceu','轻颜','水柚','b612','无他相机','一甜相机']
    date_list = ['2019-12-31','2020-01-01']
    for date in date_list:
        filters = {'time': {'$gte': date, '$lte': date}}
        for collection_name in collection_name_list:
            collection = db[collection_name]
            results = collection.find(filters)
            number = 0
            for i in range(0,results.count()):
                result = results[i]
                number = result['picture_num'] + number
            print('{}   {}: 共有图片{}张.'.format(date,collection_name,number))