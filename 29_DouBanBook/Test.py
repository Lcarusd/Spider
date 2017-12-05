# -*- coding:utf-8 -*-

import requests
import pymongo
import re
import os
import time
import urllib.parse
from bs4 import BeautifulSoup

url = "https://book.douban.com/tag/?icn=index-nav"
book_url = "https://book.douban.com"

headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		'Cookie':'bid=S3EIhFyG_u4; gr_user_id=86b0c2b8-5f81-493a-9cbf-7725c51d1339; viewed="5333562_2326403_3283546_1323345_24089050_3146174_25942191_26430928_4178907_3238803"; _pk_ref.%s.8290=%5B%22%22%2C%22%22%2C1495073726%2C%22https%3A%2F%2Fbook.douban.com%2Fsubject%2F26963900%2Fcomments%2Fnew%22%5D; _ga=GA1.3.504479495.1478321454; _pk_id.%s.8290=cda95c588b01aec9.1495073726.1.1495073734.1495073726.; ll="118163"; ue="1571239133@qq.com"; ps=y; ct=y; ap=1; dbcl2="145966625:fPfVXZOvfnw"; _ga=GA1.2.504479495.1478321454; _gid=GA1.2.1787530421.1500792445; ck=X-dw; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=8a690277-d1b4-40bf-8b7d-0bb90d3de9aa; gr_cs1_8a690277-d1b4-40bf-8b7d-0bb90d3de9aa=user_id%3A1; _vwo_uuid_v2=FB5106C8C68355E51DC13B7B70533F92|afab7b50c2db14009031e2272d0c60a5; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utma=30149280.504479495.1478321454.1500662337.1500792444.130; __utmb=30149280.21.10.1500792444; __utmc=30149280; __utmz=30149280.1500622090.127.36.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.14596'
	}

def getIndexText(url):
	
	html = requests.get(url=url, headers=headers)
	soup = BeautifulSoup(html.text, "lxml")
	
	channels = soup.select("#content > div > div.article > div > div > table > tbody > tr > td > a")
	
	for channel in channels:
		channel_url = book_url + channel.get('href')
		time.sleep(4)
		getChannelText(channel_url)


def getChannelText(channel_url):
	page_url = [data + "?start={}&type=T".format(str(i)) for i in range(0, 60, 20)]
	getInfoText(page_url)

def getInfoText(page_url):

	time.sleep(4)

	info_html = requests.get(url=page_url, headers=headers)
	info_soup = BeautifulSoup(info_html.text, "lxml")

	print(info_soup)

	names = info_soup.select("#subject_list > ul > li > div.info > h2 > a")
	infos = info_soup.select("#subject_list > ul > li > div.info > div.pub")
	grades = info_soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")
	descs = info_soup.select("#subject_list > ul > li > div.info > p")

	for name, info, grade, desc in zip(names, infos, grades, descs):
		data = {
			'name' : name.text
			# 'info' :
			# 'grade' :
			# 'desc' :
		}
		print(data)

if __name__ == "__main__":
	getIndexText(url)


