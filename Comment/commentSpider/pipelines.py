# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from commentSpider import settings

class CommentspiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'applecomments':
            self.cursor.execute(
                'insert ignore into comments_apple (id,app_id, app_name,version,rating,updated,title,content,vote_sum,vote_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['id'],item['app_id'],item['app_name'],item['version'],item['rating'],item['updated'],item['title'],item['content'],item['vote_sum'],item['vote_count'])
            )
            self.connect.commit()
        elif spider.name == 'xiaomicomments':
            self.cursor.execute(
                'insert ignore into comments_xiaomi (id,version,time,user_name,rating,content,country,device) values (%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['id'],item['version'],item['time'],item['user_name'],item['rating'],item['content'],item['country'],item['device'])
            )
            self.connect.commit()
        elif spider.name == 'yybcomments':
            self.cursor.execute(
                'insert ignore into comments_yyb (id,version_code,time,user_name,rating,content,brand,device) values (%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['id'],item['version_code'],item['time'],item['user_name'],item['rating'],item['content'],item['brand'],item['device'])
            )
            self.connect.commit()
        elif spider.name == 'huaweicomments':
            self.cursor.execute(
                'insert ignore into comments_huawei (id,version,rating,stars,pub_time,content,user_name,vote_count,app_id,app_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['id'],item['version'],item['rating'],item['stars'],item['pub_time'],item['content'],item['user_name'],item['vote_count'],item['app_id'],item['app_name'])
            )
            self.connect.commit()
        elif spider.name == 'qimaiapplecomments':
            self.cursor.execute(
                '''
                insert ignore into comments_apple_qimai (id, app_name,app_id,version,pub_time,user_name,rating,title,content,is_deleted) 
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                (item['id'],item['app_name'],item['app_id'],item['version'],item['pub_time'],item['user_name'],item['rating'],item['title'],item['content'],item['is_deleted'])

            )
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
