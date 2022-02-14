# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostcodespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    roads = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()


class RoadsspiderItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()
    roads = scrapy.Field()