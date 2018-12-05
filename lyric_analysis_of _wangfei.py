# -*- coding:utf-8 -*-

import requests

class Lyrics_Spider(object):
    '''歌词爬取'''

    def request_param(self):
        headers = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        album_url = "https://music.163.com/#/artist/album?id=9621"
        s = requests.get(album_url, headers)
        print s.text


class Lyric_Analysis(object):
    '''歌词分析'''
    pass

if __name__ == "__main__":
    ls = Lyrics_Spider()
    ls.request_param()