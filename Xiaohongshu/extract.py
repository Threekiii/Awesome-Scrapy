from mitmproxy import ctx
from jsonpath import jsonpath
import re
import json
import pymysql
import settings
import datetime
from urllib.parse import unquote

# 所有发出的请求数据包都会被这个方法所处理
def request(flow):
    # 获取请求对象
    request = flow.request
    # # 实例化输出类
    # info = ctx.log.info
    # # 打印请求的url
    # info(request.url)
    # # 打印请求方法
    # info(request.method)
    # # 打印host头
    # info(request.host)
    # # 打印请求端口
    # info(str(request.port))
    # # 打印所有请求头部
    # info(str(request.headers))
    # # 打印cookie头
    # info(str(request.cookies))

# 所有服务器响应的数据包都会被这个方法处理
def response(flow):
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        use_unicode=True)
    cursor = connect.cursor()

    insert_time = str(datetime.date.today())
    rule = re.compile('(keyword.*?)&')
    keywords = unquote(re.findall(rule,flow.request.url)[0])
    keywords = keywords.split('=')[-1]
    rule = re.compile('{"result":.*}')
    # 获取响应对象
    response = flow.response

    # # 实例化输出类
    # info = ctx.log.info
    # # 打印响应码
    # info(str(response.status_code))
    # # 打印所有头部
    # info(str(response.headers))
    # # 打印cookie头部
    # info(str(response.cookies))
    # # 打印响应报文内容
    # info(str(response.text))

    if len(re.findall(rule,str(response.text)))>0:
        data = json.loads(str(response.text))
        notes = jsonpath(data, '$.data.items[*]')
        for note in notes:
            description = ''.join(jsonpath(note, '$.note.desc'))
            id = ''.join(jsonpath(note, '$.note.id'))
            img_links = ''.join(jsonpath(note, '$.note.images_list[*].url_size_large'))
            # is_ads = jsonpath(note,'$.note.is_ads')[0]
            liked = jsonpath(note, '$.note.liked')[0]
            liked_count = jsonpath(note, '$.note.liked_count')[0]
            title = ''.join(jsonpath(note, '$.note.title'))
            type = ''.join(jsonpath(note, '$.note.type'))
            user_nickname = ''.join(jsonpath(note, '$.note.user.nickname'))
            user_id = ''.join(jsonpath(note, '$.note.user.userid'))
            post_url = 'https://www.xiaohongshu.com/discovery/item/{}'.format(id)
            cursor.execute(
                'insert ignore into xhs(id,keywords,title,type,liked,liked_count,description,img_links,user_nickname,user_id,insert_time,post_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (id,keywords,title,type,liked,liked_count,description,img_links,user_nickname,user_id,insert_time,post_url))
            connect.commit()




