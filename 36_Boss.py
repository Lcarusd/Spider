# -*- coding：utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = ["https://www.zhipin.com/c101200100/h_101200100/?query=Java&page={i}&ka=page-{i}".format(str(i, i)) for i in range(1,3,1)]


def getUrls(link):
	
	wb_data = requests.get(link)
	soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
	# print(soup)

	print(soup)

	# urls = soup.select("#main > div.job-box > div.job-list > ul > li > a")

	# print(urls)
	# for url in urls:
	# 	url = url.get("href")
	# 	print(url)

getUrls(url)