# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


url = "http://china.baixing.com/gongzuo/?src=new-home-nav"

headers = {
        'User-Agrnt' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text.encode("utf-8"), "lxml")
print(soup)




