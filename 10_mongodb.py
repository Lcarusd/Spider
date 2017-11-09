# -*- coding:utf-8 -*-

import pymongo

# 连接数据库，并且创建数据库，数据表
client = pymongo.MongoClient('localhost', 27017)
walden = client['walden']
sheet_tab = walden['sheet_tab']

# 读取本地文本并且写入数据库
path = '/Users/donghao/PycharmProjects/Spider/walden.txt'
with open(path, 'r') as f:
    lines = f.readlines()
    for index, line in enumerate(lines):
        data = {
            'index':index,
            'line':line,
            'words':len(line.split()),
        }
        sheet_tab.insert_one(data)

# 将写入数据库的数据展示出来
for item in sheet_tab.find():
    print(item['line'])
for item in sheet_tab.find({'words':0}):
    print(item)