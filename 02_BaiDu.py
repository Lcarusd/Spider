# -*- coding:utf-8 -*-

import requests

input_keyword = input("请输入你要检索的关键字：")

try:
	kv = {'wd' : input_keyword}
	r = requests.get("http://www.baidu.com/s", params=kv)
	r.raise_for_status()
except:
	print "爬取失败！"