# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class bgmspiderItem(scrapy.Item):
    bgm_name = scrapy.Field()
    bgm_time = scrapy.Field()
    bgm_music = scrapy.Field()
    bgm_img = scrapy.Field()
    bgm_link = scrapy.Field()
    bgm_cat = scrapy.Field()
    bgm_tag = scrapy.Field()
    pass
