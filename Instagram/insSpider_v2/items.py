# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InsspiderV2Item(scrapy.Item):
    post_id = scrapy.Field()
    post_url = scrapy.Field()
    post_link = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    type = scrapy.Field()
    keywords = scrapy.Field()
    is_video = scrapy.Field()
    is_ad = scrapy.Field()
    img_description = scrapy.Field()
    cover_height = scrapy.Field()
    cover_width = scrapy.Field()
    cover_link = scrapy.Field()
    video_link = scrapy.Field()
    img_links = scrapy.Field()
    video_duration = scrapy.Field()
    content = scrapy.Field()
    liked_count = scrapy.Field()
    comment_count = scrapy.Field()
    video_view_count = scrapy.Field()
    pub_time = scrapy.Field()
    user_biography = scrapy.Field()
    user_following = scrapy.Field()
    user_followed_by = scrapy.Field()
    user_fullname = scrapy.Field()
    at = scrapy.Field()
    hashtag = scrapy.Field()
    pass

class InstranslateItem(scrapy.Item):
    language = scrapy.Field()
    post_link = scrapy.Field()