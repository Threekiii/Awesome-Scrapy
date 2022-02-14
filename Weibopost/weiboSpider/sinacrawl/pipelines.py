# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sinacrawl.settings import conn

class SinacrawlPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'weibo':
            db = conn.weibo
            my_set = db["{}".format(item["insert_name"])]
            item_dic = dict(item)
            my_set.save(item_dic)
        elif spider.name =='amuse':
            db = conn.amuse
            my_set = db["{}".format(item["insert_name"])]
            item_dic = dict(item)
            my_set.save(item_dic)
        elif spider.name == 'makeup':
            db = conn.makeup
            my_set = db["{}".format(item["insert_name"])]
            item_dic = dict(item)
            my_set.save(item_dic)
        return item
