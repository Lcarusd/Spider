# -*- coding:utf-8 -*-

import requests
import re
import time
from bs4 import BeautifulSoup

url = "https://book.douban.com/people/sunlove9786/collect"
urls = "https://book.douban.com/people/sunlove9786/collect?start=15&sort=time&rating=all&filter=all&mode=grid"

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Cookie':'bid=S3EIhFyG_u4; gr_user_id=86b0c2b8-5f81-493a-9cbf-7725c51d1339; viewed="5333562_2326403_3283546_1323345_24089050_3146174_25942191_26430928_4178907_3238803"; ll="118163"; _ga=GA1.2.504479495.1478321454; ue="1571239133@qq.com"; ps=y; dbcl2="145966625:yslUXQXhPUU"; ct=y; ap=1; _vwo_uuid_v2=FB5106C8C68355E51DC13B7B70533F92|afab7b50c2db14009031e2272d0c60a5; ck=Yk_M; __utmt=1; __utmt_douban=1; __utma=30149280.504479495.1478321454.1499658809.1499689524.111; __utmb=30149280.13.10.1499689524; __utmc=30149280; __utmz=30149280.1499658809.110.29.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.14596; __utma=81379588.1013403892.1478321454.1499658682.1499689762.29; __utmb=81379588.1.10.1499689762; __utmc=81379588; __utmz=81379588.1499689762.29.24.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/sunlove9786/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1499689762%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2Fsunlove9786%2F%22%5D; _pk_id.100001.3ac3=38e7a98d9bd281d1.1478321455.29.1499689762.1499658682.; _pk_ses.100001.3ac3=*; push_noty_num=0; push_doumail_num=0'
}

wb_data = requests.get(url, headers=headers)
time.sleep(4)
soup = BeautifulSoup(wb_data.text,'lxml')

booknames = soup.select("div.info > h2 > a")
abouts = soup.select("div.info > div.pub")
comments = soup.select("div.info > div.short-note > p")

for bookname, about, comment in zip(booknames, abouts, comments):
    data = {
        "bookname":bookname.get_text(),
        "about":about.get_text(),
        "comment":comment.get_text()
    }
    print(data)
