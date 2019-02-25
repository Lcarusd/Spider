# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class DoubanBookSpider(object):
    def __init__(self, user_name, collect="book", page_value=15):
        self.user_url = "https://{0}.douban.com/people/{1}/collect?start={2}&sort=time&rating=all&filter=all&mode=grid"\
            .format(collect, user_name, page_value)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}

    def page_count_spider(self):
        response = requests.get(self.user_url, headers=self.headers)
        print(response.status_code)


stogievika = DoubanBookSpider("stogievika")
stogievika.page_count_spider()
