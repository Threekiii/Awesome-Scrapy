# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyinItem(scrapy.Item):
    keywords = scrapy.Field()
    hashtag = scrapy.Field()
    aweme_id = scrapy.Field()
    is_commerce = scrapy.Field()
    pub_time = scrapy.Field()
    video_url = scrapy.Field()
    video_link = scrapy.Field()
    cover_url = scrapy.Field()
    cover_link = scrapy.Field()
    pass
