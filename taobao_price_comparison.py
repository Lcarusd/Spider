# -*- coding:utf-8 -*-
import re

import requests

 
def get_html_text(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parse_page(products_infos, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            products_infos.append([price , title])
    except:
        pass


def print_product_list(products_infos):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for _ in products_infos:
        count = count + 1
        print(tplt.format(count, _[0], _[1]))


def main(product_name, depth=1):
    start_url = 'https://s.taobao.com/search?q=' + product_name
    products_infos = []
    for _ in range(depth):
        try:
            url = start_url + '&s=' + str(44 * _)
            html = get_html_text(url)
            parse_page(products_infos, html)
        except:
            continue
    print_product_list(products_infos)


main(product_name="牛奶", depth=2)
"""
参数说明:
product_name：商品名称
depth：页面深度
"""
