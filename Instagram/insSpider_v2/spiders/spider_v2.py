import scrapy
import json
import time,datetime
import re
import requests
import pymysql
import langid
import logging
from lxml import etree
from scrapy import Request
from jsonpath import jsonpath
from scrapy.cmdline import execute
from insSpider_v2.settings import DEFAULT_REQUEST_HEADERS,DEFAULT_USER_HEADERS
from insSpider_v2.items import InsspiderV2Item,InstranslateItem
from urllib.parse import urlencode
from insSpider_v2 import settings
from selenium import webdriver

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class inspageSpiderv2(scrapy.Spider):
    name = 'inspagev2'
    start_urls = ['https://www.instagram.com/']
    item = InsspiderV2Item()

    with open('C:/Users/W/Desktop/ins_keywords.txt', 'r', encoding='utf-8') as f:
        keywords = f.read()
        search_list = keywords.split('\n')
    #
    # search_list = ['b612selfie', 'b612camera', 'b612%F0%9F%93%B7', 'b612cameraselfie', 'b612app', '崽崽zepeto',
    #                'ulike', 'ulikecamera', 'ulikeselfie', 'faceu', 'sodacam', 'sodacamera']

    def start_requests(self):
        for s in self.search_list:
            url = 'https://www.instagram.com/explore/tags/{}/'.format(s)
            if s == 'b612%F0%9F%93%B7':
                s = 'b612相机(图标)'
            yield Request(url=url, meta={'keywords': s},callback=self.parse_page)

    def parse_page(self,response):
        url = response.url
        keywords = response.meta['keywords']
        r = requests.get(url,headers = DEFAULT_REQUEST_HEADERS)
        sel = etree.HTML(r.text)
        content = sel.xpath('/html/body/script[1]/text()')
        content = re.sub('window._sharedData = ','',content[0]).rstrip(';')
        data = json.loads(content)
        end_cursor = jsonpath(data,'$.entry_data.TagPage[0].graphql.hashtag.edge_hashtag_to_media.page_info.end_cursor')[0]
        has_next_page = jsonpath(data,'$.entry_data.TagPage[0].graphql.hashtag.edge_hashtag_to_media.page_info.has_next_page')[0]
        print(has_next_page)
        posts = jsonpath(data, '$.entry_data.TagPage[0].graphql.hashtag.[edge_hashtag_to_media,edge_hashtag_to_top_posts].edges[*]')
        for post in posts:
            self.item['keywords'] = keywords
            self.item['type'] = jsonpath(post, '$.node.__typename')[0]
            try:
                self.item['img_description'] = ''.join(jsonpath(post, '$.node.accessibility_caption'))
            except TypeError as e:
                self.item['img_description'] = ''
            self.item['cover_height'] = jsonpath(post, '$.node.dimensions.height')[0]
            self.item['cover_width'] = jsonpath(post, '$.node.dimensions.width')[0]
            self.item['cover_link'] = jsonpath(post, '$.node.display_url')[0]
            self.item['liked_count'] = jsonpath(post, '$.node.edge_liked_by.count')[0]
            try:
                self.item['content'] = ''.join(jsonpath(post, '$.node.edge_media_to_caption.edges[*].node.text'))
            except Exception as e:
                pass
            self.item['comment_count'] = jsonpath(post, '$.node.edge_media_to_comment.count')[0]
            self.item['post_id'] = jsonpath(post, '$.node.id')[0]
            self.item['post_url'] = jsonpath(post, '$.node.shortcode')[0]
            self.item['post_link'] = self.start_urls[0] + 'p/' + self.item['post_url'] + '/'
            self.item['user_id'] = jsonpath(post, '$.node.owner.id')[0]
            self.item['is_video'] = jsonpath(post, '$.node.is_video')[0]
            timestamp = jsonpath(post, '$.node.taken_at_timestamp')[0]
            self.item['pub_time'] = time.strftime("%Y-%m-%d", time.localtime(timestamp))
            yield self.item

        if has_next_page:
            variable_dict = {
                "tag_name": keywords,
                "first": 12,
                "after": end_cursor
            }
            variable_json = json.dumps(variable_dict)
            print(variable_dict)
            params = {
                'query_hash': '174a5243287c5f3a7de741089750ab3b',
                'variables': variable_json
            }
            url = 'https://www.instagram.com/graphql/query/?{}'.format(urlencode(params))
            yield Request(url=url, meta={'keywords': keywords,
                                         'break_count':1},callback=self.parse_nextpage)

    def parse_nextpage(self,response):
        try:
            keywords = response.meta['keywords']
            break_count = int(response.meta['break_count'])
            r = requests.get(response.url)
            time.sleep(1)
            data = r.json()
            end_cursor = jsonpath(data, '$.data.hashtag.edge_hashtag_to_media.page_info.end_cursor')[0]
            has_next_page = jsonpath(data, '$.data.hashtag.edge_hashtag_to_media.page_info.has_next_page')[0]
            posts = jsonpath(data,'$.data.hashtag.edge_hashtag_to_media.edges[*]')
            for post in posts:
                self.item['keywords'] = keywords
                self.item['type'] = jsonpath(post, '$.node.__typename')[0]
                try:
                    self.item['img_description'] = ''.join(jsonpath(post, '$.node.accessibility_caption'))
                except TypeError as e:
                    self.item['img_description'] = ''

                try:
                    self.item['content'] = ''.join(jsonpath(post, '$.node.edge_media_to_caption.edges[*].node.text'))
                except TypeError as e:
                    self.item['content'] = ''

                self.item['cover_height'] = jsonpath(post, '$.node.dimensions.height')[0]
                self.item['cover_width'] = jsonpath(post, '$.node.dimensions.width')[0]
                self.item['cover_link'] = jsonpath(post, '$.node.display_url')[0]
                self.item['liked_count'] = jsonpath(post, '$.node.edge_liked_by.count')[0]
                self.item['comment_count'] = jsonpath(post, '$.node.edge_media_to_comment.count')[0]
                self.item['post_id'] = jsonpath(post, '$.node.id')[0]
                self.item['post_url'] = jsonpath(post, '$.node.shortcode')[0]
                self.item['post_link'] = self.start_urls[0] + 'p/' + self.item['post_url'] + '/'
                self.item['user_id'] = jsonpath(post, '$.node.owner.id')[0]
                self.item['is_video'] = jsonpath(post, '$.node.is_video')[0]
                timestamp = jsonpath(post, '$.node.taken_at_timestamp')[0]
                self.item['pub_time'] = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                yield self.item

            # today = datetime.date.today()
            # today_weekday = today.isoweekday()
            # last_sunday = str(today - datetime.timedelta(days=today_weekday))
            # pub_time = self.item['pub_time']
            logging.error('{},{}.'.format(has_next_page,end_cursor))

            if has_next_page and break_count < 200:
                break_count +=1
                print('********************************************************************************************************************************')
                print(break_count)
                logging.error('break_count:{}.'.format(break_count))
                variable_dict = {
                    "tag_name": keywords,
                    "first": 12,
                    "after": end_cursor
                }
                variable_json = json.dumps(variable_dict)
                params = {
                    'query_hash': '174a5243287c5f3a7de741089750ab3b',
                    'variables': variable_json
                }
                url = 'https://www.instagram.com/graphql/query/?{}'.format(urlencode(params))
                yield Request(url=url,meta={'keywords': keywords,
                                            'break_count':break_count},
                              callback=self.parse_nextpage)
        except Exception as e:
            logging.error('{},{}.'.format(e,response.url))

