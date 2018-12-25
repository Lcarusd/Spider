#-*-coding:utf-8-*-

import re
import os

import requests
from bs4 import BeautifulSoup


class PlunderBeauty(object):
    def __init__(self):
        self.init_url = "http://www.umei.cc/"
        self.picture_tag_url = []

    def requests2parser(self, url, selector):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup.select(selector)

    def picture_tag_spider(self):
        tag = self.requests2parser(self.init_url, '#Nav > li:nth-of-type(10) > div')
        tag_obj_list = [i for i in tag[0].children][1:-1]
        for i in tag_obj_list:
            self.picture_tag_url.append(i['href'])

    def picture_tag_detail_spider(self):
        for i in self.picture_tag_url:
            tag = self.requests2parser(i, 'body > div.wrap > div.TypeList')
            pattern = re.compile(r'{0}(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                                 .format(self.init_url))
            for i in tag:
                url = re.findall(pattern, str(i.ul))
                print (url)

    def spider(self):
        pass

    def save_photo(self):
        file_dir = '/Users/donghao/Desktop/taoist_papers/'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)


if __name__ == "__main__":
    pb = PlunderBeauty()
    pb.picture_tag_spider()
    pb.picture_tag_detail_spider()
