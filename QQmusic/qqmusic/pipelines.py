# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from qqmusic import settings

class QqmusicPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if 'comment_id' not in item:
            self.cursor.execute(
                '''insert ignore into playlist (playlist_id, playlist_name, playlist_cat, playlist_tag, playlist_tagids,
                 playlist_author, playlist_author_qq, playlist_pubtime, playlist_songids, playlist_songnum, playlist_desc,
                 playlist_listen_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ''',
                (item['playlist_id'], item['playlist_name'], item['playlist_cat'], item['playlist_tag'],
                 item['playlist_tagids'],
                 item['playlist_author'], item['playlist_author_qq'], item['playlist_pubtime'],
                 item['playlist_songids'],
                 item['playlist_songnum'], item['playlist_desc'], item['playlist_listen_count']))

            self.cursor.execute(
                '''insert ignore into music(music_id, playlist_id, music_mid, music_media_mid, music_mv_mid, music_name,
                music_songtype, music_genre, music_language, music_pubtime, artist_id, artist_mid, artist_name, album_id)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (
                item['music_id'], item['playlist_id'], item['music_mid'], item['music_media_mid'], item['music_mv_mid'],
                item['music_name'], item['music_songtype'], item['music_genre'], item['music_language'],
                item['music_pubtime'],
                item['artist_id'], item['artist_mid'], item['artist_name'], item['album_id'])
            )

            self.cursor.execute(
                '''insert ignore into album(album_id, album_mid, album_name, album_subtitle) values (%s,%s,%s,%s)''',
                (item['album_id'],item['album_mid'],item['album_name'],item['album_subtitle'])
            )

            self.cursor.execute(
                '''insert ignore into lyric(music_id, music_name, lyric) values (%s,%s,%s)''',
                (item['music_id'],item['music_name'],item['lyric'])
            )
        else:
            self.cursor.execute(
                '''insert ignore into comment(music_id, comment_id, is_hot, is_hot_cmt, is_medal, is_stick, is_praise, user_uin, user_nickname,
                user_avatar_link, content, pub_time, liked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (item['music_id'],item['comment_id'],item['is_hot'],item['is_hot_cmt'],item['is_medal'],item['is_stick'],item['is_praise'],
                 item['user_uin'],item['user_nickname'],item['user_avatar_link'],item['content'],item['pub_time'],item['liked'])
            )

        self.connect.commit()
        return item



