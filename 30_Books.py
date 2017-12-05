# -*- coding；utf-8 -*-

import requests
import re
import time
import urllib.parse
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://book.douban.com/"
session = requests.session()


def get_Content(url):
    res = session.get(url, headers=headers)
    req = BeautifulSoup(res.content, 'lxml')
    book_content = req.findAll("div", {"class": "info"})
    return book_content


def get_items(book_content):
    global Tag
    for i in book_content:
        title = get_cleandata(i.find("a").get_text())
        tran = get_cleandata(i.find("div", {"class": "pub"}).get_text())
        rate = i.find("span", {"class": "rating_nums"})
        if not rate:
            rating = 0
        else:
            rating = float(get_cleandata(rate.get_text()))
        pl = int(''.join(re.split('\D+', get_cleandata(i.find("span", {"class": "pl"}).get_text()))))
        store(Tag, title, tran, rating, pl)


def get_cleandata(data):
    cleandata = re.sub("\n+", "", data)
    cleandata = cleandata.replace("(", "")
    cleandata = cleandata.replace(")", "")
    cleandata = re.sub(" +", "", cleandata)
    return cleandata


def get_Start(url):
    global Tag
    for i in Tag:
        a = [a * 20 for a in range(0, 100)]
        for r in a:
            time.sleep(3)
            values = {"type": "T", 'start': r}
            data = urllib.parse.urlencode(values)
            a = url + "tag/" + i + '?' + data
            content = get_Content(a)
            if not content:
                break
            else:
                get_items(content)


get_Start(url)
