# -*- coding: utf-8 -*-
import scrapy
from sinacrawl.settings import WEIBO_LIST, MAKEUP_LIST, AMUSE_LIST, conn
from sinacrawl.items import SinacrawlItem
import json
import re
import time
import datetime
import random
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    need_names = WEIBO_LIST
    start_urls = []
    db = conn.weibo

    for get_name in need_names:       
        start_urls.append('https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page=1'.format(get_name))

    def get_time(self,t):
        localtime = datetime.datetime.timetuple(datetime.datetime.now())
        hour = localtime.tm_hour
        if (("小时前" in t) and (hour - int(t[:t.find("小时前")])) < 0) or ("昨天" in t):
            return (str(datetime.datetime.now() - datetime.timedelta(days=1))[:10])
        elif (("小时前" in t) and (hour - int(t[:t.find("小时前")])) >= 0) or ("分钟前" in t) or ("刚刚" in t):
            return (str(datetime.datetime.now())[:10])
        else:
            if len(t) < 6:
                m = t[-5:-3]
                d = t[-2:]
                return str(localtime.tm_year) + "-" + (str(m) + "-" + str(d))
            else:
                y = t[:-6]
                m = t[-5:-3]
                d = t[-2:]
                return str(y) + "-" + str(m) + "-" + str(d)

    def extract_data(self,info):
        collection_name = re.search("(q:)(.+)(\|ext)",info['itemid'])
        insert_name = collection_name.group(2)
        data = info['mblog']

        # 转换时间
        time = self.get_time(data['created_at'])

        id = data['id']
        url =  "https://m.weibo.cn/detail/" + id
        text = data['text']
        # 找出@引用及#话题，使用||进行标记
        pat = re.compile('<[^>]+>')
        text = pat.sub('|', text)
        pat1 = re.compile('#.*?#')
        hash_tag = re.findall(pat1, text)
        hash_tag_num = len(hash_tag)

        picture_num = len(data['pics']) if ('pics' in data) else 0
        picture_list = []
        if picture_num != 0:
            for i in data['pics']:
                picture_list.append(i['large']['url'])
        else:
            picture_list = []

        textlength = data['textLength'] if ('textLength' in data) else 0
        source = data['source']
        reposts_count = data["reposts_count"]
        comments_count = data["comments_count"]
        attitudes_count = data["attitudes_count"]
        pending_approval_count = data["pending_approval_count"]
        user_data = data['user']
        user_id = user_data['id']
        user_name = user_data['screen_name']
        user_profile = user_data['profile_url']
        user_verified = user_data['verified']
        user_verified_type = user_data['verified_type']
        user_description = user_data['description']
        user_gender = user_data['gender']
        user_followers_count = user_data['followers_count']
        user_follow_count = user_data['follow_count']
        return insert_name,id,time,text,hash_tag_num,hash_tag,picture_num,reposts_count,comments_count,attitudes_count,user_id,user_verified,user_verified_type,user_followers_count,user_follow_count,user_gender,user_description,user_profile,user_name,source,picture_list,textlength,url

    def page_parse(self, response):
        try:
            item = response.meta
            text = response.text
            reposts_count = re.search(r'("reposts_count": )(\d+)(,)', text).group(2)
            comments_count = re.search(r'("comments_count": )(\d+)(,)', text).group(2)
            attitudes_count = re.search(r'("attitudes_count": )(\d+)(,)', text).group(2)
            item["reposts_count"] = int(reposts_count)
            item["comments_count"] = int(comments_count)
            item["attitudes_count"] = int(attitudes_count)
            yield item
        except:
            time.sleep(17)
            yield scrapy.Request(
                item['url'],
                meta = item,
                callback=self.page_parse,
                dont_filter=True
            )

    def parse(self, response):
        print(response.url)
        if response.status == 200:
            page_num = re.search("(&page=)(\d+)(>)",str(response.request))
            num = int(page_num.group(2))
            num += 1
            insert_name = ""
            text_json = json.loads(response.text)
            if text_json['ok'] == 1:
                for info in text_json['data']['cards']:
                    li = ["insert_name","id", "time", "text", "hash_tag_num", "hash_tag", "picture_num", "reposts_count",
                          "comments_count", "attitudes_count", "user_id", "user_verified", "user_verified_type",
                          "user_followers_count", "user_follow_count", "user_gender", "user_description",
                          "user_profile", "user_name", "source", "picture_list","textlength","url"]

                    # 提取data.cards[""0""].card_group的数据
                    all_data = self.extract_data(info)

                    item = SinacrawlItem()
                    insert_name = all_data[0]
                    for i in li:
                        item[i] = all_data[li.index(i)]
                    item['_id']=int(all_data[1])

                    if (item['reposts_count'] != 10) and (item['comments_count'] != 10):
                        yield item
                    else:
                        print("The reposts_count and comments_count value 10, url: {}".format(item['url']))
                        yield scrapy.Request(
                            item['url'],
                            meta = item,
                            callback=self.page_parse,
                            dont_filter= True
                )
                yield scrapy.Request(
                    'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(insert_name,str(num)),
                    callback=self.parse,
                    dont_filter= True
                )
        else:
            print("新浪服务器宕机进入睡眠等待状态10s")
            time.sleep(10)
            yield scrapy.Request(str(response.request)[5:-1],
                    callback=self.parse,
                    dont_filter= True)

