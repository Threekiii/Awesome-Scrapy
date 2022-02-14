# -*- coding: utf-8 -*-
import pymysql
from postcodeSpider.settings import *

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class PostcodespiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db = MYSQL_DBNAME,
            user = MYSQL_USER,
            passwd = MYSQL_PASSWD,
            use_unicode = True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'youbianku':
            self.cursor.execute(
                'insert ignore into postcode (postcode, address, province, city, roads, district) values (%s,%s,%s,%s,%s,%s)',
                (item['postcode'],item['address'],item['province'],item['city'],item['roads'],item['district'])
            )
        elif spider.name == 'empty':
            self.cursor.execute(
                'update postcode set address=%s, roads=%s where postcode = %s ',
                (item['address'],item['roads'],item['postcode'])
            )
        elif spider.name == 'multi':
            self.cursor.execute(
                'insert ignore into postcode (postcode, address, province, roads, district) values (%s,%s,%s,%s,%s)',
                (item['postcode'],item['address'],item['province'],item['roads'],'1')
            )
        elif spider.name == 'queshi':
            self.cursor.execute(
                'insert ignore into postcode_add (postcode, address, province, roads) values (%s,%s,%s,%s)',
                (item['postcode'],item['address'],item['province'],item['roads'])
            )
        self.connect.commit()
        return item
