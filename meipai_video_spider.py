# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

start_url = 'https://www.meipai.com/medias/hot'

# 抓取美拍前100的热门视频

# 获取主页分类列表url
def getHtmlText(start_url):
	index_wb_data = requests.get(start_url)
	index_soup = BeautifulSoup(index_wb_data.text, "lxml")
	
	channels = index_soup.select("#footerWrap > div.footer.clearfix > div.rw30.footer-content-left-wrap.fl.clearfix > div > span")
	
	for channel in channels:
		page_url = start_url + channel.get('data-href')
		# print(page_url)
		getUserText(page_url)

# 获取详情页url
def getUserText(page_url):
	user_wb_data = requests.get(page_url)
	user_soup = BeautifulSoup(user_wb_data.text, "lxml")
	
	users = user_soup.select("#mediasList > li > div > p > a")
	
	for user in users:
		user_url = start_url + user.get('href')
		getUserInfo(user_url)

# 解析并提取数据
def getUserInfo(user_url):
	info_wb_data = requests.get(user_url)
	info_soup = BeautifulSoup(info_wb_data.text, "lxml")

	title = info_soup.select("#rightUser > h3 > a")[0].text
	desc = info_soup.select("#rightUser > p")[0].text if info_soup.find_all('p') else None
	print({'title':title, 'desc':desc})

if __name__ == "__main__":
	getHtmlText(start_url)