class MakeupSpider(scrapy.Spider):
    name = 'makeup'
    allowed_domains = ['m.weibo.cn']
    need_names = MAKEUP_LIST
    db = conn.makeup
    start_urls = []

    for get_name in need_names:
        start_urls.append('https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page=1'.format(get_name))

    def get_time(self,t):
        localtime = datetime.datetime.timetuple(datetime.datetime.now())
        hour = localtime.tm_hour
        if (("小时前" in t) and (hour - int(t[:t.find("小时前")])) < 0) or ("昨天" in t):
            return (str(datetime.datetime.now() - datetime.timedelta(days=1))[:10])
        elif (("小时前" in t) and (hour - int(t[:t.find("小时前")])) >= 0) or ("分钟前" in t) or ("刚刚" in t):
            return (str(datetime.datetime.now())[:10])
        else:
            if len(t) < 6:
                m = t[-5:-3]
                d = t[-2:]
                return str(localtime.tm_year) + "-" + (str(m) + "-" + str(d))
            else:
                y = t[:-6]
                m = t[-5:-3]
                d = t[-2:]
                return str(y) + "-" + str(m) + "-" + str(d)

    def extract_data(self,info):
        collection_name = re.search("(q:)(.+)(\|ext)",info['itemid'])
        insert_name = collection_name.group(2)
        data = info['mblog']

        # 转换时间
        time = self.get_time(data['created_at'])

        id = data['id']
        url =  "https://m.weibo.cn/detail/" + id
        text = data['text']
        # 找出@引用及#话题，使用||进行标记
        pat = re.compile('<[^>]+>')
        text = pat.sub('|', text)
        pat1 = re.compile('#.*?#')
        hash_tag = re.findall(pat1, text)
        hash_tag_num = len(hash_tag)

        picture_num = len(data['pics']) if ('pics' in data) else 0
        picture_list = []
        if picture_num != 0:
            for i in data['pics']:
                picture_list.append(i['large']['url'])
        else:
            picture_list = []

        textlength = data['textLength'] if ('textLength' in data) else 0
        source = data['source']
        reposts_count = data["reposts_count"]
        comments_count = data["comments_count"]
        attitudes_count = data["attitudes_count"]
        pending_approval_count = data["pending_approval_count"]
        user_data = data['user']
        user_id = user_data['id']
        user_name = user_data['screen_name']
        user_profile = user_data['profile_url']
        user_verified = user_data['verified']
        user_verified_type = user_data['verified_type']
        user_description = user_data['description']
        user_gender = user_data['gender']
        user_followers_count = user_data['followers_count']
        user_follow_count = user_data['follow_count']
        return insert_name,id,time,text,hash_tag_num,hash_tag,picture_num,reposts_count,comments_count,attitudes_count,user_id,user_verified,user_verified_type,user_followers_count,user_follow_count,user_gender,user_description,user_profile,user_name,source,picture_list,textlength,url

    def page_parse(self, response):
        try:
            item = response.meta
            text = response.text
            reposts_count = re.search(r'("reposts_count": )(\d+)(,)', text).group(2)
            comments_count = re.search(r'("comments_count": )(\d+)(,)', text).group(2)
            attitudes_count = re.search(r'("attitudes_count": )(\d+)(,)', text).group(2)
            item["reposts_count"] = int(reposts_count)
            item["comments_count"] = int(comments_count)
            item["attitudes_count"] = int(attitudes_count)
            yield item
        except:
            time.sleep(17)
            yield scrapy.Request(
                item['url'],
                meta = item,
                callback=self.page_parse,
                dont_filter=True
            )

    def parse(self, response):
        print(response.url)
        if response.status == 200:
            page_num = re.search("(&page=)(\d+)(>)",str(response.request))
            num = int(page_num.group(2))
            num += 1
            insert_name = ""
            text_json = json.loads(response.text)
            if text_json['ok'] == 1:
                for info in text_json['data']['cards']:
                    li = ["insert_name","id", "time", "text", "hash_tag_num", "hash_tag", "picture_num", "reposts_count",
                          "comments_count", "attitudes_count", "user_id", "user_verified", "user_verified_type",
                          "user_followers_count", "user_follow_count", "user_gender", "user_description",
                          "user_profile", "user_name", "source", "picture_list","textlength","url"]

                    # 提取data.cards[""0""].card_group的数据
                    all_data = self.extract_data(info)

                    item = SinacrawlItem()
                    insert_name = all_data[0]
                    for i in li:
                        item[i] = all_data[li.index(i)]
                    item['_id']=int(all_data[1])

                    if (item['reposts_count'] != 10) and (item['comments_count'] != 10):
                        yield item
                    else:
                        print("The reposts_count and comments_count value 10, url: {}".format(item['url']))
                        yield scrapy.Request(
                            item['url'],
                            meta = item,
                            callback=self.page_parse,
                            dont_filter= True
                )
                yield scrapy.Request(
                    'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(insert_name,str(num)),
                    callback=self.parse,
                    dont_filter= True
                )
        else:
            print("新浪服务器宕机进入睡眠等待状态10s")
            time.sleep(10)
            yield scrapy.Request(str(response.request)[5:-1],
                    callback=self.parse,
                    dont_filter= True)

