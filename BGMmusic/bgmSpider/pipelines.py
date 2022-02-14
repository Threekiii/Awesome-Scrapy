# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from bgmSpider import settings
import pymysql

class BgmspiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'bgm':
            self.cursor.execute(
                'insert ignore into bgm (bgm_name,bgm_cat,bgm_tag,bgm_time,bgm_music,bgm_link,bgm_img) values (%s,%s,%s,%s,%s,%s,%s)',
                (item['bgm_name'],item['bgm_cat'],item['bgm_tag'],item['bgm_time'],item['bgm_music'],
                 item['bgm_link'],item['bgm_img']))
            self.connect.commit()
        return item
