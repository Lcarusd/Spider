# -*- coding:utf-8 -*-

import urllib
import re
import os
from urllib import request
from multiprocessing import Pool

# 获取页面数据
# def getHtml(url):
# 	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# 	page = urllib.request.Request(url=url, headers=headers)
# 	html = urllib.request.urlopen(page).read()
# 	html = html.decode('utf-8')
# 	# return html
# 	getImg(html)

# 将页面图片保存到本地
def getImg(html):
	reg = r'src="(.*\.jpg)"'
	imgre = re.compile(reg)
	imglist = re.findall(imgre, html)
	
	file_path = '/Users/donghao/Desktop/img/'
	
	if os.path.isdir(file_path):
		pass
	else:
		os.mkdir(file_path)

	x = 0
	for imgurl in imglist:
		urllib.request.urlretrieve(imgurl, file_path+'%s.jpg' % x)
		x += 1
	return imglist

# if __name__ == "__main__":
# 	url = 'https://www.pinterest.com/miki1395/your-pinterest-likes/'
# 	pool = Pool()
# 	pool.map(getHtml(url))

html = "/Users/donghao/Desktop/Pinterest.htm"
getImg(html)



