import sys
import os
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
ffpath = os.path.abspath(os.path.join(fpath,".."))
sys.path.append(ffpath)

import scrapy
import datetime
import requests
from scrapy import Request
from scrapy.cmdline import execute
from lxml import etree
from postcodeSpider.settings import DEFAULT_REQUEST_HEADERS
from postcodeSpider.items import PostcodespiderItem

class postcodeSpider(scrapy.Spider):
    name = 'youbianku'
    start_urls = 'https://www.youbianku.com'
    headers = DEFAULT_REQUEST_HEADERS
    municipality_list = ['北京','上海','天津','重庆']
    hkmctw_list = ['香港','澳门','台湾']

    # province
    def start_requests(self):
        url = 'https://www.youbianku.com/%E6%8C%89%E7%9C%81%E6%9F%A5%E8%AF%A2'
        r = requests.get(url,headers=self.headers)
        content = etree.HTML(r.text)
        province = content.xpath('//*[@id="mw-content-text"]/table[1]/tr/td')
        for p_list in province:
            p = p_list.xpath('a[position()>1]')
            for i in p:
                province_name = i.xpath('text()')[0]
                province_link = self.start_urls + i.xpath('@href')[0]
                print(province_name,province_link)
                yield Request(url=province_link, meta = {'province_name':province_name}, callback= self.parse_city)

    # city
    def parse_city(self,response):
        url = response.url
        province_name = response.meta['province_name']
        r = requests.get(url,headers=self.headers)
        content = etree.HTML(r.text)
        city = content.xpath('//*[@id="mw-content-text"]/table/tr[position()>1]')
        for c in city:
            city_name = c.xpath('td[1]/p/a/text()')[0]
            city_link = self.start_urls + c.xpath('td[1]/p/a/@href')[0]
            yield Request(url=city_link, meta = {'province_name':province_name,
                                            'city_name':city_name},callback=self.parse_district)
        # yield Request(url='https://www.youbianku.com/%E5%94%90%E5%B1%B1', meta={'province_name': '河北',
        #                                                                                  'city_name': '唐山'
        #                                                                                  }, callback=self.parse_district)

    #district
    def parse_district(self,response):
        city_name, district_name, postcode = '','',''
        try:
            url = response.url
            province_name = response.meta['province_name']
            city_name = response.meta['city_name']
            if province_name in self.municipality_list:
                city_name = province_name
                province_name = '(None)'
                r = requests.get(url, headers=self.headers)
                content = etree.HTML(r.text)
                district_name = content.xpath('//*[@id="mw-content-text"]/div[2]/div[3]/ul/li[4]/a/span/text()')[0].split('市')[-1]
                district_link = content.xpath('//*[@id="mw-content-text"]/div[2]/div[3]/ul/li[4]/a/@href')[0]
                r = requests.get(district_link, headers=self.headers)
                d = etree.HTML(r.text)
                postcodes = d.xpath('//*[@id="mw-content-text"]/p[1]/a/text()')
                for postcode in postcodes:
                    postcode_link = self.start_urls + '/' + postcode
                    yield Request(url=postcode_link,meta={'province_name':province_name,
                                            'city_name':city_name,
                                            'district_name':district_name,
                                            'postcode':postcode},callback=self.parse_postcode)
            elif province_name in self.hkmctw_list:
                pass
            else:
                r = requests.get(url,headers = self.headers)
                content = etree.HTML(r.text)
                district = content.xpath('//*[@id="mw-content-text"]/div[2]/div[4]/table/tr[position()>2]')
                for d in district:
                    district_name = d.xpath('td[3]/dl/dd/a/text()')[0].split('市')[-1]
                    district_link = self.start_urls + d.xpath('td[3]/dl/dd/a/@href')[0]
                    r = requests.get(district_link, headers=self.headers)
                    d = etree.HTML(r.text)
                    postcodes = d.xpath('//*[@id="mw-content-text"]/p[1]/a/text()')
                    for postcode in postcodes:
                        postcode_link = self.start_urls + '/' + postcode
                        yield Request(url=postcode_link, meta={'province_name': province_name,
                                                 'city_name': city_name,
                                                 'district_name': district_name,
                                                 'postcode': postcode}, callback=self.parse_postcode)
        except Exception as e:
            dt = datetime.datetime.now()
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            with open('exception.txt','a',encoding='utf8') as f:
                f.writelines('{}\tError:[district]\tCity_name:{}\tDistrict_name:{}\tPostcode:{}\tException:{}'.format(dt_str,city_name,district_name,postcode,e))

    # 新版postcode（跨区postcode，分区存入字典）
    def parse_postcode(self,response):
        item = PostcodespiderItem()
        url = response.url
        postcode = response.meta['postcode']
        r = requests.get(url, headers = self.headers)
        content = etree.HTML(r.text)
        all_address = content.xpath('//*[@id="myarticle"]/p/a')
        d = {}
        for i in all_address:
            address = ''.join(i.xpath('span/text()'))
            road = ''.join(i.xpath('text()')).strip()
            if address not in d:
                d[address] = [road]
            else:
                d[address].append(road)

        for i_d in d:
            item['address'] = i_d
            item['roads'] = ','.join(d[i_d])
            item['postcode'] = postcode
            if '省' in i_d:
                item['province'] = i_d.split('省')[0] +'省'
            elif '自治区' in i_d:
                item['province'] = i_d.split('自治区')[0] + '自治区'
            yield item

    # # 旧版postcode
    # # postcode
    # def parse_postcode(self,response):
    #     item = PostcodespiderItem()
    #     url = response.url
    #     province_name = response.meta['province_name']
    #     city_name = response.meta['city_name']
    #     district_name = response.meta['district_name']
    #     postcode = response.meta['postcode']
    #     r = requests.get(url, headers = self.headers)
    #     content = etree.HTML(r.text)
    #     address = ''.join(content.xpath('//*[@id="myarticle"]/p/a[1]/span/text()'))
    #     roads = ','.join([i.strip() for i in content.xpath('//*[@id="myarticle"]/p/a/text()')])
    #     item['province'] = province_name
    #     item['city'] = city_name
    #     item['district'] = district_name
    #     item['address'] = address
    #     item['roads'] = roads
    #     item['postcode'] = postcode
    #     yield item

