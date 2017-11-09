# -*- coding:utf-8 -*-

# =========================
	Name:requests库的使用
	
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


# if __name__ == '__main__' 如何理解?
# __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。
# 一个 Python 源码文件除了可以被直接运行外，还可以作为模块（也就是库）被导入。