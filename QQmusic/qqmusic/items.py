# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqmusicItem(scrapy.Item):
    playlist_pubtime = scrapy.Field()
    playlist_author = scrapy.Field()
    playlist_author_qq = scrapy.Field()
    playlist_id = scrapy.Field()
    playlist_name = scrapy.Field()
    playlist_listen_count = scrapy.Field()
    playlist_desc = scrapy.Field()
    playlist_songids = scrapy.Field()
    playlist_songnum = scrapy.Field()
    playlist_cat = scrapy.Field()
    playlist_tag = scrapy.Field()
    playlist_tagids = scrapy.Field()
    album_id = scrapy.Field()
    album_mid = scrapy.Field()
    album_name = scrapy.Field()
    album_subtitle = scrapy.Field()
    music_media_mid = scrapy.Field()
    music_id = scrapy.Field()
    music_mid = scrapy.Field()
    music_mv_mid = scrapy.Field()
    music_name = scrapy.Field()
    music_genre = scrapy.Field()
    music_language = scrapy.Field()
    artist = scrapy.Field()
    artist_id = scrapy.Field()
    artist_mid = scrapy.Field()
    artist_name = scrapy.Field()
    music_songtype = scrapy.Field()
    music_pubtime = scrapy.Field()
    lyric = scrapy.Field()
    pass


class CommentItem(scrapy.Item):
    music_id = scrapy.Field()
    comment_id = scrapy.Field()
    is_hot = scrapy.Field()
    is_hot_cmt = scrapy.Field()
    is_medal = scrapy.Field()
    is_stick = scrapy.Field()
    is_praise = scrapy.Field()
    user_uin = scrapy.Field()
    user_nickname = scrapy.Field()
    user_avatar_link = scrapy.Field()
    content = scrapy.Field()
    pub_time = scrapy.Field()
    liked = scrapy.Field()
    pass
