# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
DouBanMovie = client['DouBanMovie']
KangRinpocheComment = DouBanMovie['KangRinpocheComment']


headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Cookie':'bid=S3EIhFyG_u4; gr_user_id=86b0c2b8-5f81-493a-9cbf-7725c51d1339; viewed="5333562_2326403_3283546_1323345_24089050_3146174_25942191_26430928_4178907_3238803"; ll="118163"; _ga=GA1.2.504479495.1478321454; ue="1571239133@qq.com"; ps=y; dbcl2="145966625:yslUXQXhPUU"; ct=y; ck=Yk_M; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1499737784%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F145966625%2F%22%5D; __utmt=1; _vwo_uuid_v2=FB5106C8C68355E51DC13B7B70533F92|afab7b50c2db14009031e2272d0c60a5; _pk_id.100001.4cf6=65beaec77ba011bf.1494327231.23.1499739047.1499579802.; _pk_ses.100001.4cf6=*; __utma=30149280.504479495.1478321454.1499735488.1499737774.113; __utmb=30149280.10.10.1499737774; __utmc=30149280; __utmz=30149280.1499658809.110.29.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.14596; __utma=223695111.504479495.1478321454.1499579438.1499737783.22; __utmb=223695111.0.10.1499737783; __utmc=223695111; __utmz=223695111.1499737783.22.21.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/145966625/; push_noty_num=0; push_doumail_num=0'
}

url = "https://movie.douban.com/subject/26606242/comments?status=P"
urls = ["https://movie.douban.com/subject/26606242/comments?start={}&limit=20&sort=new_score&status=P".format(str(i)) for i in range(20,6000,20)]

def getHTMLText(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, "lxml")

    time.sleep(3)

    unames = soup.select("div.comment > h3 > span.comment-info > a")
    utimes = soup.select("div.comment > h3 > span.comment-info > span.comment-time")
    ucomments = soup.select("div.comment > p")

    for uname, utime, ucomment in zip(unames, utimes, ucomments):
        data = {
            '用户名:':uname.get_text(),
            '评论时间:': utime.get_text(),
            '影评内容': ucomment.get_text()
        }
        KangRinpocheComment.insert_one(data)

getHTMLText(url)
for single_url in urls:
    getHTMLText(single_url)
