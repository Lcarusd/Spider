# -*- coding:utf-8 -*-

"""
format方法
split的用法
以及[0]什么类型才有，是什么类型
"""

from bs4 import BeautifulSoup
import requests
import time
import pymongo

# 在最左边是在python 中对象的名称，后面的是在数据库中的名称
client = pymongo.MongoClient('localhost', 27017)    # 连接到mongo数据库
ceshi = client['ceshi']    # 创建数据库
url_list = ceshi['url_list']    # 创建数据表
item_info = ceshi['item_info']    # 创建数据表

# Spider 1
def get_links_from(channel, pages, who_sells=0):
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, "lxml")
    time.sleep(1)
    # td.t 没有这个就终止
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url' : item_link})
            print(item_link)
            # get_item_info(item_link)
    else:
        # It's the last page!
        pass

# Spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, "lxml")
    no_longer_exist = '404' in soup.find('script', type='text/javascript').get('src').spilt('/')
    if no_longer_exist:
        pass
    else:
        
        title = soup.title.text
        price = soup.select("span.price.c_f50")[0].text
        date = soup.select(".time")[0].text
        area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
        item_info.insert_one({'title':title, 'price':price, 'date':date, 'area':area, 'url':url})
        print({'title':title, 'price':price, 'date':date, 'area':area, 'url':url})





