# -*- coding:utf-8 -*-

import time
import os
import queue
import threading

import requests


def paper_spider(i):
    while True:
        item = q.get()
        if item is None:
            print("线程%s退出！" % i)
            break
        time.sleep(2)

        file_dir = '/Users/donghao/Desktop/taoist_papers/'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        try:
            r = requests.get(item)
        except requests.exceptions.ConnectionError as e:
            raise e
        file_name = item.split('/')[-1].replace(".pdf", "")
        with open('{0}{1}.pdf'.format(file_dir, file_name), 'wb') as file:
            file.write(r.content)
        q.task_done()


if __name__ == '__main__':
    num_of_threads = 15
    q = queue.Queue()
    threads = []
    for i in range(1, num_of_threads + 1):
        t = threading.Thread(target=paper_spider, args=(i,))
        threads.append(t)
        t.start()

    # 任务源
    paper_list_url = "http://www.daoist.org/BookSearch/BookSearch/list009/0"
    paper_value_init = 1
    paper_urls_lt_10 = [paper_list_url + "0" + str(i) + ".pdf" for i in range(paper_value_init, 10)]
    paper_value_init = 10
    paper_urls_gt_10 = [paper_list_url + str(i) + ".pdf" for i in range(paper_value_init, 1000)]
    paper_urls = paper_urls_lt_10 + paper_urls_gt_10

    for item in paper_urls:
        time.sleep(0.5)
        q.put(item)

    print("工作已完成...")
    q.join()
    # 停止工作线程
    for i in range(num_of_threads):
        q.put(None)
    for t in threads:
        t.join()
    print(threads)
