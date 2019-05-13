# -*- coding:utf-8 -*-

import json
import random
import time
import os
import logging
import requests

from huochaihe.tools import get_register_id, get_udid, requests_post, get_headers, get_proxies, logger
from settings import con_redis_0, con_redis_1

class UserInfoSpider(object):
    def __init__(self):
        self.url  = "http://soa.matchbox.72zhe.com/v1/user/info"

    def get_uid_task(self):
        return con_redis_0.get("user_id_count").decode("utf-8")

    def get_random_account(self):
        length = con_redis_0.llen("huochaihe_account")
        account = con_redis_0.lindex('huochaihe_account', random.randint(0, length - 1))
        return account.decode("utf-8")


    def mix_data(self):
        account = eval(self.get_random_account())
        value_task = self.get_uid_task()
        if not value_task:
            return False

        data = {
            "source": "APP",
            "uid": account["user_id"],
            "register_id": get_register_id(),
            "platform": "IOS",
            "udid": get_udid(),
            "user_id": value_task,
            "version": "4.10.5",
            "token_key": account["token_key"]
        }

        resp = requests.post(self.url, data=json.dumps(data), headers=get_headers(), proxies=get_proxies())
        return resp, value_task

    def start_process_data(self):
        resp, value_task = self.mix_data()
        try:
            content = json.loads(resp.content)
            print("用户信息抓取结果：\n%s" % content)
        except:
            return

        if content["error_code"] == "20000":
            con_redis_0.set("user_id_count", int(con_redis_0.get("user_id_count").decode("utf-8")) + 1)
            print("账号%s不存在..." % value_task)

        if not content["error_code"] == "0" and not content["error_code"] == "20000":
            logger(content)

        if content["error_code"] == "0":
            if not con_redis_0.exists(content["data"]["user_id"]):
                try:
                    con_redis_0.rpush("huochaihe_user_info", str(content["data"]))
                    con_redis_0.set("user_id_count", int(con_redis_0.get("user_id_count")) + 1)
                    con_redis_1.set(content["data"]["user_id"], 0)
                    print("用户信息抓取成功!")
                except:
                    raise

        print("*" * 100)

def main():
    uis = UserInfoSpider()
    for _ in range(100000):
        uis.start_process_data()


if __name__ == "__main__":
    main()



