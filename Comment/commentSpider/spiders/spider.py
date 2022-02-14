import scrapy
import requests
import re
import datetime
import json
import time
import hashlib
import pymysql
import json, execjs
from scrapy import Request
from urllib.parse import urlencode
from jsonpath import jsonpath
from commentSpider.settings import *
from commentSpider.items import *
from scrapy.cmdline import execute
from commentSpider.spiders.get_version import get_version


class huaweicommentSpider(scrapy.Spider):
    name = 'huaweicomments'
    item = HuaweiCommentspiderItem()

    def start_requests(self):
        for i in huawei_dict:
            app_name = i
            app_id = huawei_dict[i]
            base_url = 'http://a.vmall.com/uowap/index?method=internal.user.commenList3&reqPageNum={}&maxResults=10&appid={}&locale=zh_CN&LOCALE_NAME=zh_CN&version=10.0.0'
            url = base_url.format('1', app_id)
            r = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
            data = r.json()
            total_page = jsonpath(data, '$.totalPages')[0]
            for page in range(1, total_page + 1):
                print('{},page:{}'.format(app_name, page))
                base_url = 'http://a.vmall.com/uowap/index?method=internal.user.commenList3&reqPageNum={}&maxResults=10&appid={}&locale=zh_CN&LOCALE_NAME=zh_CN&version=10.0.0'
                url = base_url.format(page, app_id)
                yield Request(url=url, meta={'app_id': app_id,
                                             'app_name': app_name}, callback=self.parse)

    def parse(self, response):
        item = self.item
        url = response.url
        app_id = response.meta['app_id']
        app_name = response.meta['app_name']
        r = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        data = r.json()
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        comment_list = jsonpath(data, '$.list')[0]
        for comment in comment_list:
            item['id'] = jsonpath(comment, '$.commentId')[0]
            item['version'] = jsonpath(comment, '$.versionName')[0]
            item['rating'] = jsonpath(comment, '$.rating')[0]
            item['stars'] = jsonpath(comment, '$.stars')[0]
            item['pub_time'] = '-'.join(jsonpath(comment, '$.operTime')[0].split(' ')[0].split('/'))
            item['content'] = jsonpath(comment, '$.commentInfo')[0]
            item['user_name'] = jsonpath(comment, '$.nickName')[0]
            item['vote_count'] = jsonpath(comment, '$.approveCounts')[0]
            item['app_id'] = app_id
            item['app_name'] = app_name
            yield item


class applecommentSpider(scrapy.Spider):
    name = 'applecomments'
    item = AppleCommentspiderItem()

    def start_requests(self):
        for i in apple_dict:
            app_name = i
            app_id = apple_dict[i]
            page_num = 1
            while page_num < 300:
                print(page_num)
                base_url = "https://itunes.apple.com/cn/rss/customerreviews/page={}/id={}/sortby=mostrecent/json"
                url = base_url.format(page_num, app_id)
                page_num = page_num + 1
                yield Request(url=url, meta={'app_id': app_id,
                                             'app_name': app_name}, callback=self.parse)

    def parse(self, response):
        item = self.item
        item['app_id'] = response.meta['app_id']
        item['app_name'] = response.meta['app_name']
        url = response.url
        r = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        data = r.json()
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        item['updated'] = jsonpath(data, '$.feed.updated.label')[0]
        comments = jsonpath(data, '$.feed.entry')[0]
        for comment in comments:
            item['version'] = jsonpath(comment, '$.im:version.label')[0]
            item['rating'] = jsonpath(comment, '$.im:rating.label')[0]
            item['id'] = jsonpath(comment, '$.id.label')[0]
            item['title'] = jsonpath(comment, '$.title.label')[0]
            item['content'] = jsonpath(comment, '$.content.label')[0]
            item['vote_sum'] = jsonpath(comment, '$.im:voteSum.label')[0]
            item['vote_count'] = jsonpath(comment, '$.im:voteCount.label')[0]
            yield item


class xiaomicommentSpider(scrapy.Spider):
    name = 'xiaomicomments'
    item = XiaomoCommentspiderItem()

    def start_requests(self):
        page_num = 0
        while page_num < 400:
            # print(page_num)
            appid = '432169'
            # base_url = 'http://market.xiaomi.com/apm/comment/list/{}?clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN&la=zh&os=1576131580&page={}&sdk=22'
            base_url = 'http://app.market.xiaomi.com/apm/comment/list/{}?clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN&la=zh&os=1461822601&page={}&sdk=22'
            url = base_url.format(appid, page_num)
            page_num = page_num + 1
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = self.item
        url = response.url
        r = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        data = r.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        comments = jsonpath(data, '$.comments')[0]
        for comment in comments:
            item['id'] = jsonpath(comment, '$.commentId')[0]
            item['version'] = jsonpath(comment, '$.versionName')[0]
            timestamp = str(jsonpath(comment, '$.updateTime')[0])[:-3]
            item['time'] = time.strftime('%Y-%m-%d', time.localtime(int(timestamp)))
            item['user_name'] = jsonpath(comment, '$.nickname')[0]
            item['rating'] = jsonpath(comment, '$.pointValue')[0]
            item['content'] = jsonpath(comment, '$.commentValue')[0]
            item['country'] = jsonpath(comment, '$.country')[0]
            try:
                item['device'] = jsonpath(comment, '$.device')[0]
            except Exception:
                item['device'] = 'None'
            yield item


