import os

class Sign():
    def generate_signature(self,value):
        p = os.popen('node fuck-byted-acrawler.js %s' % value)
        return (p.readlines()[0]).strip()


class Params():
    def get_params(self,id,signature):
        params = {
            'ch_id': str(id),
            'count': '9',
            'cursor': '0',
            'aid': '1128',
            'screen_limit': '3',
            'download_click_limit': '0',
            '_signature': signature
        }
        return params
