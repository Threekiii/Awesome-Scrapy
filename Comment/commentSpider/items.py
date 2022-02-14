# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppleCommentspiderItem(scrapy.Item):
    id = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    version = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    vote_sum = scrapy.Field()
    vote_count = scrapy.Field()
    updated = scrapy.Field()


class XiaomoCommentspiderItem(scrapy.Item):
    id = scrapy.Field()
    version = scrapy.Field()
    time = scrapy.Field()
    user_name = scrapy.Field()
    rating = scrapy.Field()
    content = scrapy.Field()
    country = scrapy.Field()
    device = scrapy.Field()


class YybCommentspiderItem(scrapy.Item):
    id = scrapy.Field()
    version_code = scrapy.Field()
    time = scrapy.Field()
    user_name = scrapy.Field()
    rating = scrapy.Field()
    content = scrapy.Field()
    brand = scrapy.Field()
    device = scrapy.Field()

class HuaweiCommentspiderItem(scrapy.Item):
    id = scrapy.Field()
    version = scrapy.Field()
    rating = scrapy.Field()
    stars = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    user_name = scrapy.Field()
    vote_count = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()


class QimaiappleCommentspiderItem(scrapy.Item):
    id = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    version = scrapy.Field()
    pub_time = scrapy.Field()
    user_name = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    is_deleted = scrapy.Field()
    vote_up= scrapy.Field()
    vote_down = scrapy.Field()
