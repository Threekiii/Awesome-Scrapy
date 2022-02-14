# coding:utf8
import sys
import os
import time
import htmlfilter
fpath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
ffpath = os.path.abspath(os.path.join(fpath,".."))
sys.path.append(ffpath)

import re
import scrapy
import scrapy
import datetime
import requests
import urllib.parse
from scrapy import Request
from scrapy.cmdline import execute
from lxml import etree
from liepinSpider.settings import DEFAULT_REQUEST_HEADERS,PARAMS,JOBS_PARAMS
from liepinSpider.items import LiepinspiderItem

class liepinlinkSpider(scrapy.Spider):
    name = 'liepin_link'
    start_urls = 'https://www.liepin.com'
    headers = DEFAULT_REQUEST_HEADERS
    params = PARAMS.copy()

    def start_requests(self):
        get_city_url = self.start_urls +'/citylist/'
        r = requests.get(get_city_url)
        content = etree.HTML(r.text)
        cities = content.xpath('//div[@class="citieslist"]/ol/li/p/span[2]/a/@href')
        dqs_id = []
        company_entity_id = []
        company_rank_id = []
        industry_id = []
        salary_id = []

        search_url = self.start_urls + '/zhaopin/?d_sfrom=search_fp_nvbar&init=1'
        r = requests.get(search_url)
        content = etree.HTML(r.text)
        company_entity_link = content.xpath('//div[@class="search-conditions"]/dl/dd/ul/li/a/@href')
        for s in company_entity_link:
            compIds = re.findall('compIds=([0-9a-zA-Z_%]+)',s)
            if compIds:
                company_entity_id.append(compIds[0])

        company_rank_link = content.xpath('//div[@class="search-conditions"]/dl/dd/div[3]/a/@href')
        for s in company_rank_link:
            compTag = re.findall('compTag=([0-9a-zA-Z_%]+)',s)
            if compTag:
                company_rank_id.append(compTag[0])

        industry_link = content.xpath('//div[@class="search-conditions"]/dl[2]/dd/ul/li/div/a/@href')
        for s in industry_link:
            industryType = re.findall('industryType=([0-9a-zA-Z_%]+)',s)
            industries = re.findall('industries=([0-9a-zA-Z_%]+)',s)
            if industryType and industries:
                industry_id.append('{}|{}'.format(industryType[0],industries[0]))

        salary_link = content.xpath('//div[@class="search-conditions"]/dl[4]/dd/a/@href')
        for s in salary_link:
            salary = re.findall('salary=([0-9a-zA-Z_%]+)', s)
            if salary:
                salary = urllib.parse.unquote(salary[0])
                salary_id.append(salary)

        for c in cities:
            city_link = self.start_urls + c
            r = requests.get(city_link)
            content = etree.HTML(r.text)
            city_dqs = content.xpath('//*[@id="search_form"]/input[2]/@value')[0]
            dqs_id.append(city_dqs)

        print('——————————————————————log——————————————————————')
        print('获取company_entity_id：{}'.format(len(company_entity_id)))
        print('获取company_rank_id：{}'.format(len(company_rank_id)))
        print('获取industry_id：{}'.format(len(industry_id)))
        print('获取salary_id：{}'.format(len(salary_id)))
        print('获取dqs_id：{}'.format(len(dqs_id)))

        all_link = []

        for pn in range(10):
            for ii in industry_id:
                for di in dqs_id:
                    params = self.params.copy()
                    # params['compIds'] = ce
                    # params['compTag'] = cr
                    params['industryType'] = ii.split('|')[0]
                    params['industries'] = ii.split('|')[1]
                    # params['salary'] = si
                    params['dqs'] = di
                    params['curPage'] = pn
                    url = self.start_urls + '/zhaopin/?' + urllib.parse.urlencode(params)
                    # print(url)
                    all_link.append(url + '\n')

        with open('liepin_link.txt','w',encoding='utf8') as f:
            f.writelines(all_link)

        yield Request(url=self.start_urls, callback= self.parse)

    def parse(self, response):
        print('猎聘网【省市/职位】link已更新完成.')
        pass

class liepinjobSpider(scrapy.Spider):
    name = 'liepin'
    start_urls = 'https://www.liepin.com'
    headers = DEFAULT_REQUEST_HEADERS
    params = JOBS_PARAMS.copy()
    date = time.strftime("%Y-%m-%d", time.localtime())
    dir = '/data/crawl/crawltool/user_work/guolinchong/data/profession/猎聘网/{}'.format(date)


    def start_requests(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        with open('liepin_link.txt',encoding='utf8') as f:
            urls = f.read().splitlines()
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        r = requests.get(url)
        content = etree.HTML(r.text)
        all_links = content.xpath('//@href')
        for i in all_links:
            if i.startswith('https://www.liepin.com/job/') and len(i)>27:
                print(i)
                yield Request(url=i, callback=self.parse_job)

    def parse_job(self, response):
        url = response.url + '?' + urllib.parse.urlencode(self.params)
        print(url)
        r = requests.get(url)
        with open('{}/data.txt'.format(self.dir),'a',encoding='utf8') as f:
            output = '{}\t{}\t{}\n'.format(response.url,' '.join(r.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').split()),
                                           self.date)
            f.write(output)

if __name__ == '__main__':
    execute('scrapy crawl liepin'.split())