class insaddpageSpiderv2(scrapy.Spider):
    name = 'insaddpagev2'
    start_urls = ['https://www.instagram.com/']
    item = InsspiderV2Item()

    # with open('C:/Users/W/Desktop/ins_keywords.txt', 'r', encoding='utf-8') as f:
    #     keywords = f.read()
    #     search_list = keywords.split('\n')
    #
    search_list = ['ulike', 'ulikecamera', 'ulikeselfie', 'zepeto']

    def start_requests(self):
        for s in self.search_list:
            url = 'https://www.instagram.com/explore/tags/{}/'.format(s)
            if s == 'b612%F0%9F%93%B7':
                s = 'b612相机(图标)'
            yield Request(url=url, meta={'keywords': s},callback=self.parse_page)

    def parse_page(self,response):
        url = response.url
        keywords = response.meta['keywords']
        r = requests.get(url,headers = DEFAULT_REQUEST_HEADERS)
        sel = etree.HTML(r.text)
        content = sel.xpath('/html/body/script[1]/text()')
        content = re.sub('window._sharedData = ','',content[0]).rstrip(';')
        data = json.loads(content)
        end_cursor = jsonpath(data,'$.entry_data.TagPage[0].graphql.hashtag.edge_hashtag_to_media.page_info.end_cursor')[0]
        has_next_page = jsonpath(data,'$.entry_data.TagPage[0].graphql.hashtag.edge_hashtag_to_media.page_info.has_next_page')[0]
        print(has_next_page)
        posts = jsonpath(data, '$.entry_data.TagPage[0].graphql.hashtag.[edge_hashtag_to_media,edge_hashtag_to_top_posts].edges[*]')
        for post in posts:
            self.item['keywords'] = keywords
            self.item['type'] = jsonpath(post, '$.node.__typename')[0]
            try:
                self.item['img_description'] = ''.join(jsonpath(post, '$.node.accessibility_caption'))
            except TypeError as e:
                self.item['img_description'] = ''
            self.item['cover_height'] = jsonpath(post, '$.node.dimensions.height')[0]
            self.item['cover_width'] = jsonpath(post, '$.node.dimensions.width')[0]
            self.item['cover_link'] = jsonpath(post, '$.node.display_url')[0]
            self.item['liked_count'] = jsonpath(post, '$.node.edge_liked_by.count')[0]
            try:
                self.item['content'] = ''.join(jsonpath(post, '$.node.edge_media_to_caption.edges[*].node.text'))
            except Exception as e:
                pass
            self.item['comment_count'] = jsonpath(post, '$.node.edge_media_to_comment.count')[0]
            self.item['post_id'] = jsonpath(post, '$.node.id')[0]
            self.item['post_url'] = jsonpath(post, '$.node.shortcode')[0]
            self.item['post_link'] = self.start_urls[0] + 'p/' + self.item['post_url'] + '/'
            self.item['user_id'] = jsonpath(post, '$.node.owner.id')[0]
            self.item['is_video'] = jsonpath(post, '$.node.is_video')[0]
            timestamp = jsonpath(post, '$.node.taken_at_timestamp')[0]
            self.item['pub_time'] = time.strftime("%Y-%m-%d", time.localtime(timestamp))
            yield self.item

        if has_next_page:
            variable_dict = {
                "tag_name": keywords,
                "first": 12,
                "after": end_cursor
            }
            variable_json = json.dumps(variable_dict)
            print(variable_dict)
            params = {
                'query_hash': '174a5243287c5f3a7de741089750ab3b',
                'variables': variable_json
            }
            url = 'https://www.instagram.com/graphql/query/?{}'.format(urlencode(params))
            yield Request(url=url, meta={'keywords': keywords,
                                         'break_count':1},callback=self.parse_nextpage)

    def parse_nextpage(self,response):
        try:
            keywords = response.meta['keywords']
            break_count = int(response.meta['break_count'])
            r = requests.get(response.url)
            time.sleep(1)
            data = r.json()
            end_cursor = jsonpath(data, '$.data.hashtag.edge_hashtag_to_media.page_info.end_cursor')[0]
            has_next_page = jsonpath(data, '$.data.hashtag.edge_hashtag_to_media.page_info.has_next_page')[0]
            posts = jsonpath(data,'$.data.hashtag.edge_hashtag_to_media.edges[*]')
            for post in posts:
                self.item['keywords'] = keywords
                self.item['type'] = jsonpath(post, '$.node.__typename')[0]
                try:
                    self.item['img_description'] = ''.join(jsonpath(post, '$.node.accessibility_caption'))
                except TypeError as e:
                    self.item['img_description'] = ''

                try:
                    self.item['content'] = ''.join(jsonpath(post, '$.node.edge_media_to_caption.edges[*].node.text'))
                except TypeError as e:
                    self.item['content'] = ''

                self.item['cover_height'] = jsonpath(post, '$.node.dimensions.height')[0]
                self.item['cover_width'] = jsonpath(post, '$.node.dimensions.width')[0]
                self.item['cover_link'] = jsonpath(post, '$.node.display_url')[0]
                self.item['liked_count'] = jsonpath(post, '$.node.edge_liked_by.count')[0]
                self.item['comment_count'] = jsonpath(post, '$.node.edge_media_to_comment.count')[0]
                self.item['post_id'] = jsonpath(post, '$.node.id')[0]
                self.item['post_url'] = jsonpath(post, '$.node.shortcode')[0]
                self.item['post_link'] = self.start_urls[0] + 'p/' + self.item['post_url'] + '/'
                self.item['user_id'] = jsonpath(post, '$.node.owner.id')[0]
                self.item['is_video'] = jsonpath(post, '$.node.is_video')[0]
                timestamp = jsonpath(post, '$.node.taken_at_timestamp')[0]
                self.item['pub_time'] = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                yield self.item

            logging.error('{},{}.'.format(has_next_page,end_cursor))

            if has_next_page and break_count < 200:
                break_count +=1
                print('********************************************************************************************************************************')
                print(break_count)
                logging.error('break_count:{}.'.format(break_count))
                variable_dict = {
                    "tag_name": keywords,
                    "first": 12,
                    "after": end_cursor
                }
                variable_json = json.dumps(variable_dict)
                params = {
                    'query_hash': '174a5243287c5f3a7de741089750ab3b',
                    'variables': variable_json
                }
                url = 'https://www.instagram.com/graphql/query/?{}'.format(urlencode(params))
                yield Request(url=url,meta={'keywords': keywords,
                                            'break_count':break_count},
                              callback=self.parse_nextpage)
        except Exception as e:
            logging.error('{},{}.'.format(e,response.url))



