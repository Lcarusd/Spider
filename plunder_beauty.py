#-*-coding:utf-8-*-

import re
import os
import time
import random
import queue
import threading

import requests
from bs4 import BeautifulSoup


class PlunderBeauty(object):
    def __init__(self):
        self.init_url = "http://www.umei.cc/"
        self.num_of_threads = 50
        self.picture_tag_url = []
        self.page_sums_url = []
        self.picture_series_urls = []
        self.picture_series_queue = queue.Queue()
        self.piture_page_urls = []
        self.piture_page_queue = queue.Queue()
        self.piture_paths = []
        self.piture_path_queue = queue.Queue()

    def requests2parser(self, url, selector, type):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            return soup.select(selector)
        except:
            if type == 2:
                self.picture_series_queue.put(url)
            elif type == 3:
                self.piture_page_queue.put(url)

    def thread_pool(self, num_of_threads, tasks, queue, func):
        threads = []
        for thread_num in range(1, num_of_threads + 1):
            thread = threading.Thread(target=func, args=(thread_num,))
            threads.append(thread)
            thread.start()

        for item in tasks:
            queue.put(item)

        queue.join()
        for i in range(num_of_threads):
            queue.put(None)
        for thread_end in threads:
            thread_end.join()

    def picture_tag_spider(self):
        tag = self.requests2parser(self.init_url, '#Nav > li:nth-of-type(10) > div', 0)
        tag_list = [i for i in tag[0].children][1:-1]
        for i in tag_list:
            if i['href'] == u"http://www.umei.cc/p/gaoqing/cn/":    # TODO:测试用，仅保存国内分类tag
                self.picture_tag_url.append(i['href'])
        print (u"图片分类页面url爬取成功...")

    def tag_page_sums_spider(self):
        for i in self.picture_tag_url:
            page_sums = self.requests2parser(i, "body > div.wrap > div.NewPages > ul > li:nth-of-type(10) > a", 1)

            if len(page_sums) == 0:
                self.page_sums_url.append(i + "1.htm")
                continue

            page_sums_list = [i + str(page) + ".htm" for page in range(1, int(page_sums[0]['href'].split('.')[0]) + 1)]
            self.page_sums_url = self.page_sums_url + page_sums_list
        print (u"图片分类页所有页面url爬取成功...")

    def picture_series_spider(self, thread_num):
        while True:
            page = self.picture_series_queue.get()
            if page is None:
                print(u"线程 %s 退出！" % thread_num)
                break
            tag = self.requests2parser(page, 'body > div.wrap > div.TypeList', 2)
            pattern = re.compile(r'{0}(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                                 .format(self.init_url))
            for i in tag:
                url = re.findall(pattern, str(i.ul))
                self.picture_series_urls = list(set(self.picture_series_urls + url))
                print (u"去重后数量：" + str(len(self.picture_series_urls)))
            self.picture_series_queue.task_done()

    def piture_page_spider(self, thread_num):
        while True:
            item = self.piture_page_queue.get()

            if item is None:
                print(u"线程 %s 退出！" % thread_num)
                break

            piture_page_sums = self.requests2parser(item, "body > div.wrap > div.tag-page.l.oh > div.NewPages > ul > li:nth-of-type(1) > a", 3)

            for piture_page in range(1, int(re.findall(re.compile(r'[1-9]\d*'), piture_page_sums[0].text)[0]) + 1):
                if piture_page == 1:
                    self.piture_page_urls.append(item)
                    continue
                self.piture_page_urls.append(item[0:-4] + "_" + str(piture_page) + item[-4:])
                self.piture_page_urls = list(set(self.piture_page_urls))
                print (u"已抓取数量：" + str(len(self.piture_page_urls)))
            self.piture_page_queue.task_done()

    def get_piture_path_and_name(self, thread_num):
        while True:
            picture_page_url = self.piture_path_queue.get()
            if picture_page_url is None:
                print(u"线程 %s 退出！" % thread_num)
                break

            soup = None
            try:
                r = requests.get(picture_page_url, headers=headers)
                soup = BeautifulSoup(r.content, 'lxml')
            except:
                self.piture_path_queue.put(picture_page_url)

            picture_path = soup.select("#ArticleId0 > p > a > img")
            picture_name = soup.select("body > div.wrap > div.ArticleTitle > strong")[0].text
            if picture_path:
                self.piture_paths.append(picture_path[0]['src'])
            else:
                picture_path = soup.select("#ArticleId0 > p > img")
                self.piture_paths.append(picture_path[0]['src'])

            self.save_photo(picture_path[0]['src'], picture_name)

            self.piture_path_queue.task_done()

    def save_photo(self, picture, picture_name):
        file_path = '{0}/file/umei_picture'.format(os.getcwd())
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        try:
            r = requests.get(picture)
            print (picture)
            print (r.status_code)
            if r.status_code == 200:
                with open('{0}/{1}{2}.jpeg'.format(file_path, int(round(time.time() * 1000)), str(random.randint(1, 100))), 'wb') as file:
                    for chunk in r.iter_content():
                        file.write(chunk)
        except Exception as e:
            # HTTPConnectionPool(host='i1.umei.cc', port=80): Max retries exceeded with url: /img2012/2013/04/10LIGUI/014LIGUI20130315anna/000_4416_1.jpg (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x112a89d30>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))
            # https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url
            print ("[ErrorInfo]:" + str(e))


    def main(self):
        pb.picture_tag_spider()
        pb.tag_page_sums_spider()

        pb.thread_pool(self.num_of_threads, self.page_sums_url, self.picture_series_queue, self.picture_series_spider)
        pb.thread_pool(self.num_of_threads, self.picture_series_urls, self.piture_page_queue, self.piture_page_spider)
        pb.thread_pool(self.num_of_threads, self.piture_page_urls, self.piture_path_queue, self.get_piture_path_and_name)

if __name__ == "__main__":
    pb = PlunderBeauty()
    pb.main()
