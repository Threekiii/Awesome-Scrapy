import requests
import time
import random
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
with open('C:/Users/W/Desktop/code/makeupspider/sinacrawl/host.txt','w',encoding='utf8') as f:
    f.write("")
f.close()
for i in range(1,2):
    time.sleep(random.uniform(0,1))
    #代理ip爬取
    url = 'https://www.xicidaili.com/nt/{}/'.format(i)
    s = requests.get(url,headers = headers)
    sel = etree.HTML(s.text, etree.HTMLParser())
    result = sel.xpath('//*[@id="ip_list"]/tr')
    with open('C:/Users/W/Desktop/code/spider/sinacrawl/host.txt','a',encoding='utf8') as fp:
        for r in result:
            try:
                ip = r.xpath('td[2]/text()')[0]
                host = r.xpath('td[3]/text()')[0]
                print(ip,host)
                fp.write(ip)
                fp.write('\t')
                fp.write(host)
                fp.write('\n')
            except Exception as e :
                pass
    fp.close()
