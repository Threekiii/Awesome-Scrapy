# coding=utf-8

import requests
import time
import random
import urllib.parse
from lxml import etree
from fake_useragent import UserAgent
ua = UserAgent()

keyword = 'HIDS'
data = {
    'keyword': keyword
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.cnvd.org.cn',
    'Referer': 'http://www.cnvd.org.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Cookie': '__jsluid_s=ac2e9b4a7df85f7c6a8ec9b10c68ec5f; JSESSIONID=DFB2D5E99173517B3F725E0835550423; __jsl_clearance_s=1647518540.307|0|IQLJUKc%2BwS%2BPkiDzY%2FKgMPcxXW4%3D'
}

result = []
result.append('title\tlink\tlevel\tclick\tcomment\tcollect\tpubtime\n')
for i in range(5):
    time.sleep(random.randint(1,10))
    base_url = 'https://www.cnvd.org.cn/'
    list_url = base_url + 'flaw/list?flag=true&offset={}&max=100&'.format(str(i*100))
    url = list_url+urllib.parse.urlencode(data)
    print(url)
    r = requests.get(url,headers=headers)
    # print(r.text)
    sel = etree.HTML(r.text)
    items = sel.xpath('//div[@id="flawList"]/tbody/tr')
    print(items)
    if len(items)<=1:
        break
    for i in items:
        title= ''.join(i.xpath('td/a/@title')).strip()
        link = base_url+''.join(i.xpath('td/a/@href')).strip()
        level = ''.join(i.xpath('td[2]/text()')).strip()
        click = ''.join(i.xpath('td[3]/text()')).strip()
        comment = ''.join(i.xpath('td[4]/text()')).strip()
        collect = ''.join(i.xpath('td[5]/text()')).strip()
        pubtime = ''.join(i.xpath('td[6]/text()')).strip()
        result.append('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(title,link,level,click,comment,collect,pubtime))

    with open('cnvd_{}.txt'.format(keyword),'w',encoding='utf-8') as f:
        f.writelines(result)