class emptypostcodeSpider(scrapy.Spider):
    name = 'empty'
    start_urls = 'https://www.youbianku.com'
    headers = DEFAULT_REQUEST_HEADERS

    # province
    def start_requests(self):
        with open('empty_postcode.txt',encoding='utf8') as f:
            content = f.readlines()

        for line in content:
            postcode = line.strip('\n')
            postcode_link = self.start_urls + '/' + postcode
            print(postcode)
            yield Request(url=postcode_link, meta={'postcode':postcode}, callback=self.parse_postcode)

    # postcode
    def parse_postcode(self,response):
        item = PostcodespiderItem()
        url = response.url
        postcode = response.meta['postcode']
        r = requests.get(url, headers = self.headers)
        content = etree.HTML(r.text)
        address = ''.join(content.xpath('//*[@id="myarticle"]/p/a[1]/span/text()'))
        roads = ','.join([i.strip() for i in content.xpath('//*[@id="myarticle"]/p/a/text()')])
        item['address'] = address
        item['roads'] = roads
        item['postcode'] = postcode
        yield item

class multipostcodeSpider(scrapy.Spider):
    name = 'multi'
    start_urls = 'https://www.youbianku.com'
    headers = DEFAULT_REQUEST_HEADERS

    # province
    def start_requests(self):
        with open('last_postcode.txt',encoding='utf8') as f:
            content = f.readlines()
        for line in content:
            postcode = line.strip('\n')
            postcode_link = self.start_urls + '/' + postcode
            print(postcode)
            yield Request(url=postcode_link, meta={'postcode':postcode}, callback=self.parse_postcode)

    # postcode
    def parse_postcode(self,response):
        item = PostcodespiderItem()
        url = response.url
        postcode = response.meta['postcode']
        r = requests.get(url, headers = self.headers)
        content = etree.HTML(r.text)
        all_address = content.xpath('//*[@id="myarticle"]/p/a')
        d = {}
        for i in all_address:
            address = ''.join(i.xpath('span/text()'))
            road = ''.join(i.xpath('text()')).strip()
            if address not in d:
                d[address] = [road]
            else:
                d[address].append(road)

        for i_d in d:
            item['address'] = i_d
            item['roads'] = ','.join(d[i_d])
            item['postcode'] = postcode
            if '省' in i_d:
                item['province'] = i_d.split('省')[0] +'省'
            elif '自治区' in i_d:
                item['province'] = i_d.split('自治区')[0] + '自治区'
            else:
                item['province'] = i_d.split('市')[0] +'市'

            yield item

