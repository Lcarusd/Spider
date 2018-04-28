# -*- coding:utf-8 -*-

# =========================
# 	Name:requests库的使用
	
# =========================



import requests

def getHTMLText(url, kv):
	try:
		r = requests.get(url, timeout=30, headers=kv)
		r.raise_for_status() # 如果状态不是200，引发HTTPError异常
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "爬取失败!"

if __name__ == '__main__':
	kv = {'user-agent':'Mozilla/5.0'}
	url = input("请输入需要爬取的网址：")
	print(getHTMLText(url, kv))