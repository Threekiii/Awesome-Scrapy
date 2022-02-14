from urllib.parse import urlencode

class Function():
    def get_url_with_params(self,url,params):
        url += urlencode(params)
        return url