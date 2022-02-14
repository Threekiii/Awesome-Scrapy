# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from weibo.settings import DEFAULT_REQUEST_HEADERS, XHS_REQUEST_HEADERS
from io import BytesIO
from PIL import Image

class imgPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'weibopicture':
            r = requests.get(item['img_url'], headers = DEFAULT_REQUEST_HEADERS, timeout = 3)
            if r.status_code == 200:
                with open(item['img_path'],'ab') as f:
                    f.write(r.content)
                    f.close()
        elif spider.name == 'xhspicture':
            r = requests.get(item['img_url'], headers = XHS_REQUEST_HEADERS, timeout = 20)
            byte_stream = BytesIO(r.content)
            img = Image.open(byte_stream)
            print(item['img_path'])
            img.save(item['img_path'],'PNG')
        return item

