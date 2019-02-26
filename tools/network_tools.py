# -*- coding:utf-8 -*-

import time

import requests

from settings import proxies
from tools.request_tools import request_tool

class NetworkTools(object):
    def is_url_status_to_get(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return True
        return False

    def request_get(self, url):
        # TODO:错误机制、随机请求头
        # time.sleep(1)
        resp = requests.get(url, headers={"User-agent": request_tool.get_random_ua()}, proxies=proxies)
        return resp

network_tool = NetworkTools()


