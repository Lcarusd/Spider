# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import time
import pymysql
from channel import channel    # 开始爬取的链接
import random
from multiprocessing import Pool

# print("=========================开始建立数据库连接准备工作=========================")
# # 创建连接对象
# conn = pymysql.connect(user="root", password="19950925", database="DoubanTest", charset="utf8mb4")
# # 创建游标
# cur = conn.cursor()
# # 若数据库中存在allbooks数据表则删除
# cur.execute('DROP TABLE IF EXISTS allbooks')
# # 创建新的数据表allbooks
# sql = """CREATE TABLE allbooks(
#     书名 char(255) not null,
#     -- scor char(255),
#     -- author char(255),
#     -- price char(255),
#     -- time char(255),
#     -- publish char(255),
#     -- person char(255),
#     -- yizhe char(255),
#     detil char(255),
#     scor char(255),
#     descs char(255),
#     tag char(255)
# )"""
# cur.execute(sql)
# print("=========================数据库连接准备工作建立完毕=========================")

def pageSpider(url):
    
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
    
    # 书名
    titles = soup.select("#wrapper > h1 > span")
    # 作者
    detils = soup.select("#wrapper > #content > div > div > div > div > div > div#info")
    # # 评分信息
    # scors = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")
    # # 图书简介
    # descs = soup.select("#subject_list > ul > li > div.info > p")
    # # 从链接中抽取标签抽取标签信息，然后存储
    # tag = url.split("?")[0].split("/")[-1]

    for title, detil in zip(titles, detils):
        title = title.get_text()
        detil = detil.get_text().split()[1]
        # detil.strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
        print({detil})
    # 将抓取的标签信息，分离出来
    # for title,detil,scor,desc in zip(titles,detils,scors,descs):
    #     l = []
    #     try:
    #         title = title.get_text().split()[0] if True else ""
    #         detil = detil.get_text().split()[0] if True else ""
    #         scor  = scor.get_text().split()[0] if True else ""
    #         desc = desc.get_text().split()[0] if True else ""
    #         print({title,detil,scor,tag})
    #     except :
    #         continue

    # l.append([title,detil,scor,desc,tag])

    #执行sql语句，并用executemary()函数批量插入数据库中
    # sql="INSERT INTO allbooks values(%s,%s,%s,%s,%s)"
    # cur.executemany(sql, l)
    # conn.commit()






def urlSpider(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
    pages = soup.select("#info > a")
    for page in pages:
        page_url = page.get("href")
        pageSpider(page_url)


def main(channel):
    for urls in channel.split():
        # 从channel中提取url信息，并组装成每一页的链接
        urlss = [urls + "?start={}&type=T".format(str(i) for i in range(0,40,20))]
        for url in urlss:            
            urlSpider(url)
            time.sleep(int(format(random.randint(0,9))))


if __name__ == "__main__":
    start = time.clock()    # 设置时钟，记录爬取时间

    pool = Pool()
    pool.map(main, channel.split())
    
    # 计算采集时间和数据总量
    end = time.clock()
    print("采集共用时:", end - start)
    # count = cur.execute('select * from allbooks')
    # print("共有{}条记录.".format(count))
    
    # 释放数据库链接
    # if cur:
    #     cur.close()
    # if conn:
    #     conn.close()






