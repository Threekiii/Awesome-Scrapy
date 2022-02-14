# https://www.qimai.cn/app/comment/appid/592331499/country/cn
# 获取版本号

def get_version(date, app_name):
    # if date >= '' and date <= '':
    #     version = ''
    # elif date >= '' and date <= '':
    #     version = ''
    # elif date >= '' and date <= '':
    #     version = ''
    if app_name == 'B612咔叽':
        if date >= '2019-12-28 01:48:21' and date <= '2019-12-31 23:59:59':
            version = '8.14.5'
        elif date >= '2019-12-22 22:11:33' and date <= '2019-12-28 01:48:21':
            version = '8.14.3'
        elif date >= '2019-12-20 06:19:24' and date <= '2019-12-22 22:11:33':
            version = '8.14.2'
        elif date >= '2019-12-19 01:45:12' and date <= '2019-12-20 06:19:24':
            version = '8.14.1'
        elif date >= '2019-12-11 00:33:08' and date <= '2019-12-19 01:45:12':
            version = '8.13.1'
        elif date >= '2019-12-06 03:23:16' and date <= '2019-12-11 00:33:08':
            version = '8.13.0'
        elif date >= '2019-11-24 01:34:49' and date <= '2019-12-06 03:23:16':
            version = '8.12.0'
    elif app_name == '轻颜相机':
        if date >= '2019-12-17 18:14:24' and date <= '2019-12-31 23:59:59':
            version = '2.8.0'
        elif date >= '2019-12-06 19:08:54' and date <= '2019-12-17 18:14:24':
            version = '2.7.6'
        elif date >= '2019-12-02 22:41:47' and date <= '2019-12-06 19:08:54':
            version = '2.7.4'
        elif date >= '2019-11-27 23:50:02' and date <= '2019-12-02 22:41:47':
            version = '2.7.2'
    elif app_name == '一甜相机':
        if date >= '2019-12-29 21:03:05' and date <= '2019-12-31 23:59:59':
            version = '2.1.5'
        elif date >= '2019-12-24 00:26:16' and date <= '2019-12-29 21:03:05':
            version = '2.1.4'
        elif date >= '2019-12-21 21:03:02' and date <= '2019-12-24 00:26:16':
            version = '2.1.3'
        elif date >= '2019-12-12 02:06:46' and date <= '2019-12-21 21:03:02':
            version = '2.1.2'
        elif date >= '2019-11-29 17:11:54' and date <= '2019-12-12 02:06:46':
            version = '2.1.1'
    elif app_name == '崽崽Zepeto':
        if date >= '2019-12-18 04:44:56' and date <= '2019-12-31 23:59:59':
            version = '2.17.1'
        elif date >= '2019-12-16 08:47:42' and date <= '2019-12-18 04:44:56':
            version = '2.17.0'
        elif date >= '2019-11-01 06:42:28' and date <= '2019-12-16 08:47:42':
            version = '2.15.2'
    elif app_name == 'Faceu激萌':
        if date >= '2019-12-19 03:33:07' and date <= '2019-12-31 23:59:59':
            version = '5.4.5'
        elif date >= '2019-12-12 00:07:32' and date <= '2019-12-19 03:33:07':
            version = '5.3.9'
        elif date >= '2019-12-03 23:59:57' and date <= '2019-12-12 00:07:32':
            version = '5.3.8'
        elif date >= '2019-11-27 02:26:22' and date <= '2019-12-03 23:59:57':
            version = '5.3.7'
    elif app_name == '美颜相机':
        if date >= '2019-12-16 20:08:43' and date <= '2019-12-31 23:59:59':
            version = '9.1.60'
        elif date >= '2019-12-12 00:54:30' and date <= '2019-12-16 20:08:43':
            version = '9.1.40'
        elif date >= '2019-12-03 21:27:21' and date <= '2019-12-12 00:54:30':
            version = '9.1.20'
        elif date >= '2019-11-13 21:42:10' and date <= '2019-12-03 21:27:21':
            version = '9.1.20'
    else:
        version = ''

    return version
