### -*- coding:utf-8 -*-

import requests
import os
import re
import time
import pymongo
from multiprocessing import Pool
from urllib.Request import urllib2
from bs4 import BeautifulSoup

# 初始化爬取链接
url = "{}{}".format()

# SQL准备工作
client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
ceshiTable = ceshi['ceshiTable']

# 获取页面数据
def getHtml(url):
    # 反爬虫策略Cookie/User-Agent
    headers = {
        'User-Agrnt' : '',
        'Cookie' : ''
    }
    r = requests.get(url, timeout=30, headers=headers)
    # r.raise_for_status
    r.encoding = r.apparent_encoding
    return r.text

# DeepPage深度
def deepTh(html):
    # 解析页面，提取url链接，构造urls池
    urls = "".format().split()
    page = urllib.urljoin()
    getHtmlData(page)
    # 配置爬虫信息
    # 何时停止爬取，如何判断解析数据是否存在
    Tag =  soup.select()
    if Tag:
        # 继续爬取
    else:
        # 停止爬取
        pass

# 解析并且保存数据
def getHtmlData(html):
    soup = BeautifulSoup(html.text, "lxml")
   
   # Method_1
    Method_1 =  soup.select("")
    
    # Method_2
    reg = ""
    regc = re.compile(reg)
    re.finall(regc, html)
    
    # Method_3
    M_3  = response.xpath("/text()")[0].extract()
    
    # Save_1
    for M_1 in zip(Method_1):
        data = {
            'title' : M_1.text()
        }

    # Save_2 
    yield data
    ceshiTable.insert_one(data)
    # 反爬虫策略，set间隔时间
    time.sleep(4)

# SaveImg到本地
def SaveImg(html):
    reg = r'src="(.*\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    
    # 设置图片保存路径
    file_path = ""

    # 判断目标文件夹是否存在，若否就创建
    if os.path.isdir(file_path):
        pass
    else:
        os.mkdir(file_path)

    # 将图片遍历保存到目标文件夹
    x = 0
    for imgurl in imglist:
        urllib.request.urlretrieve(imhurl,file_path+'%s.jpg' % x)
        x += 1
    return imglist

# 读取本地文本写入数据库
def readText():
    path = "/Text.txt"
    with open(path, 'r')  as f :
        lines = f.readlines()
    for line in enumerate(lines):
        data = {
                
                }
    ceshiTable.insert_one(data)

# 主函数执行程序
if __name__ == "__main__":
    # 使用线程池，优化爬虫
    pool = Pool()
    pool.map(getHtml, url)

url = "{}{}".format()