class yingyingbaocommentSpider(scrapy.Spider):
    name = 'yybcomments'
    item = YybCommentspiderItem()

    def start_requests(self):
        page_num = 0
        id = 0
        t = 0
        pkgname = 'com.campmobile.snowcamera'
        while True:
            if page_num == 0:
                print(page_num)
                base_url = 'http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_getcomment?type=myapp_all_comment&appid=1108066916&pkgname={}&pageNo=1&pageSize=10&platform=touch'
                url = base_url.format(pkgname)
                page_num += 1
            else:
                base_url = 'http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_getcomment?type=myapp_all_comment&appid=1108066916&pkgname={}&pageNo={}&pageSize=10&comment_contex=id%3D{}%2Ct%3D{}&platform=touch'
                url = base_url.format(pkgname, page_num, id, t)
                page_num += 1

            r = requests.get(url)
            rule_id_t = re.compile('"comment_contex":"id=(.*),t=(.*?)"')
            id_t = re.findall(rule_id_t, r.text)[0]
            id = id_t[0]
            t = id_t[1]
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = self.item
        url = response.url
        r = requests.get(url)
        print(r.text)
        rule_comments = re.compile('"comments":\[.*\]')
        data = re.findall(rule_comments, r.text)[0]
        data = json.loads('{%s}' % data)
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        comments = jsonpath(data, '$.comments[*]')
        for comment in comments:
            item['version_code'] = jsonpath(comment, '$.versionCode')[0]
            timestamp = jsonpath(comment, '$.createdTime')[0]
            item['time'] = time.strftime('%Y-%m-%d', time.localtime(int(timestamp)))
            item['user_name'] = jsonpath(comment, '$.name')[0]
            item['rating'] = jsonpath(comment, '$.score')[0]
            item['content'] = jsonpath(comment, '$.content')[0]
            item['brand'] = jsonpath(comment, '$.brand')[0]
            item['device'] = jsonpath(comment, '$.deviceInfo')[0]
            hash_data = item['content'] + item['time'] + item['user_name']
            item['id'] = hashlib.md5(hash_data.encode('utf8')).hexdigest()
            yield item


class qimaiapplecommentSpider(scrapy.Spider):
    name = 'qimaiapplecomments'
    start_urls = ['https://api.qimai.cn/rank/index']
    item = QimaiappleCommentspiderItem()

    def parse(self, response):
        with open('C:/Users/W/Desktop/CommentSpider/commentSpider/functions/encrypt.js', encoding='utf-8') as f:
            js = f.read()
        js = execjs.compile(js)
        base_url = 'https://api.qimai.cn/app/comment'
        for a in apple_dict:
            app_name = a
            app_id = apple_dict[a]
            for i in range(1,2):
                qimai_params = QIMAI_PARAMS
                if i == 1:
                    if 'page' in qimai_params:
                        qimai_params.pop('page')
                    input = [app_id, 'cn']
                    analysis = js.call('get_analysis', base_url, input)
                    qimai_params['appid'] = app_id
                    qimai_params['analysis'] = analysis
                    print(qimai_params)
                else:
                    input = [app_id, 'cn', i]
                    analysis = js.call('get_analysis', base_url, input)
                    qimai_params['appid'] = app_id
                    qimai_params['analysis'] = analysis
                    qimai_params['page'] = i

                r = requests.get(base_url,params=qimai_params,headers = QIMAI_HEADERS)
                # data = json.dumps(r.json(),indent=4,ensure_ascii=False)
                comments = jsonpath(r.json(),'$.appComments')[0]
                for comment in comments:
                    self.item['id'] = jsonpath(comment,'$.id')[0]
                    self.item['app_name'] = app_name
                    self.item['app_id'] = app_id
                    self.item['rating'] = jsonpath(comment,'$.rating')[0]
                    self.item['user_name'] = jsonpath(comment,'$.comment.name')[0]
                    self.item['title'] = jsonpath(comment,'$.comment.title')[0]
                    self.item['content'] = ''.join(jsonpath(comment,'$.comment.body'))
                    self.item['is_deleted'] = jsonpath(comment,'$.comment.delStatus')[0]
                    pub_time = jsonpath(comment,'$.date')[0]
                    self.item['pub_time'] = pub_time.split()[0]
                    self.item['version'] = get_version(pub_time,app_name)
                    yield self.item

if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'qimaiapplecomments'])
