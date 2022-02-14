# -*- coding: utf-8 -*-

# Scrapy settings for liepinSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'liepinSpider'

SPIDER_MODULES = ['liepinSpider.spiders']
NEWSPIDER_MODULE = 'liepinSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'liepinSpider (+http://www.yourdomain.com)'
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Host':'www.liepin.com',
    'User-Agent':ua.random,
    'Connection':'keep-alive',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Upgrade-Insecure-Requests':'1'
}

PARAMS = {
    'flushckid': '1',
    'compkid': '',
    'dqs': '',
    'pubTime': '',
    'jobTitles': '',
    'pageSize': '40',
    'salary': '',
    'compTag': '',
    'sortFlag': '',
    'compIds': '',
    'subIndustry': '',
    'industryType': '',
    'jobKind': '',
    'industries': '',
    'compscale': '',
    'key': '',
    'siTag': '1B2M2Y8AsgTpgAmY7PhCfg~fA9rXquZc5IkJpXC-Ycixw',
    'd_sfrom': 'search_fp_nvbar',
    'd_ckId': '1030fb8d3c58fdae0178b5ab2872aad8',
    'd_curPage': '0',
    'd_pageSize': '40',
    'd_headId': '1030fb8d3c58fdae0178b5ab2872aad8',
    'curPage': ''
}

JOBS_PARAMS = {
    'imscid': 'R000000075',
    'siTag': '1B2M2Y8AsgTpgAmY7PhCfg~fA9rXquZc5IkJpXC-Ycixw',
    'd_sfrom': 'search_fp_nvbar',
    'd_ckId': 'f51bfb836cffaf9c884def0bd5f0d47e',
    'd_curPage': '0',
    'd_pageSize': '40',
    'd_headId': 'f51bfb836cffaf9c884def0bd5f0d47e',
    'd_posi':'5'
}
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'liepinSpider.middlewares.LiepinspiderSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'liepinSpider.middlewares.LiepinspiderDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'liepinSpider.pipelines.LiepinspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
