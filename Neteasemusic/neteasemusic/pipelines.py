# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from neteasemusic import settings

class NeteasemusicPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if 'playlist_name' in item:
            self.cursor.execute(
                '''insert ignore into playlist (playlist_id, playlist_name, playlist_cat, playlist_tag,
                 playlist_author, playlist_author_id, playlist_pubtime,  playlist_songnum, playlist_desc,
                 playlist_fav_count,playlist_share_count,playlist_comment_count,playlist_crawltime) 
                 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ''',
                (item['playlist_id'], item['playlist_name'], item['playlist_cat'], item['playlist_tag'],
                 item['playlist_author'], item['playlist_author_id'], item['playlist_pubtime'],
                 item['playlist_songnum'], item['playlist_desc'], item['playlist_fav_count'],
                 item['playlist_share_count'],item['playlist_comment_count'],item['playlist_crawltime']))

        if 'music_name' in item:
            self.cursor.execute(
                '''insert ignore into music(music_id, playlist_id,  music_name, artist_id, artist_name, 
                album_id,album_name,music_crawltime) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                (
                    item['music_id'], item['playlist_id'], item['music_name'],
                    item['artist_id'], item['artist_name'], item['album_id'],
                    item['album_name'],item['music_crawltime'])
            )

        if 'lyric' in item:
            self.cursor.execute(
                '''insert ignore into lyric(music_id, music_name, lyric) values (%s,%s,%s)''',
                (item['music_id'], item['music_name'], item['lyric'])
            )

        if item['comment_id']:
            self.cursor.execute(
                """insert ignore into comment(comment_id,music_id,playlist_id,user_id,comment_content,
                comment_like_count) values(%s,%s,%s,%s,%s,%s)""",
                (item['comment_id'],item['music_id'],item['playlist_id'],item['user_id'],
                 item['comment_content'],item['comment_like_count'])
            )

        self.connect.commit()
        return item
