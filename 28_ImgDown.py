#-*-coding:utf-8-*-

import re
import requests
import os


class Spider:
    def savePageInfo(self, _url, _position, _regX):

        # 要爬的网址
        url = _url
        # 本地地址 
        position = _position
        # 获取网页源代码
        html = requests.get(url).text

        # 正则
        regX = _regX

        pic_url = re.findall(regX,html,re.S)

        i = 0
        for each in pic_url:
            pic = requests.get( each )
            print(url + each)
            
            # 如果文件夹不存在，则创建一个文件夹
            if not os.path.isdir(position):
                os.makedirs(position)

            fp = open( position+str(i)+'.jpg', 'wb' )
            fp.write(pic.content)
            fp.close()
            i+=1

#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝网页爬取图片＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

position_end = ''

# 要爬的网址
url = 'http://www.umei.cc/' + position_end

# 本地地址
position = '/Users/donghao/Desktop/1/' + position_end

# 正则
regX = '_blank\'><img src=(.*?) t'

#参数 url, 储存位置, 爬取的正则
spider = Spider()
spider.savePageInfo(url, position, regX)
