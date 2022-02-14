# coding: utf-8
import re
import scrapy
import os, random, requests
from scrapy.cmdline import execute
from scrapy import Request
from pymongo import MongoClient
from weibo.items import WeiboItem,XhsItem
from weibo.settings import *
import datetime
import pymysql
from datetime import timedelta

class weiboimgSpider(scrapy.Spider):
    name = 'weibopicture'
    start_urls = []
    today = datetime.datetime.now()

    # last_saturday = str((today - timedelta(days=today.weekday() + 2)).date())
    # last_friday = str((today - timedelta(days=today.weekday() + 3)).date())
    # last_saturday = '2019-12-31'
    # last_friday = '2020-01-01'
    # date_list = [last_saturday,last_friday]

    def __init__(self,start_date=str((today - timedelta(days=today.weekday() + 2)).date()),end_date= str((today - timedelta(days=today.weekday() + 3)).date()),**kwargs):
        self.date_list = [start_date,end_date]

    def get_filter_dir(self,collection_name,start_date,end_date):
        filter_list = []
        with open('C:/Users/W/Desktop/filter_keywords.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                filter_list.append(line.strip())

        filter = {"$and": [{"time": {'$gte': start_date, '$lte': end_date}}] +
                          [{"text": {"$not": re.compile("b6-{0,1}12.{0,5}星球{0,1}", re.I)}}] +
                          [{"text": {"$not": re.compile(".*{}.*".format(i), re.I)}} for i in filter_list]}
        # filter = {'time': {'$gte': start_date, '$lte': end_date}}

        dir = 'C:/Users/W/Desktop/img/' + MONGODB_DBNAME + '-' + collection_name + '(' + \
              ''.join(start_date.split('-')) + '-' + ''.join(end_date.split('-')) + ')/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        return filter, dir

    def start_requests(self):
        print('Get urls from mongoDB...')
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        # collection_list = ['水柚']
        with open('C:/Users/W/Desktop/pic_keywords.txt', 'r', encoding='utf-8') as f:
            keywords = f.read()
            collection_list = keywords.split('\n')

        db = client[MONGODB_DBNAME]
        for date in self.date_list:
            for collection_name in collection_list:
                img_id = 0
                collection = db[collection_name]
                filter, dir = self.get_filter_dir(collection_name,start_date=date,end_date=date)
                results = collection.find(filter)
                for i in range(0, results.count()):
                    result = results[i]
                    for url in result['picture_list']:
                        img_id +=1
                        yield Request(url, meta={'dir': dir, 'img_id': str(img_id) } ,callback=self.parse_img)

    def parse_img(self,response):
        item = WeiboItem()
        item['img_url'] = response.url
        item['img_id'] = response.meta['img_id']
        item['img_path'] = response.meta['dir']+ item['img_id'] + response.url[-4:]
        yield item

class imgexcelSpider(scrapy.Spider):
    name = 'filepicture'
    start_urls = []

    def get_filter_dir(self,collection_name):
        today = datetime.datetime.now()
        last_sunday = str((today - timedelta(days=today.weekday() + 1)).date())
        last_saturday = str((today - timedelta(days=today.weekday() + 2)).date())
        filter = {'time': {'$gte': '2019-10-01', '$lte': '2019-10-03'}}
        # filter = {'time': {'$gte': last_saturday, '$lte': last_sunday}}
        dir = 'C:/Users/W/Desktop/img/' + MONGODB_DBNAME + '-' + collection_name + '(' + \
              ''.join(last_saturday.split('-')) + '-' + ''.join(last_sunday.split('-')) + ')/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        return filter, dir

    def start_requests(self):
        print('Get urls from file...')
        pattern = re.compile(r'[a-zA-Z]+://[^\s]*.cn\/[^\s]*\/[^\s]*[.jpg|.gif]')
        with open('C:/Users/W/Desktop/pic_keywords.txt', 'r', encoding='utf-8') as f:
            keywords = f.read()
            collection_list = keywords.split('\n')

        for collection_name in collection_list:
            img_id = 0
            filter, dir = self.get_filter_dir(collection_name)
            print('Collection name: {}'.format(collection_name))
            with open('C:/Users/W/Desktop/{}.txt'.format(collection_name), 'r', encoding='utf-8') as f:
                content = f.read()
                urls = re.findall(pattern, content)
                for url in urls:
                    img_id +=1
                    yield Request(url, meta={'dir': dir, 'img_id': str(img_id) } ,callback=self.parse_img)

    def parse_img(self,response):
        item = WeiboItem()
        item['img_url'] = response.url
        item['img_id'] = response.meta['img_id']
        item['img_path'] = response.meta['dir']+ item['img_id'] + response.url[-4:]
        yield item

class xhsimgSpider(scrapy.Spider):
    name = 'xhspicture'
    start_urls = []
    today = datetime.datetime.now()
    # last_saturday = str((today - timedelta(days=today.weekday() + 2)).date())
    # last_friday = str((today - timedelta(days=today.weekday() + 3)).date())
    # last_saturday = '2019-12-31'
    # last_friday = '2020-01-01'
    # date_list = [last_saturday,last_friday]
    item = XhsItem()

    def __init__(self,start_date=str((today - timedelta(days=today.weekday() + 2)).date()),end_date= str((today - timedelta(days=today.weekday() + 3)).date()),**kwargs):
        self.date_list = [start_date,end_date]


    def get_dir(self,keyword,start_date,end_date):
        dir = 'C:/Users/W/Desktop/img/' + 'xhs-' + keyword + '(' + \
              ''.join(start_date.split('-')) + '-' + ''.join(end_date.split('-')) + ')/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def start_requests(self):
        print('Get urls from MySQL...')
        keywords = ['b612', '轻颜', 'zepeto', 'faceu']

        unwanted_list = []
        with open('C:/Users/W/Desktop/filter_keywords.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                unwanted_list.append(line.strip())

        for date in self.date_list:
            for k in keywords:
                connect = pymysql.connect(
                    host=MYSQL_HOST,
                    db=MYSQL_DBNAME,
                    user=MYSQL_USER,
                    passwd=MYSQL_PASSWD,
                    use_unicode=True)
                cursor = connect.cursor()
                cursor.execute('select id,img_links,description,title,user_nickname from xhs where keywords = %s and pub_time = %s',(k,date))
                results = cursor.fetchall()
                for r in results:
                    unwanted = False
                    for u in unwanted_list:
                        description = r[2]
                        title = r[3]
                        user_nickname = r[4]
                        if description.find(u) != -1 or title.find(u) != -1 or user_nickname.find(u) != -1:
                            unwanted = True
                    if not unwanted:
                        url_list = r[1].split(',')
                        dir = self.get_dir(keyword=k,start_date=date,end_date=date)
                        for url in url_list:
                            yield Request(url=url,meta={'dir':dir},callback=self.parse)
                cursor.close()
                connect.close()

    def parse(self, response):
        url = response.url
        dir = response.meta['dir']
        self.item['img_url'] = url
        # item['img_id'] = id + '-' + str(img_num)
        self.item['img_id'] = url.split('/')[3].split('?')[0]
        self.item['img_name'] = self.item['img_id'] + '.png'
        self.item['img_path'] = dir + self.item['img_name']
        yield self.item

if __name__ == '__main__':
    execute('scrapy crawl xhspicture -a start_date=2019-12-03 -a end_date=2019-12-04'.split())
