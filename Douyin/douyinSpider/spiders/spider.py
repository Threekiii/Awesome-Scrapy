import scrapy
import copy
import re
import urllib.parse
import requests
import json
import os
import time
from jsonpath import jsonpath
from scrapy import Request
from scrapy.cmdline import execute
from douyinSpider.settings import DEFAULT_REQUEST_HEADERS,DOUYIN_KEYWORDS_DIR
from douyinSpider.functions import functions
from douyinSpider.items import DouyinItem

class douyinSpider(scrapy.Spider):
    name = 'douyin'
    start_urls = ['https://www.iesdouyin.com/share/challenge/']
    CSign = functions.Sign()
    CParams = functions.Params()
    item = DouyinItem()

    challenge_dict = {}
    with open(DOUYIN_KEYWORDS_DIR, 'r', encoding='utf-8') as f:
        challenge = f.readlines()
        for c in challenge:
            keyword = c.split('id:')[0].strip()
            id = c.split('id:')[1].strip()
            challenge_dict[keyword] = id

    def start_requests(self):
        for challenge in self.challenge_dict:
            challenge_id = self.challenge_dict[challenge]
            keywords = challenge
            url = self.start_urls[0] + challenge_id
            yield Request(url=url,callback=self.parse,meta={'keywords':keywords})

    def parse(self, response):
        url = response.url
        keywords = response.meta['keywords']
        id = re.findall('share/challenge/(\d+)', url)[0]
        hostname = urllib.parse.urlparse(url).hostname
        signature = self.CSign.generate_signature(str(id) + '9' + '0')
        params = self.CParams.get_params(id,signature)
        url = "https://%s/aweme/v1/challenge/aweme/" % hostname

        cursor, video_count = 2480, 0
        while True:
            if cursor:
                params['cursor'] = str(cursor)
                params['_signature'] = self.CSign.generate_signature(
                    str(id) + '9' + str(cursor))
                print(cursor)
            headers = copy.deepcopy(DEFAULT_REQUEST_HEADERS)
            headers['cookie'] = '_ga=GA1.2.1280899533.15586873031; _gid=GA1.2.2142818962.1559528881'
            res = requests.get(url, headers=headers, params=params)
            content = res.content.decode('utf-8')
            res = json.loads(content)
            if int(cursor) > 5000 :
                break
            if not res:
                break
            aweme_list = res.get('aweme_list', [])
            if aweme_list:
                for aweme in aweme_list:
                    video_count += 1
                if res.get('has_more'):
                    cursor = res.get('cursor')
                else:
                    break
                print(content)
                print(json.loads(content))
                print(json.dumps(json.loads(content), indent=4))
                data = json.loads(content)
                aweme_list = jsonpath(data, '$.aweme_list')[0]
                for aweme in aweme_list:
                    try:
                        self.item['hashtag']= jsonpath(aweme, '$.text_extra[*].hashtag_name')
                        for i in range(self.item['hashtag'].count('')):
                            self.item['hashtag'].remove('')
                        self.item['hashtag'] = ','.join(self.item['hashtag'])
                    except TypeError as e:
                        self.item['hashtag'] = ''
                    except AttributeError as e:
                        self.item['hashtag'] = ''

                    self.item['is_commerce'] = jsonpath(aweme, '$.text_extra[*].is_commerce')

                    if self.item['is_commerce'] != True and self.item['is_commerce'] != False:
                        self.item['is_commerce'] = jsonpath(aweme, '$.text_extra[*].is_commerce')[0]

                    create_timestamp = jsonpath(aweme, '$.create_time')[0]
                    self.item['keywords'] = keywords
                    self.item['pub_time'] = time.strftime("%Y-%m-%d", time.localtime(create_timestamp))
                    self.item['video_url'] = ','.join(jsonpath(aweme, '$.video.play_addr.uri'))
                    self.item['video_link'] = jsonpath(aweme, '$.video.play_addr.url_list')[0][0]
                    self.item['cover_link'] = jsonpath(aweme, '$.video.cover.url_list')[0][0]
                    self.item['cover_url'] = ','.join(jsonpath(aweme, '$.video.cover.uri'))
                    self.item['aweme_id'] = ','.join(jsonpath(aweme, '$.aweme_id'))
                    yield self.item
            else:
                cursor = str(int(cursor)+ 9)

if __name__ == '__main__':
    execute('scrapy crawl douyin'.split())