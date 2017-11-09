# -*- coding:utf-8 -*-

import requests
import re
import urllib
import os
import time
from bs4 import BeautifulSoup
from urllib import request

start_url = "https://7777av.co/html/tupian/index.html"
channel_url = "https://7777av.co"

def getIndexText(start_url):
	index_html = requests.get(start_url)
	index_html.encoding = index_html.apparent_encoding
	index_soup = BeautifulSoup(index_html.text, "lxml")

	channels = index_soup.select("#main > div > div.pside > ul > li > a")

	for channel in channels:
		page_url = channel_url + channel.get('href')
		getChannelUrl(page_url)


def getChannelUrl(page_url):
	channel_html = requests.get(page_url)
	channel_html.encoding = channel_html.apparent_encoding
	channel_soup = BeautifulSoup(channel_html.text, "lxml")

	infos = channel_soup.select("#main > div > div.art_box > div > ul > li > a")

	for info in infos:
		info_url = channel_url + info.get('href')
		getInfoImg(info_url)

def getInfoImg(info_url):
	time.sleep(4)
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
	}
	info_html = requests.get(url=info_url, headers=headers)
	info_html.encoding = info_html.apparent_encoding
	info_soup = BeautifulSoup(info_html.text, "lxml")

	file_path = '/Users/donghao/Desktop/img/'
	
	if os.path.isdir(file_path):
		pass
	else:
		os.mkdir(file_path)

	h = "https:"
	imglist = info_soup.select("#main > div > div.art_box > div > p > img")
	
	x = 0
	for imgs in imglist:
		imgurl = h + imgs.get('src')
		urllib.request.urlretrieve(imgurl, file_path+'%s.jpg' % x)
		x += 1
		print(imgurl+"已保存...")

if __name__ == "__main__":
	getIndexText(start_url)


