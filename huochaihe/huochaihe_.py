# -*- coding:utf-8 -*-

import json
import requests

url = "http://soa.matchbox.72zhe.com/v1/user/info"
login_url = "http://soa.matchbox.72zhe.com/v1/user/login"

data ={
	"source": "APP",
	"uid": "455565",
	"register_id": "13165ffa4e4f325953f",
	"platform": "IOS",
	"udid": "51d9218d5742c1873d9b0160f5aed80c4755949a",
	"user_id": "1221256",
	"version": "4.10.5",
	"token_key": "NDU1NTY1LOeZveiMtuWPtuibiywxNTcxMjM5MTMzQHFxLmNvbSw2ZGFmMztkNWQwM2NhODc3ODAwNTFlYzgzZWViZjFmNDRhYWQyZQ=="
}

login_data = {
	"mobile": "17127290868",
	"password": "12345678",
	"source": "APP",
	"register_id": "1114a89792ee9193c76",
	"platform": "IOS",
	"areacode": "86",
	"uid": "",
	"udid": "435a8ab8dc84acb2e8fa8cdb553c5a36f946dd01",
	"version": "4.10.5",
	"token_key": ""
}

headers = {
	"Content-Type":	"application/json",
	"Connection":"keep-alive",
	"X-HCH-KEY":"pbrle2t7qs9fu169wraezdu8pjgqyau4ovbv7qdkpqfci8ad",
	"Accept":"*/*",
	"User-Agent":"matchbox/4.10.5 (iPhone; iOS 11.4.1; Scale/2.00)",
	"Accept-Language":"zh-Hans-CN;q=1",
	"Content-Length":"291",
	"Accept-Encoding":"gzip, deflate",
}


# def get_proxies():
# 	PROXY_HOST = "http-dyn.abuyun.com"
# 	PROXY_PORT = "9020"
# 	PROXY_USER = "H604FTTV52G21P9D"
# 	PROXY_PASSWORD = "76B6725157C5FC22"
#
# 	PROXY_META = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
# 		"host": PROXY_HOST, "port": PROXY_PORT,
# 		"user": PROXY_USER, "pass": PROXY_PASSWORD, }
#
# 	proxies = {"http": PROXY_META, "https": PROXY_META, }
# 	return proxies
#
# resp = requests.post(url, data=json.dumps(data), headers=headers, proxies=get_proxies())
#
# print(json.loads(resp.content.decode("utf-8")))


"""
17127290868
17124267535
17124267523
17124267519
18445840934
13596827284
"""
# "1312959"用户有多也内容发布   "/v1/thread/user_new"

'''
验证码
'''

# import random
#
# udid_len = "51d9218d5742c1873d9b0160f5aed80c4755949a"
# reg_len = "13165ffa4e4f325953f"
# print(len(udid_len))
# print(len(reg_len))
#
# numbers = ["1", "2", "3", "4", "5"]
#
# numbers = [str(number) for number in range(10)]
# print(numbers)
#
# letters = [chr(i) for i in range(97, 123)]
# print(letters)
#
# a = numbers + letters
# print(a)
# b = "".join(random.choice(a)) for _ in range(0, len(reg_len) - 1)
# print(b)
