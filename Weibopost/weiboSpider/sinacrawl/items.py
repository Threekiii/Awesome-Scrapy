# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinacrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    insert_name = scrapy.Field()
    id = scrapy.Field()
    time = scrapy.Field()
    text = scrapy.Field()
    textlength = scrapy.Field()
    picture_num = scrapy.Field()
    picture_list = scrapy.Field()
    hash_tag_num = scrapy.Field()
    hash_tag = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    pending_approval_count = scrapy.Field()
    user_id  = scrapy.Field()
    user_gender = scrapy.Field()
    user_name = scrapy.Field()
    source = scrapy.Field()
    user_description = scrapy.Field()
    user_verified = scrapy.Field()
    user_verified_type = scrapy.Field()
    user_follow_count = scrapy.Field()
    user_followers_count = scrapy.Field()
    user_profile = scrapy.Field()
    url = scrapy.Field()
