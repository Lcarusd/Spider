# -*- coding:utf-8 -*-

import json
import random
import time
import os

from huochaihe.tools import get_register_id, get_udid, requests_post
from settings import con_redis_0

class UserInfoSpider(object):
    def __init__(self):
        self.url  = "http://soa.matchbox.72zhe.com/v1/user/info"
        self.data = {}

    def get_uid_task(self):
        if con_redis_0.llen("huochaihe_tasks_1") != 0:
            value_task = con_redis_0.lpop("huochaihe_tasks_1")
            return value_task.decode("utf-8")
        else:
            return None

    def get_random_account(self):
        length = con_redis_0.llen("huochaihe_account")
        account = con_redis_0.lindex('huochaihe_account', random.randint(0, length - 1))
        return account.decode("utf-8")


    def mix_data(self):
        account = eval(self.get_random_account())
        value_task = self.get_uid_task()
        if not value_task:
            return False

        self.data = {
            "source": "APP",
            "uid": account["user_id"],
            "register_id": get_register_id(),
            "platform": "IOS",
            "udid": get_udid(),
            "user_id": value_task,
            "version": "4.10.5",
            "token_key": account["token_key"]
        }
        resp = requests_post(self.url, self.data)
        return resp

    def start_process_data(self):
        resp = self.mix_data()
        content = json.loads(resp.content)

        if content["error_code"] == "0":
            print(content)
            try:
                con_redis_0.rpush("huochaihe_user_info", str(content["data"]))
            except:
                raise
            con_redis_0.rpush("huochaihe_user_id", content["data"]["user_id"])


        if content["error_code"] != "0":
            content.update({
                "requests_account":self.data["uid"],
                "task_user_id":self.data["user_id"]})
            log_msg = "[{0}]:{1}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), content)
            print(content)
            with open(os.getcwd() + "/huochaihe/huochaihe.log", mode="a") as f:
                f.write(log_msg + "\n")

    def clear_param(self):
        self.data = {}

def main():
    # for _ in range(con_redis_0.llen("huochaihe_tasks_1") - 1):
    for _ in range(5):
        try:
            uis = UserInfoSpider()
            uis.start_process_data()
            uis.clear_param()
        except Exception as e:
            log_msg = "[{0}]:{1}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), e)
            print(log_msg)
            with open(os.getcwd() + "/huochaihe/huochaihe.log", mode="a") as f:
                f.write(log_msg + "\n")

            main()

if __name__ == "__main__":
    main()



