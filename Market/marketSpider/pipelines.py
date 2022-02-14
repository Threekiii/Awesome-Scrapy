# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from marketSpider import settings


class MarketspiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'apple' or spider.name == 'addapple':
            if '年' in item['publish_date']:
                date = datetime.datetime.strptime(item['publish_date'], "%Y年%m月%d日")
                item['publish_date'] = str(date.date())

            self.cursor.execute(
                'insert ignore into apple_store (time, app_name, rank, rating, comment_count) values (%s,%s,%s,%s,%s)',
                (item['time'], item['app_name'], item['rank'], item['rating'], item['comment_count'])
            )
            self.cursor.execute(
                'insert ignore into apple_details (app_name, category, subtitle, company_name, company_link, app_link, publish_date) values (%s,%s,%s,%s,%s,%s,%s)',
                (item['app_name'], item['category'], item['subtitle'], item['company_name'], item['company_link'],
                 item['app_link'], item['publish_date'])
            )
            self.connect.commit()
        elif spider.name == 'huawei':
            # self.cursor.execute(
            #     'insert ignore into huawei_store (time, app_name, rank, rating, comment_count, download_count) values (%s,%s,%s,%s,%s,%s)',
            #     (item['time'], item['app_name'], item['rank'], item['rating'], item['comment_count'],
            #      item['download_count'])
            # )
            self.cursor.execute(
                'insert ignore into huawei_store (time, app_name, rank, download_count) values (%s,%s,%s,%s)',
                (item['time'], item['app_name'], item['rank'],item['download_count'])
            )
            self.cursor.execute(
                'insert ignore into huawei_details (app_name, category, subtitle, app_link, huawei_id) values (%s,%s,%s,%s,%s)',
                (item['app_name'], item['category'], item['subtitle'], item['app_link'], item['huawei_id'])
            )
            self.connect.commit()

        elif spider.name == 'qimaihuawei':
            self.cursor.execute(
                'update huawei_details set company_name = %s where app_name = %s',
                (item['company_name'], item['app_name']))
            self.cursor.execute(
                'update huawei_store set rating = %s, comment_count = %s where app_name = %s and time = %s',
                (item['rating'], item['comment_count'], item['app_name'],item['time']))
            self.connect.commit()

        elif spider.name == 'qimai':
            if '年' in item['last_release_date']:
                date = datetime.datetime.strptime(item['last_release_date'], "%Y年%m月%d日")
                item['last_release_date'] = str(date.date())

            self.cursor.execute('select * from apple_details where app_name = %s', (item['app_name']))
            result = self.cursor.fetchone()

            if result is None:
                self.cursor.execute(
                    'insert ignore into apple_store (time, app_name, rank,total_rank ,rating) values (%s,%s,%s,%s,%s)',
                    (item['time'], item['app_name'], item['rank'], item['total_rank'], item['rating'])
                )
                self.cursor.execute(
                    'insert ignore into apple_details (app_name, apple_id,category, company_name, last_release_date) values (%s,%s,%s,%s,%s)',
                    (item['app_name'], item['apple_id'], item['category'], item['company_name'],
                     item['last_release_date'])
                )
            else:
                self.cursor.execute(
                    'update apple_details set apple_id = %s, last_release_date = %s where app_name = %s',
                    (item['apple_id'], item['last_release_date'], item['app_name']))
                self.cursor.execute(
                    'update apple_store set total_rank = %s where app_name = %s and time = %s',
                                    (item['total_rank'], item['app_name'], item['time']))
            self.connect.commit()

        elif spider.name == 'qimaikeywords':
            if '年' in item['last_release_date']:
                date = datetime.datetime.strptime(item['last_release_date'], "%Y年%m月%d日")
                item['last_release_date'] = str(date.date())
            if '年' in item['publish_date']:
                date = datetime.datetime.strptime(item['publish_date'], "%Y年%m月%d日")
                item['publish_date'] = str(date.date())

            self.cursor.execute(
                'replace into apple_store(time, app_name, rank, total_rank ,rating, comment_count) values (%s,%s,%s,%s,%s,%s)',
                (item['time'], item['app_name'], item['rank'], item['total_rank'], item['rating'],
                 item['comment_count'])
            )
            self.cursor.execute(
                'replace into apple_details(app_name, apple_id, publish_date,last_release_date, category, subtitle, company_name, company_link, app_link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (item['app_name'], item['apple_id'], item['publish_date'], item['last_release_date'],
                 item['category'], item['subtitle'], item['company_name'],
                 item['company_link'], item['app_link'])
            )
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
