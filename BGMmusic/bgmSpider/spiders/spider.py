import requests
import scrapy
import urllib.parse
from lxml import etree
from scrapy.cmdline import execute
from scrapy import Request
from bgmSpider.items import bgmspiderItem

class bgmSpider(scrapy.Spider):
    name = 'bgm'
    start_urls = ['https://www.bensound.com/royalty-free-music/']
    item = bgmspiderItem()
    category_dict = {
        # 'acoustic-folk': 4,
        'cinematic': 8,
        'corporate-pop': 6,
        'electronica': 5,
        'funky-groove': 3,
        'jazz': 2,
        'rock': 3,
        'world-others': 2
    }
    all_page_number = 23

    def start_requests(self):
        # for i in range(1,self.all_page_number+1):
        #     url = self.start_urls[0] + str(i)
        for cat in self.category_dict:
            for page in range(1,self.category_dict[cat]+1):
                url = self.start_urls[0] + str(cat) + '/' + str(page)
                print(url)
                yield Request(url = url, callback= self.parse)

    def parse(self, response):
        r = requests.get(response.url)
        hostname = urllib.parse.urlparse(response.url).hostname
        sel = etree.HTML(r.text)
        all_bgm = sel.xpath('//*[@id="products_grid"]/div[4]/div')
        for bgm in all_bgm:
            self.item['bgm_cat'] = response.url.split('/')[-2]
            self.item['bgm_name'] = bgm.xpath('div[2]/div[1]/p[1]/text()')[0].strip()
            self.item['bgm_time'] = bgm.xpath('div[2]/div[1]/p[2]/text()')[0]
            self.item['bgm_music'] = 'https://{}'.format(hostname)+bgm.xpath('div[2]/div[2]/div[1]/div[1]/audio/@src')[0]
            self.item['bgm_img'] = 'https://{}'.format(hostname)+'/'+bgm.xpath('div[1]/a/img[1]/@src')[0]
            self.item['bgm_link'] = bgm.xpath('div[2]/div[2]/div[1]/a/@href')[0]
            r = requests.get(url=self.item['bgm_link'])
            sel = etree.HTML(r.text)
            bgm_tag = sel.xpath('//*[@id="info_focus"]/p/span/a/text()')
            for i in range(bgm_tag.count('')):
                bgm_tag.remove('')
            self.item['bgm_tag'] = ','.join(bgm_tag)
            yield self.item

if __name__ == '__main__':
    execute('scrapy crawl bgm'.split())

