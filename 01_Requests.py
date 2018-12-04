# -*- coding:utf-8 -*-

import requests

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