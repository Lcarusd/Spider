# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 分析纽约热门景点并可视化

page_step = 15

url = 'https://www.tripadvisor.cn/Attractions-g60763-Activities-oa{0}-New_York_City_New_York.html#FILTERED_LIST'.format(15)

r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")

titles = soup.select("div.listing_title > a")
imgs = soup.select("img[width='180']")
cates = soup.select("div.p13n_reasoning_v2")

for title, img, cate in zip(titles, imgs, cates):
    print ("test")
    data = {
        "景点名称": title.get_text(),
        "标签 ": list(cate.stripped_strings),
    }
