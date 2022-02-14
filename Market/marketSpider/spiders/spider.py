import scrapy
import requests
import re
import datetime
import json, execjs
import time
import pymysql
from lxml import etree
from jsonpath import jsonpath
from scrapy.cmdline import execute
from scrapy import Request
from marketSpider import settings
from marketSpider.settings import DEFAULT_REQUEST_HEADERS, QIMAI_PARAMS, QIMAI_REQUEST_HEADERS,HUAWEI_PARAMS
from marketSpider.items import ApplespiderItem, HuaweispiderItem, QimaispiderItem


class appleSpider(scrapy.Spider):
    name = 'apple'
    start_urls = ['https://apps.apple.com/cn/genre/ios-%E6%91%84%E5%BD%B1%E4%B8%8E%E5%BD%95%E5%83%8F/id6008']
    item = ApplespiderItem()

    def parse(self, response):
        r = requests.get(response.url, headers=DEFAULT_REQUEST_HEADERS)
        sel = etree.HTML(r.text)
        apps = sel.xpath('//*[@id="selectedcontent"]/div/ul/li')
        for app in apps:
            app_name = app.xpath('a/text()')[0]
            app_link = app.xpath('a/@href')[0]
            yield Request(url=app_link, meta={'app_name': app_name}, callback=self.parse_app)

    def parse_app(self, response):
        try:
            self.item['app_name'] = response.meta['app_name']
            self.item['app_link'] = response.url
            r = requests.get(response.url, headers=DEFAULT_REQUEST_HEADERS)
            sel = etree.HTML(r.text)
            self.item['subtitle'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2[1]/text()')[0]
            self.item['company_name'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2/a/text()')[0]
            self.item['company_link'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2/a/@href')[0]
            category = sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[1]/ul/li/text()')[0].strip()
            pattern = re.compile(r'[“](.*?)[”]')
            if len(category) == 0:
                self.item['category'] = ''
            else:
                self.item['category'] = re.findall(pattern, category)[0]
            self.item['rank'] = ''.join(
                re.findall('\d+', sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[1]/ul/li/text()')[0].strip()))
            json_content = json.loads(sel.xpath('//html/head/script/text()')[0])
            self.item['comment_count'] = json_content['aggregateRating']['reviewCount']
            self.item['publish_date'] = json_content['datePublished']
            self.item['rating'] = \
                sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[2]/ul/li/figure/@aria-label')[0].split('（')[0]
            self.item['time'] = str(datetime.date.today())
            yield self.item

        except IndexError as e:
            print(e)


class addappleSpider(scrapy.Spider):
    name = 'addapple'
    start_urls = ['https://apps.apple.com/cn/app/']
    item = ApplespiderItem()

    def start_requests(self):
        with open('C:/Users/W/Desktop/marketSpider/marketSpider/functions/apple_keywords.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                id = line.split(' id:')[-1]
                app_name = line.split(' id:')[0]
                url = self.start_urls[0] + app_name + '/id' + id
                yield Request(url=url, callback=self.parse, meta={'app_name': app_name})

    def parse(self, response):
        r = requests.get(response.url, headers=DEFAULT_REQUEST_HEADERS)
        sel = etree.HTML(r.text)
        self.item['app_name'] = response.meta['app_name']
        self.item['app_link'] = response.url
        self.item['subtitle'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2[1]/text()')[0]

        self.item['company_name'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2/a/text()')[0]
        self.item['company_link'] = sel.xpath('//*[@class="l-row"]/div[2]/header/h2/a/@href')[0]

        category = sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[1]/ul/li/text()')[0].strip()
        pattern = re.compile(r'[“](.*?)[”]')
        if len(category) == 0:
            self.item['category'] = ''
        else:
            self.item['category'] = re.findall(pattern, category)[0]
        self.item['rank'] = ''.join(
            re.findall('\d+', sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[1]/ul/li/text()')[0].strip()))
        json_content = json.loads(sel.xpath('//html/head/script/text()')[0])
        self.item['comment_count'] = json_content['aggregateRating']['reviewCount']
        self.item['publish_date'] = json_content['datePublished']
        self.item['rating'] = \
            sel.xpath('//*[@class="l-row"]/div[2]/header/ul[1]/li[2]/ul/li/figure/@aria-label')[0].split('（')[0]
        self.item['time'] = str(datetime.date.today())
        yield self.item


class huaweiSpider(scrapy.Spider):
    name = 'huawei'
    start_urls = [
        'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri=thirdcatdetail%7C33_ALL_1&maxResults=100&reqPageNum=1']
    item = HuaweispiderItem()

    def parse(self, response):
        r = requests.get(response.url)
        js = json.loads(r.text)
        datalist = jsonpath(js, '$..dataList[*]')
        for i, element in enumerate(datalist):
            rank = i + 1
            app_id = jsonpath(element, '$.appid')[0]
            subtitle = jsonpath(element, '$.memo')[0]
            app_name = jsonpath(element, '$.name')[0]
            category = jsonpath(element, '$.tagName')[0]
            download_count = jsonpath(element, '$.downCountDesc')[0]
            download_count = download_count.split('次')[0].replace(',', '')
            # app_link = 'https://a.vmall.com/uowap/index?method=internal.user.commenList3&serviceType=13&reqPageNum=1&maxResults=5&appid={}&locale=zh_CN&LOCALE_NAME=zh_CN&version=10.0.0'.format(
            #     app_id)
            app_link = 'http://a.vmall.com/uowap/index.html#/detailApp/{}'.format(
                app_id)

            # 华为comment接口2019.11.25失效
            self.item['rank'] = rank
            self.item['huawei_id'] = app_id
            self.item['subtitle'] = subtitle
            self.item['app_name'] = app_name
            self.item['category'] = category
            self.item['download_count'] = download_count
            self.item['time'] = str(datetime.date.today())
            self.item['app_link'] = response.url
            yield self.item

            # yield Request(url=app_link, meta={
            #     'rank': rank,
            #     'subtitle': subtitle,
            #     'app_name': app_name,
            #     'category': category,
            #     'download_count': download_count
            # }, callback=self.parse_app)

    # def parse_app(self, response):
    #     r = requests.get(response.url)
    #     js = json.loads(r.text)
    #     print(r.text)
    #     self.item['rank'] = response.meta['rank']
    #     self.item['subtitle'] = response.meta['subtitle']
    #     self.item['app_name'] = response.meta['app_name']
    #     self.item['category'] = response.meta['category']
    #     self.item['download_count'] = response.meta['download_count']
    #
    #     self.item['app_link'] = response.url
    #     self.item['rating'] = jsonpath(js, '$.stars')[0]
    #     self.item['comment_count'] = jsonpath(js, '$.count')[0]
    #     self.item['time'] = str(datetime.date.today())
    #     yield self.item

class qimaihuaweiSpider(scrapy.Spider):
    name = 'qimaihuawei'
    start_urls = ['https://api.qimai.cn/rank/marketRank']
    item = HuaweispiderItem()

    def parse(self, response):
        today = str(datetime.date.today())
        with open('C:/Users/W/Desktop/marketSpider/marketSpider/functions/encrypt.js', encoding='utf-8') as f:
            js = f.read()
        js = execjs.compile(js)

        input = []
        params = HUAWEI_PARAMS
        params['date'] = today
        if 'analysis' in params:
            params.pop('analysis')

        for item in params:
            input.append(params[item])
        analysis = js.call('get_analysis', response.url, input)
        params['analysis'] = analysis
        time.sleep(1)
        r = requests.get(response.url, params=params, headers=QIMAI_REQUEST_HEADERS)
        data = json.loads(r.text, encoding='utf-8')
        print(json.dumps(data, sort_keys=True, indent=2))
        app_list = jsonpath(data, '$.rankInfo[*]')
        for element in app_list:
            self.item['app_name'] = jsonpath(element, '$.appInfo.appName')[0].split('-')[0].strip()
            self.item['comment_count'] = jsonpath(element, '$.appInfo.app_comment_count')[0]
            self.item['rating'] = jsonpath(element, '$.appInfo.app_comment_score')[0]
            self.item['company_name'] = jsonpath(element, '$.appInfo.publisher')[0]
            self.item['time'] = params['date']
            yield self.item

class qimaiSpider(scrapy.Spider):
    name = 'qimai'
    start_urls = ['https://api.qimai.cn/rank/index']
    page_list = ['1','2','3','4']
    item = QimaispiderItem()

    def parse(self, response):
        today = str(datetime.date.today())
        with open('C:/Users/W/Desktop/marketSpider/marketSpider/functions/encrypt.js', encoding='utf-8') as f:
            js = f.read()
        js = execjs.compile(js)

        for i in self.page_list:
            input = []
            params = QIMAI_PARAMS
            params['date'] = today
            params['page'] = i
            if 'analysis' in params:
                params.pop('analysis')

            for item in params:
                input.append(params[item])
            analysis = js.call('get_analysis', response.url, input)
            params['analysis'] = analysis
            time.sleep(1)
            r = requests.get(response.url, params=params, headers=QIMAI_REQUEST_HEADERS)
            data = json.loads(r.text, encoding='utf-8')
            app_list = jsonpath(data, '$.rankInfo[*]')
            for element in app_list:
                self.item['apple_id'] = jsonpath(element, '$.appInfo.appId')[0]
                self.item['app_name'] = jsonpath(element, '$.appInfo.appName')[0]
                self.item['last_release_date'] = jsonpath(element, '$.lastReleaseTime')[0]
                self.item['rank'] = jsonpath(element, '$.rank_c.ranking')[0]
                self.item['total_rank'] = jsonpath(element, '$.rank_b.ranking')[0]
                self.item['company_name'] = jsonpath(element, '$.appInfo.publisher')[0]
                self.item['category'] = jsonpath(element, '$.rank_c.genre')[0]
                self.item['rating'] = jsonpath(element, '$.comment.rating')[0]
                self.item['time'] = str(datetime.date.today())
                yield self.item

class qimaikeywordsSpider(scrapy.Spider):
    name = 'qimaikeywords'
    start_urls = ['https://api.qimai.cn/app/appinfo']
    item = QimaispiderItem()
    id_dic = {}
    with open('C:/Users/W/Desktop/marketSpider/marketSpider/functions/apple_keywords.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            id = line.split(' id:')[-1]
            app_name = line.split(' id:')[0]
            id_dic[app_name] = id

    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        use_unicode=True)
    cursor = connect.cursor()

    def parse(self, response):
        with open('C:/Users/W/Desktop/marketSpider/marketSpider/functions/encrypt.js', encoding='utf-8') as f:
            js = f.read()
        js = execjs.compile(js)
        # print(self.id_dic)
        for app_name in self.id_dic:
            id = self.id_dic[app_name]
            self.item['time'] = str(datetime.date.today())
            self.cursor.execute('select publish_date,subtitle,company_link,app_link,app_name from apple_details where app_name = %s',[app_name])
            result = self.cursor.fetchone()
            print(result)
            print('***********')
            if result is not None:
                self.item['publish_date'] = result[0]
                self.item['subtitle'] = result[1]
                self.item['company_link'] = result[2]
                self.item['app_link'] = result[3]
            else:
                self.item['publish_date'] = ''
                self.item['subtitle'] = ''
                self.item['company_link'] = ''
                self.item['app_link'] = ''

            self.cursor.execute('select * from apple_store where app_name = %s and time = %s', [app_name,self.item['time']])
            result = self.cursor.fetchone()
            print(result)
            if result is not None:
                self.item['comment_count'] = result[5]
            else:
                self.item['comment_count'] = None

            if result is None or result[3] is None:
                input = []
                params = {}
                params['appid'] = id
                params['country'] = 'cn'
                if 'analysis' in params:
                    params.pop('analysis')

                for item in params:
                    input.append(params[item])
                analysis = js.call('get_analysis', response.url, input)
                params['analysis'] = analysis
                r = requests.get(response.url, params=params, headers=QIMAI_REQUEST_HEADERS)
                print(r.text)
                data = json.loads(r.text, encoding='utf-8')
                self.item['apple_id'] = jsonpath(data, '$.appInfo.appid')[0]
                self.item['app_name'] = app_name
                self.item['last_release_date'] = jsonpath(data, '$.appInfo.version')[0]
                self.item['company_name'] = jsonpath(data, '$.appInfo.company.name')[0]
                self.item['category'] = jsonpath(data, '$.appInfo.genre.name')[0]

                input = []
                params = {}
                url = 'https://api.qimai.cn/app/commentRate'
                params['appid'] = id
                params['country'] = 'cn'
                if 'analysis' in params:
                    params.pop('analysis')

                for item in params:
                    input.append(params[item])
                analysis = js.call('get_analysis', url, input)
                params['analysis'] = analysis
                r = requests.get(url, params=params, headers=QIMAI_REQUEST_HEADERS)
                data = json.loads(r.text, encoding='utf-8')
                self.item['rating'] = jsonpath(data, '$.rateInfo.all.ratingAverage')[0]

                input = []
                params = {}
                url = 'https://api.qimai.cn/app/rank'
                params['appid'] = id
                params['country'] = 'cn'
                params['brand'] = 'free'
                if 'analysis' in params:
                    params.pop('analysis')
                for item in params:
                    input.append(params[item])
                analysis = js.call('get_analysis', url, input)
                params['analysis'] = analysis
                r = requests.get(url, params=params, headers=QIMAI_REQUEST_HEADERS)
                data = json.loads(r.text, encoding='utf-8')
                self.item['rank'] = jsonpath(data, '$.realTimeRank[1][2].ranking')[0]
                self.item['total_rank'] = jsonpath(data, '$.realTimeRank[1][3].ranking')[0]
                yield self.item


if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'qimaihuawei'])
