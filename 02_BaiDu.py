# -*- coding:utf-8 -*-

import requests

input_keyword = input("请输入你要检索的关键字：")

try:
	kv = {'wd' : input_keyword}
	r = requests.get("http://www.baidu.com/s", params=kv)
	r.raise_for_status()
except:
	print "爬取失败！"

# ............................

def getHTMLText(url, kv):
	try:
		r = requests.get(url, timeout=30, headers=kv)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "爬取失败!"

if __name__ == '__main__':
	kv = {'user-agent':'Mozilla/5.0'}
	url = input("请输入需要爬取的网址：")
	print getHTMLText(url, kv)