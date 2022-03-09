import requests
from lxml import etree


def title():
    print('+--------------------------------------------------')
    print('+  \033[36m安全牛 https://all.aqniu.com/ 安全行业公司数据采集      \033[0m')
    print('+  \033[36m结果文件：                                           \033[0m')
    print('+  \033[36m1.行业类别链接：categories.txt                          \033[0m')
    print('+  \033[36m2.安全公司安全牛链接：aqniu_urls.txt                          \033[0m')
    print('+  \033[36m2.安全公司官网链接：corp_urls.txt                            \033[0m')
    print('+  \033[31m代码仅供学习，任何人不得将其用于非法用途，否则后果自行承担。  \033[0m')
    print('+--------------------------------------------------')


def get_category():
    print('+  \033[34m正在获取目标网站类别...\033[0m')
    output = []
    r = requests.get('https://all.aqniu.com/')
    sel = etree.HTML(r.text)
    category = sel.xpath('//*[@id]/div/a/@href')
    for i in category:
        if not i.endswith('.html'):
            output.append(i + '\n')

    output = list(set(output))
    with open('categories.txt', 'w', encoding='utf-8') as f:
        f.writelines(output)
    print('+  \033[34m获取目标网站类别成功，结果文件：category.txt\033[0m')


def get_aqniu_urls():
    print('+  \033[34m正在获取各安全公司在安全牛中的链接...\033[0m')
    output = []
    with open('categories.txt', 'r', encoding='utf-8') as f_in:
        urls = f_in.read().split()
        count = len(urls)

    for n, url in enumerate(urls):
        if n % 10 == 0 and n != 0:
            print('+  \033[34m共{}条，正在获取第{}条...\033[0m'.format(count, n))
        r = requests.get(url)
        sel = etree.HTML(r.text)
        items = sel.xpath('//*[@id]/div[1]/div/div/div/a/@href')
        items = [s + '\n' if r'/news/' not in s else '' for s in items]
        output.extend(items)
        with open('aqniu_urls.txt', 'w', encoding='utf-8') as f_out:
            f_out.writelines(output)
    print('+  \033[34m获取各安全公司在安全牛中的链接成功，结果文件：aqniu_urls.txt\033[0m')


def get_corp_urls():
    print('+  \033[34m正在获取各安全公司官网链接...\033[0m')
    output = []
    with open('aqniu_urls.txt', 'r', encoding='utf-8') as f_in:
        urls = f_in.read().split()
        count = len(urls)

    for n, url in enumerate(urls):
        if n % 100 == 0 and n != 0:
            print('+  \033[34m共{}条，正在获取第{}条...\033[0m'.format(count, n))
        r = requests.get(url)
        sel = etree.HTML(r.text)
        title = ''.join(sel.xpath('//*[@id="photo"]/div/div/main/article/div[2]/h1/text()'))
        link = ''.join(sel.xpath('//*[@id="photo"]/div/div/main/article/div[3]/a/@href'))
        output.append('{}\t{}\n'.format(title, link))
        with open('corp_urls.txt', 'w', encoding='utf-8') as f_out:
            f_out.writelines(output)
    print('+  \033[34m获取各安全公司官网链接成功，结果文件：corp_urls.txt\033[0m')


if __name__ == '__main__':
    title()
    # get_category()
    get_aqniu_urls()
    get_corp_urls()
