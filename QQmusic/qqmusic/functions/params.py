class Params():
    def get_playlist_params(self,page,categoryId):
        params = {
            'picmid': '1',
            'rnd': '0.3634810717772081',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'categoryId': categoryId,
            'sortId': '5',
            'sin': int(page) * 30 - 30,
            'ein': int(page) * 30 - 1,
        }
        return params

    def get_info_params(self,disstid):
        params = {
            'type': '1',
            'json': '1',
            'utf8': '1',
            'onlysong': '0',
            'new_format': '1',
            'disstid': disstid,
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0'
        }
        return params

    def get_vkey_params(self,mid):
        params = {
            '-': 'getplaysongvkey7256617694143965',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'data': '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5300386295","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}' % mid
        }
        return params

    def get_download_params(self,vkey):
        params = {
            'guid': '5300386295',
            'vkey': vkey,
            'uin': '0',
            'fromtag': '66'
        }
        return params

    def get_lyric_params(self,music_id):
        params = {
            'nobase64': 1,
            'musicid': music_id,
            '-': 'jsonp1',
            'g_tk': 5381,
            'loginUin': 0,
            'hostUin': 0,
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': 0,
            'platform': 'yqq.json',
            'needNewCode': 0,
        }
        return params

    def get_comment_params(self, music_id, page, last_comment_id):
        params = {
            'g_tk':5381,
            'loginUin':0,
            'hostUin':0,
            'format':'json',
            'inCharset':'utf8',
            'outCharset':'GB2312',
            'notice':0,
            'platform':'yqq.json',
            'needNewCode':0,
            'cid':205360772,
            'reqtype':2,
            'biztype':1,
            'topid': music_id,
            'cmd':8,
            'needmusiccrit':0,
            'pagenum':page,
            'pagesize':25,
            'lasthotcommentid':last_comment_id,
            'domain':'qq.com',
            'ct':24,
            'cv':10101010
        }
        return params