class AmuseSpider(scrapy.Spider):
    name = 'amuse'
    allowed_domains = ['m.weibo.cn']
    need_names = AMUSE_LIST
    db = conn.amuse
    start_urls = []
    for get_name in need_names:
        start_urls.append('https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page=1'.format(get_name))

    def get_time(self,t):
        localtime = datetime.datetime.timetuple(datetime.datetime.now())
        hour = localtime.tm_hour
        if (("小时前" in t) and (hour - int(t[:t.find("小时前")])) < 0) or ("昨天" in t):
            return (str(datetime.datetime.now() - datetime.timedelta(days=1))[:10])
        elif (("小时前" in t) and (hour - int(t[:t.find("小时前")])) >= 0) or ("分钟前" in t) or ("刚刚" in t):
            return (str(datetime.datetime.now())[:10])
        else:
            if len(t) < 6:
                m = t[-5:-3]
                d = t[-2:]
                return str(localtime.tm_year) + "-" + (str(m) + "-" + str(d))
            else:
                y = t[:-6]
                m = t[-5:-3]
                d = t[-2:]
                return str(y) + "-" + str(m) + "-" + str(d)

    def extract_data(self,info):
        collection_name = re.search("(q:)(.+)(\|ext)",info['itemid'])
        insert_name = collection_name.group(2)
        data = info['mblog']

        # 转换时间
        time = self.get_time(data['created_at'])

        id = data['id']
        url =  "https://m.weibo.cn/detail/" + id
        text = data['text']
        # 找出@引用及#话题，使用||进行标记
        pat = re.compile('<[^>]+>')
        text = pat.sub('|', text)
        pat1 = re.compile('#.*?#')
        hash_tag = re.findall(pat1, text)
        hash_tag_num = len(hash_tag)

        picture_num = len(data['pics']) if ('pics' in data) else 0
        picture_list = []
        if picture_num != 0:
            for i in data['pics']:
                picture_list.append(i['large']['url'])
        else:
            picture_list = []

        textlength = data['textLength'] if ('textLength' in data) else 0
        source = data['source']
        reposts_count = data["reposts_count"]
        comments_count = data["comments_count"]
        attitudes_count = data["attitudes_count"]
        pending_approval_count = data["pending_approval_count"]
        user_data = data['user']
        user_id = user_data['id']
        user_name = user_data['screen_name']
        user_profile = user_data['profile_url']
        user_verified = user_data['verified']
        user_verified_type = user_data['verified_type']
        user_description = user_data['description']
        user_gender = user_data['gender']
        user_followers_count = user_data['followers_count']
        user_follow_count = user_data['follow_count']
        return insert_name,id,time,text,hash_tag_num,hash_tag,picture_num,reposts_count,comments_count,attitudes_count,user_id,user_verified,user_verified_type,user_followers_count,user_follow_count,user_gender,user_description,user_profile,user_name,source,picture_list,textlength,url

    def page_parse(self, response):
        try:
            item = response.meta
            text = response.text
            reposts_count = re.search(r'("reposts_count": )(\d+)(,)', text).group(2)
            comments_count = re.search(r'("comments_count": )(\d+)(,)', text).group(2)
            attitudes_count = re.search(r'("attitudes_count": )(\d+)(,)', text).group(2)
            item["reposts_count"] = int(reposts_count)
            item["comments_count"] = int(comments_count)
            item["attitudes_count"] = int(attitudes_count)
            yield item
        except:
            time.sleep(17)
            yield scrapy.Request(
                item['url'],
                meta = item,
                callback=self.page_parse,
                dont_filter=True
            )

    def parse(self, response):
        print(response.url)
        if response.status == 200:
            page_num = re.search("(&page=)(\d+)(>)",str(response.request))
            num = int(page_num.group(2))
            num += 1
            insert_name = ""
            text_json = json.loads(response.text)
            if text_json['ok'] == 1:
                for info in text_json['data']['cards']:
                    li = ["insert_name","id", "time", "text", "hash_tag_num", "hash_tag", "picture_num", "reposts_count",
                          "comments_count", "attitudes_count", "user_id", "user_verified", "user_verified_type",
                          "user_followers_count", "user_follow_count", "user_gender", "user_description",
                          "user_profile", "user_name", "source", "picture_list","textlength","url"]

                    # 提取data.cards[""0""].card_group的数据
                    all_data = self.extract_data(info)

                    item = SinacrawlItem()
                    insert_name = all_data[0]
                    for i in li:
                        item[i] = all_data[li.index(i)]
                    item['_id']=int(all_data[1])

                    if (item['reposts_count'] != 10) and (item['comments_count'] != 10):
                        yield item
                    else:
                        print("The reposts_count and comments_count value 10, url: {}".format(item['url']))
                        yield scrapy.Request(
                            item['url'],
                            meta = item,
                            callback=self.page_parse,
                            dont_filter= True
                )
                yield scrapy.Request(
                    'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(insert_name,str(num)),
                    callback=self.parse,
                    dont_filter= True
                )
        else:
            print("新浪服务器宕机进入睡眠等待状态10s")
            time.sleep(10)
            yield scrapy.Request(str(response.request)[5:-1],
                    callback=self.parse,
                    dont_filter= True)