class queshipostcodeSpider(scrapy.Spider):
    name = 'queshi'
    start_urls = 'https://www.youbianku.com'
    headers = DEFAULT_REQUEST_HEADERS

    # province
    def start_requests(self):
        with open('queshi_name.txt',encoding='utf8') as f:
            content = f.readlines()
        for line in content:
            city = line.strip('\n')
            city_link = self.start_urls + '/' + city
            yield Request(url=city_link, callback=self.parse_district)

        # postcode_link = self.start_urls + '/' + '324118'
        # yield Request(url=postcode_link, meta={'postcode':'324118'}, callback=self.parse_postcode)

    #district
    def parse_district(self,response):
        city_name, district_name, postcode = '','',''
        try:
            url = response.url
            r = requests.get(url,headers = self.headers)
            content = etree.HTML(r.text)
            district = content.xpath('//*[@id="mw-content-text"]/div[2]/div[4]/table/tr[position()>2]')
            for d in district:
                district_link = self.start_urls + d.xpath('td[3]/dl/dd/a/@href')[0]
                r = requests.get(district_link, headers=self.headers)
                d = etree.HTML(r.text)
                postcodes = d.xpath('//*[@id="mw-content-text"]/p[1]/a/text()')
                for postcode in postcodes:
                    postcode_link = self.start_urls + '/' + postcode
                    yield Request(url=postcode_link, meta={'postcode': postcode}, callback=self.parse_postcode)
        except Exception as e:
            dt = datetime.datetime.now()
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            with open('exception.txt','a',encoding='utf8') as f:
                f.writelines('{}\tError:[district]\tCity_name:{}\tDistrict_name:{}\tPostcode:{}\tException:{}'.format(dt_str,city_name,district_name,postcode,e))

    # postcode
    def parse_postcode(self,response):
        item = PostcodespiderItem()
        url = response.url
        postcode = response.meta['postcode']
        r = requests.get(url, headers = self.headers)
        content = etree.HTML(r.text)
        all_address = content.xpath('//*[@id="myarticle"]/p/a')
        d = {}
        for i in all_address:
            address = ''.join(i.xpath('span/text()'))
            road = ''.join(i.xpath('text()')).strip()
            if address not in d:
                d[address] = [road]
            else:
                d[address].append(road)

        for i_d in d:
            item['address'] = i_d
            item['roads'] = ','.join(d[i_d])
            item['postcode'] = postcode
            if '省' in i_d:
                item['province'] = i_d.split('省')[0] +'省'
            elif '自治区' in i_d:
                item['province'] = i_d.split('自治区')[0] + '自治区'
            print(item['address'],item['postcode'],item['roads'])
            yield item


if __name__ == '__main__':
    execute('scrapy crawl youbianku'.split())
    # execute('scrapy crawl queshi'.split())
