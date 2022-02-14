# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApplespiderItem(scrapy.Item):
    app_name = scrapy.Field()
    app_link = scrapy.Field()
    subtitle = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    category = scrapy.Field()
    rank = scrapy.Field()
    rating = scrapy.Field()
    comment_count = scrapy.Field()
    time = scrapy.Field()
    publish_date = scrapy.Field()
    pass

class HuaweispiderItem(scrapy.Item):
    app_name = scrapy.Field()
    app_link = scrapy.Field()
    subtitle = scrapy.Field()
    category = scrapy.Field()
    rank = scrapy.Field()
    rating = scrapy.Field()
    comment_count = scrapy.Field()
    download_count = scrapy.Field()
    time = scrapy.Field()
    huawei_id = scrapy.Field()
    company_name = scrapy.Field()
    pass

class QimaispiderItem(scrapy.Item):
    app_name = scrapy.Field()
    apple_id = scrapy.Field()
    category = scrapy.Field()
    company_name = scrapy.Field()
    rank = scrapy.Field()
    rating = scrapy.Field()
    total_rank = scrapy.Field()
    last_release_date = scrapy.Field()
    comment_count = scrapy.Field()
    time = scrapy.Field()
    publish_date = scrapy.Field()
    subtitle = scrapy.Field()
    company_link = scrapy.Field()
    app_link = scrapy.Field()


