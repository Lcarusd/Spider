# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import time
import pymysql
from channel import channel    # 开始爬取的链接
import random
from multiprocessing import Pool

print("=========================开始建立数据库连接准备工作=========================")
# 创建连接对象
conn = pymysql.connect(user="root", password="19950925", database="DoubanTest", charset="utf8mb4")
# 创建游标
cur = conn.cursor()
# 若数据库中存在allbooks数据表则删除
cur.execute('DROP TABLE IF EXISTS allbooks')
# 创建新的数据表allbooks
sql = """CREATE TABLE allbooks(
    title char(255) not null,
    -- scor char(255),
    -- author char(255),
    -- price char(255),
    -- time char(255),
    -- publish char(255),
    -- person char(255),
    -- yizhe char(255),
    detil char(255),
    scor char(255),
    tag char(255)
)"""
cur.execute(sql)
print("=========================数据库连接准备工作建立完毕=========================")


# 提取评价人数的函数，如果评价人数少于十人，按十人处理
def ceshi_person(person):
    try:
        person = int(person.get_text().split()[0][1:len(person.get_text().split()[0])-4])
    except ValueError:
        person = int(10)
        return person

#分情况提取价格的函数，用正则表达式找到含有特殊字符的信息，并换算为“元”
def ceshi_priceone(detil):
    price = detil.get_text().split("/",4)[4].split()
    
    if re.match("USD", price[0]):
        price = float(price[1]) * 6
    elif re.match("CNY", price[0]):
        price = price[1]
    elif re.match("\A$", price[0]):
        price = float(price[1:len(price)]) * 6
    else:
        price = price[0]
    return price

def ceshi_pricetwo(detil):
    price = detil.get_text().split("/",3)[3].split()
    
    if re.match("USD", price[0]):
        price = float(price[1]) * 6
    elif re.match("CNY", price[0]):
        price = price[1]
    elif re.match("\A$", price[0]):
        price = float(price[1:len(price)]) * 6
    else:
        price = price[0]
    return price

def startSpider(url):
    
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
    
    # 从链接中抽取标签抽取标签信息，然后存储
    tag = url.split("?")[0].split("/")[-1]

    # 抓取作者、出版社等信息，稍后用split()在抽取细节信息
    detils = soup.select("#subject_list > ul > li > div.info > div.pub")
    # 抓取评分信息
    scors = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")
    # 抓取评价人数
    persons = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.pl")
    # 抓取书名
    titles = soup.select("#subject_list > ul > li > div.info > h2 > a")

    # 将抓取的标签信息，分离出来
    for detil,scor,person,title in zip(detils,scors,persons,titles):
        l = []
        try:
            # author = detil.get_text().split("/",4)[0].split()[0]
            # yizhe = detil.get_text().split("/",4)[1]
            # publish = detil.get_text().split("/",4)[2]
            # time = detil.get_text().split("/",4)[3].split()[0].split("-")[0]
            
            # 因价格单位不同意使用价格单位，将他们换算成元
            # price = ceshi_priceone(detil)
            # 有些书评价人数少于10人，爬取过程会出错，用此函数来处理
            # person = ceshi_person(person)
            # 有些书没有评分，为避免错误，将此情况设置为空
            scor  = scor.get_text() if True else ""

            title = title.get_text().split()[0]

            detil = detil.get_text().split()[0]

            print({title,detil,scor,tag})
        
        # 当没有译者信息时，会出现IndexError，分开处理此情况
        except IndexError:
            try:
                # author = detil.get_text().split("/",3)[0].split()[0]
                # yizhe = ""
                # publish  = detil.get_text().split("/",3)[1]
                # time = detil.get_text().split("/",3)[2].split()[0].split("-")[0]

                # price = ceshi_pricetwo(detil)
                # person = ceshi_person(person)
                scor = scor.get_text() if True else ""
                
                title = title.get_text().split()[0]

                detil = detil.get_text().split()[0]

                print({title,detil,scor,tag})

            except (IndexError,TypeError):
                continue

    # l.append([title,scor,author,price,time,publish,person,yizhe,tag])
    l.append([title,detil,scor,tag])

    #执行sql语句，并用executemary()函数批量插入数据库中
    sql="INSERT INTO allbooks values(%s,%s,%s,%s)"
    cur.executemany(sql, l)
    conn.commit()






def main(channel):
    start = time.clock()    # 设置时钟，记录爬取时间

    for urls in channel.split():
        # 从channel中提取url信息，并组装成每一页的链接
        urlss = [urls + "?start={}&type=T".format(str(i) for i in range(0,60,20))]
        for url in urlss:
            print("正在采集页面数据:" + url)
            url_start = time.clock()
            startSpider(url)
            time.sleep(int(format(random.randint(0,9))))
            url_end = time.clock()
            print("页面已采集完成, 用时", url_end - url_start )

    # 计算采集时间和数据总量
    end = time.clock()
    print("采集共用时:", end - start)
    count = cur.execute('select * from allbooks')
    print("共有{}条记录.".format(count))

if __name__ == "__main__":
    pool = Pool()
    pool.map(main, channel.split())
    # 释放数据库链接
    if cur:
        cur.close()
    if conn:
        conn.close()






