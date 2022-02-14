# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from douyinSpider import settings

class DouyinPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'douyin':
            self.cursor.execute(
                'insert ignore into douyin(aweme_id, keywords, hashtag, video_url, video_link, cover_url,cover_link,pub_time,is_commerce) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['aweme_id'],item['keywords'],item['hashtag'],item['video_url'],item['video_link'],item['cover_url'],item['cover_link'],item['pub_time'],item['is_commerce']))
            self.connect.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()