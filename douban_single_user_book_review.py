# -*- coding:utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup


DOUBAN_ID = "user id"

url = "https://book.douban.com/people/{0}/collect".format(DOUBAN_ID)

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Cookie':'your cookie'
}

wb_data = requests.get(url, headers=headers)
time.sleep(4)
soup = BeautifulSoup(wb_data.text,'lxml')

booknames = soup.select("div.info > h2 > a")
abouts = soup.select("div.info > div.pub")
comments = soup.select("div.info > div.short-note > p")

for bookname, about, comment in zip(booknames, abouts, comments):
    print("\n")
