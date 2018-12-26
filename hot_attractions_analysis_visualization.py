# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 分析纽约热门景点并可视化

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, "lxml")

titles = soup.select("div.listing_title > a")
imgs = soup.select("img[width='180']")
cates = soup.select("div.p13n_reasoning_v2")

for title, img, cate in zip(titles, imgs, cates):
    data = {
        "景点名称": title.get_text(),
        "标签 ": list(cate.stripped_strings),
    }
    # print data["景点名称"]
    print data["标签 "][0]
