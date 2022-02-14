
# 招标公告 page：1380 id：lia_12
# 结果公告 page：447 id：lia_13


import requests
import time
from selenium import webdriver

zhaobiao_page = 1380
jieguo_page = 447
zhaobiao_id = 'lia_12'
jieguo_id = 'lia_13'

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--user-data-dir=/data/crawl/chrome')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')
    chrome_options.add_argument("--proxy-server=http://172.16.32.34:12345")
    driver  = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(180)
    driver.implicitly_wait(20)
    driver.get('http://www.cntcitc.com.cn/more.html?chanType=3&chanId=16')
    time.sleep(5)
    driver.find_element_by_id(zhaobiao_id).click()
    time.sleep(5)
    for p in range(1,zhaobiao_page):
        links = driver.find_elements_by_class_name('sid_l')
        links_num = len(links)
        for l in range(links_num):
            links[l].click()
            time.sleep(4)
            # print(driver.page_source)
            with open('data.txt','a',encoding='utf8') as f:
                output = '{}\t{}\n'.format(' '.join(
                    driver.page_source.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').split()),
                                              time.strftime("%Y-%m-%d", time.localtime()))
                f.write(output)
            print('Current page：{}'.format(p))
            driver.find_element_by_id(zhaobiao_id).click()
            time.sleep(4)
            links = driver.find_elements_by_class_name('sid_l')
        set_page = driver.find_element_by_id('setPage').send_keys(p+1)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="right"]/div[3]/div[2]/span[2]/a[10]').click()
        # pages = driver.find_element_by_xpath('//*[@id="right"]/div[3]/div[2]/span[2]/a[8]')
        # pages.click()
        time.sleep(5)
    driver.close()