class inspostSpiderv2(scrapy.Spider):
    name = 'inspostv2'
    start_urls = ['https://www.instagram.com/']
    item = InsspiderV2Item()

    def start_requests(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        cursor = connect.cursor()
        cursor.execute('select post_link,cover_link from ins where img_links is Null')
        result = cursor.fetchall()
        for link in result:
            yield Request(url=link[0], meta={'cover_link':link[1]},callback=self.parse_page)

    def parse_page(self,response):
        self.item['post_link'] = response.url
        self.item['cover_link'] = response.meta['cover_link']
        r = requests.get(self.item['post_link'], headers=DEFAULT_REQUEST_HEADERS)
        sel = etree.HTML(r.text)
        content = sel.xpath('/html/body/script[1]/text()')
        content = re.sub('window._sharedData = ', '', content[0]).rstrip(';')
        data = json.loads(content)
        self.item['is_ad'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.is_ad')[0]
        self.item['is_video'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.is_video')[0]
        self.item['user_name'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.owner.username')[0]
        self.item['user_fullname'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.owner.full_name')[0]

        if self.item['is_video']:
            self.item['video_link'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.video_url')[0]
            self.item['video_duration'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.video_duration')[0]
            self.item['video_view_count'] = jsonpath(data, '$.entry_data.PostPage[*].graphql.shortcode_media.video_view_count')[0]
            self.item['img_links'] = None
        else:
            self.item['video_link'] = None
            self.item['video_duration'] = None
            self.item['video_view_count'] = None
            self.item['img_links'] = jsonpath(data,'$.entry_data.PostPage[*].graphql.shortcode_media.edge_sidecar_to_children.edges[*].node.display_url')

        if self.item['img_links']:
            self.item['img_links'] = ','.join(self.item['img_links'])
        else:
            self.item['img_links'] = self.item['cover_link']
        yield self.item

class insuserSpiderv2(scrapy.Spider):
    name = 'insuserv2'
    start_urls = ['https://www.instagram.com/']
    item = InsspiderV2Item()

    def start_requests(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        cursor = connect.cursor()
        cursor.execute('select user_name,post_link from ins where user_following is Null')
        result = cursor.fetchall()
        for item in result:
            # user_link = 'https://www.instagram.com/{}/'.format(item[0])
            post_link = item[1]
            yield Request(url=post_link,meta={'user_name':item[0]},callback=self.parse_page)

    def parse_page(self,response):
        self.item['user_name'] = response.meta['user_name']
        url = 'https://www.instagram.com/{}/'.format(self.item['user_name'])
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        driver = webdriver.Chrome(options=chrome_options, executable_path='C:/chromedriver')
        driver.get(url)
        time.sleep(2)
        sel = etree.HTML(driver.page_source)

        try:
            self.item['user_followed_by'] = sel.xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span/@title')[0].replace(',', '')
        except IndexError:
            self.item['user_followed_by'] = '-1'

        try:
            self.item['user_following'] = sel.xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span/text()')[0].replace(',', '')
        except IndexError:
            self.item['user_following'] = '-1'

        self.item['user_biography'] = sel.xpath(
            'string(//*[@id="react-root"]/section/main/div/header/section/div[2]/span)')

        driver.close()
        yield self.item




        #
        # user_link = response.url
        # self.item['user_name'] = response.meta['user_name']
        # r = requests.get(user_link, headers=DEFAULT_USER_HEADERS)
        # sel = etree.HTML(r.text)
        # content = sel.xpath('/html/body/script[1]/text()')
        # content = re.sub('window._sharedData = ', '', content[0]).rstrip(';')
        # data = json.loads(content)
        # print(data)
        # try:
        #     self.item['user_biography'] = jsonpath(data, '$.entry_data.ProfilePage[*].graphql.user.biography')[0]
        # except TypeError as e:
        #     self.item['user_biography'] = None
        #
        # try:
        #     self.item['user_following'] = jsonpath(data, '$.entry_data.ProfilePage[*].graphql.user.edge_follow.count')[0]
        # except TypeError:
        #     self.item['user_following'] = None
        #
        # try:
        #     self.item['user_followed_by'] = jsonpath(data, '$.entry_data.ProfilePage[*].graphql.user.edge_followed_by.count')[0]
        # except TypeError:
        #     self.item['user_followed_by'] = None
        #
        # try:
        #     self.item['user_fullname'] = jsonpath(data, '$.entry_data.ProfilePage[*].graphql.user.full_name')[0]
        # except TypeError:
        #     self.item['user_fullname'] = None
        # yield self.item

class instranslateSpiderv2(scrapy.Spider):
    name = 'instranslatev2'
    start_urls = ['https://www.instagram.com/']
    item = InstranslateItem()

    def start_requests(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            use_unicode=True)
        cursor = connect.cursor()
        cursor.execute('select post_link,content from ins where machine_translation_language is Null')
        result = cursor.fetchall()
        for item in result:
            content = item[1]
            if len(content.replace(' ', '')) != 0:
                abbr = langid.classify(content)[0]
                language = settings.language_dict[abbr]
                yield Request(url=item[0], meta={'language':language},callback=self.parse)

    def parse(self, response):
        self.item['language'] = response.meta['language']
        self.item['post_link'] = response.url
        yield self.item

if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'inspagev2'])
    execute(['scrapy', 'crawl', 'inspostv2'])
    # execute(['scrapy', 'crawl', 'insuserv2'])
    # execute(['scrapy', 'crawl', 'instranslatev2'])