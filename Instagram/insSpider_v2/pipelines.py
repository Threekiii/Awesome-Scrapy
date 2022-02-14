# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from insSpider_v2 import settings
import re

class InsspiderV2Pipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if spider.name == 'inspagev2' or spider.name == 'insaddpagev2':
            self.cursor.execute('select * from ins where post_id = %s',(item['post_id']))
            result = self.cursor.fetchall()
            if len(result) == 0:
                pattern1 = re.compile(r'#\S+')
                pattern2 = re.compile(r'@\S+')
                item['hashtag'] = ','.join(pattern1.findall(item['content']))
                item['at'] = ','.join(pattern2.findall(item['content']))
                self.cursor.execute(
                    '''insert ignore into ins (post_id, post_url, post_link, user_id, type, keywords, is_video, img_description, cover_height, 
                    cover_width, cover_link, content, liked_count, comment_count, pub_time, at, hashtag) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (item['post_id'],item['post_url'],item['post_link'],item['user_id'],item['type'],item['keywords'],item['is_video'],
                     item['img_description'],item['cover_height'],item['cover_width'],item['cover_link'],item['content'],item['liked_count'],
                     item['comment_count'],item['pub_time'],item['at'],item['hashtag']))
            else:
                self.cursor.execute(
                    'update ins set liked_count = %s, comment_count = %s where post_id = %s',
                    (item['liked_count'],item['comment_count'],item['post_id'])
                )

            self.connect.commit()

        elif spider.name == 'inspostv2':
            self.cursor.execute(
                '''update ins set is_ad= %s ,user_name= %s, video_link= %s, video_duration= %s, video_view_count= %s, 
                 user_fullname= %s,img_links= %s where post_link = %s''',
                (item['is_ad'], item['user_name'], item['video_link'], item['video_duration'],  item['video_view_count'],
                 item['user_fullname'],item['img_links'],item['post_link']))
            self.connect.commit()

        elif spider.name == 'insuserv2':
            self.cursor.execute(
                '''update ins set user_biography= %s, user_following= %s, user_followed_by= %s where user_name= %s''',
                (item['user_biography'],item['user_following'], item['user_followed_by'],item['user_name']))
            self.connect.commit()

        elif spider.name == 'instranslatev2':
            self.cursor.execute(
                'update ins set machine_translation_language = %s where post_link = %s',(item['language'],item['post_link']))
            self.connect.commit()

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
