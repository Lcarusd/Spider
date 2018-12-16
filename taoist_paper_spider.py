# -*- coding:utf-8 -*-

import time

import requests


# value init
paper_list_url = "http://www.daoist.org/BookSearch/BookSearch/list009/0"
paper_value_init = 1

# paper spider
for i in range(paper_value_init, 2000):
    paper_url = paper_list_url + str(i) + ".pdf"
    if i < 10:
        paper_url = paper_list_url + "0" + str(i) + ".pdf"

    try:
        r = requests.get(paper_url)
        with open('/Users/donghao/Desktop/test/{0}.pdf'.format(i), 'wb') as file:
            file.write(r.content)
        print "end spider paper {0}...".format(i)
        time.sleep(1)
    except Exception as e:
        print e
        break

# TODO:多线程下载代码
