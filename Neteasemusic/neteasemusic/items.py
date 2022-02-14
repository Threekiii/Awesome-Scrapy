# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteasemusicItem(scrapy.Item):
    # define the fields for your item here like:
    playlist_id = scrapy.Field()
    playlist_name = scrapy.Field()
    playlist_cat = scrapy.Field()
    playlist_tag = scrapy.Field()
    playlist_author = scrapy.Field()
    playlist_author_id = scrapy.Field()
    playlist_pubtime = scrapy.Field()
    playlist_songnum = scrapy.Field()
    playlist_desc = scrapy.Field()
    playlist_fav_count = scrapy.Field()
    playlist_share_count = scrapy.Field()
    playlist_comment_count = scrapy.Field()
    music_id = scrapy.Field()
    music_url = scrapy.Field()
    music_name = scrapy.Field()
    music_pubtime = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    album_id = scrapy.Field()
    album_name = scrapy.Field()
    lyric = scrapy.Field()
    music_crawltime = scrapy.Field()
    playlist_crawltime = scrapy.Field()
    pass

class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    comment_id = scrapy.Field()
    music_id = scrapy.Field()
    playlist_id = scrapy.Field()
    user_id = scrapy.Field()
    comment_content = scrapy.Field()
    comment_like_count = scrapy.Field()
