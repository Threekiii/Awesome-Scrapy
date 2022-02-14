# -*- coding: utf-8 -*-

# Scrapy settings for insSpider_v2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'insSpider_v2'

SPIDER_MODULES = ['insSpider_v2.spiders']
NEWSPIDER_MODULE = 'insSpider_v2.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'insSpider_v2 (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
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
from fake_useragent import UserAgent
ua = UserAgent()
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': ua.random
}
DEFAULT_USER_HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie':'mid=XV5NowALAAFLAY_OhkeFrCBn-m44; csrftoken=B6hWfLthaGJeUg6uqObAkr6FnxJPKyhe; ds_user_id=1477045790; sessionid=1477045790%3Aj9BH14XYjHFqsS%3A13; shbid=16503; shbts=1573443991.981885; rur=FRC; urlgen="{\"211.249.66.5\": 23576}:1iU5CO:uEx95BeFvOEC1YKP1EKTTS0WMjI"',
    'User-Agent': ua.random,

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'insSpider_v2.middlewares.InsspiderV2SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'insSpider_v2.middlewares.InsspiderV2DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'insSpider_v2.pipelines.InsspiderV2Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Mysql Database
MYSQL_HOST = YOUR_HOST
MYSQL_DBNAME = YOUR_DBNAME
MYSQL_USER = YOUR_USERNAME
MYSQL_PASSWD = YOUR_PASSWD

#dict
language_dict = {
    # ISO 639-1
    'af': '南非语',
    'am': '阿姆哈拉语',
    'an': '阿拉贡语',
    'ar': '阿拉伯语',
    'as': '阿萨姆语',
    'az': '阿塞拜疆语',
    'be': '白俄罗斯语',
    'bg': '保加利亚语',
    'bn': '孟加拉语',
    'br': '布列塔尼语',
    'bs': '波斯尼亚语',
    'ca': '加泰隆语',
    'cs': '捷克语',
    'cy': '威尔士语',
    'da': '丹麦语',
    'de': '德语',
    'dz': '不丹语',
    'el': '现代希腊语',
    'en': '英语',
    'eo': '世界语',
    'es': '西班牙语',
    'et': '爱沙尼亚语',
    'eu': '巴斯克语',
    'fa': '波斯语',
    'fi': '芬兰语',
    'fo': '法罗语',
    'fr': '法语',
    'ga': '爱尔兰语',
    'gl': '加利西亚语',
    'gu': '古吉拉特语',
    'he': '希伯来语',
    'hi': '印地语',
    'hr': '克罗地亚语',
    'ht': '海地克里奥尔语',
    'hu': '匈牙利语',
    'hy': '亚美尼亚语',
    'id': '印尼语',
    'is': '冰岛语',
    'it': '意大利语',
    'ja': '日语',
    'jv': '爪哇语',
    'ka': '格鲁吉亚语',
    'kk': '哈萨克语',
    'km': '高棉语',
    'kn': '卡纳达语',
    'ko': '韩语',
    'ku': '库尔德语',
    'ky': '吉尔吉斯语',
    'la': '拉丁语',
    'lb': '卢森堡语',
    'lo': '老挝语',
    'lt': '立陶宛语',
    'lv': '拉脱维亚语',
    'mg': '马达加斯加语',
    'mk': '马其顿语',
    'ml': '马拉亚拉姆语',
    'mn': '蒙古语',
    'mr': '马拉提语',
    'ms': '马来语',
    'mt': '马耳他语',
    'nb': '书面挪威语',
    'ne': '尼泊尔语',
    'nl': '荷兰语',
    'nn': '新挪威语',
    'no': '挪威语',
    'oc': '奥克语',
    'or': '奥利亚语',
    'pa': '旁遮普语',
    'pl': '波兰语',
    'ps': '普什图语',
    'pt': '葡萄牙语',
    'qu': '凯楚亚语',
    'ro': '罗马尼亚语',
    'ru': '俄语',
    'rw': '卢旺达语',
    'se': '北萨米语',
    'si': '僧伽罗语',
    'sk': '斯洛伐克语',
    'sl': '斯洛文尼亚语语',
    'sq': '阿尔巴尼亚语',
    'sr': '塞尔维亚语',
    'sv': '瑞典语',
    'sw': '斯瓦希里语',
    'ta': '泰米尔语',
    'te': '泰卢固语',
    'th': '泰语',
    'tl': '他加禄语',
    'tr': '土耳其语',
    'ug': '维吾尔语',
    'uk': '乌克兰语',
    'ur': '乌尔都语',
    'vi': '越南语',
    'vo': '沃拉普克语',
    'wa': '沃伦语',
    'xh': '科萨语',
    'zh': '中文',
    'zu': '祖鲁语'
}

#logging
LOG_LEVEL = 'ERROR'
LOG_FILE = './log.log'