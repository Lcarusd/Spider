# -*- coding:utf-8 -*-

"""
解决各种报错问题，包括导入报错
"""

from multiprocessing import Pool
from channel_exact import channel_list
from pager_parsing import get_links_from

def get_all_links_from(channel):
    for i in range(1, 100):
        get_links_from(channel, i)


if __name__ == 'main':
    pool = Pool()
    pool.map(get_all_links_from, channel_list.split())


