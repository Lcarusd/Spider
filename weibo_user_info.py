# -*- coding:utf-8 -*-

import os
import re
import json
import codecs
import sys
import traceback
from datetime import datetime
from datetime import timedelta

import requests
from lxml import etree
import jieba.analyse

# TODO:全文信息的爬取

class Weibo:
    cookie = {"Cookie": "your cookie"}  # 将your cookie替换成自己的cookie

    # Weibo类初始化
    def __init__(self, user_id, filter=1):
        self.user_id = user_id  # 用户id
        self.filter = filter    # 微博类别过滤
        self.username = ''  # 用户名
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数
        self.content_lst = []  #今日微博内容
        self.words = {} #微博内容词频统计

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print (u"用户名: " + self.username)
        except Exception as e:
            print("Error: ", e)

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"
            # 微博数
            str_wb = selector.xpath(
                "//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print (u"微博数: " + str(self.weibo_num))
            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print (u"关注数: " + str(self.following))
            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print (u"粉丝数: " + str(self.followers))
        except Exception as  e:
            print ("Error: ", e)
            traceback.print_exc()

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        today = datetime.now().date()

        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath("//input[@name='mp']")[0].attrib["value"])

            pattern = r"\d+\.?\d*"
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (datetime.now() - minute).strftime("%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]

                        self.publish_time.append(publish_time)
                        print (u"发布时间：" + publish_time)
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)").encode(sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        self.weibo_content.append(weibo_content)
                        self.content_lst.append(weibo_content)
                        print(u"微博内容：" + weibo_content)
                        # 词频统计
                        # word_list = jieba.analyse.extract_tags(weibo_content)
                        # for word in word_list:
                        #     if word in self.words:
                        #         self.words[word] += 1
                        #     else:
                        #         self.words[word] = 1
                        # 点赞数
                        print (info[i].xpath("div/a/text()"))
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid = re.findall(pattern, str_zan, re.M)
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        # 转发数
                        retweet = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, retweet, re.M)
                        retweet_num = int(guid[0])
                        self.retweet_num.append(retweet_num)
                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        comment_num = int(guid[0])
                        self.comment_num.append(comment_num)

                        self.weibo_num2 += 1

            before_10 = sorted(self.words.items(), key=lambda item:item[1], reverse=True)
            for i in before_10:
                print (i)

            if not self.filter:
                print (u"共" + str(self.weibo_num2) + u"条微博")
            else:
                print (u"共" + str(self.weibo_num) + u"条微博，其中" + str(self.weibo_num2) + u"条为原创微博")
        except Exception as e:
            print ("Error: ", e)
            traceback.print_exc()

    # 将爬取的信息写入文件
    def write_txt(self):
        # TODO:如果多人数据都存进同一个json文件需加一个list
        try:
            user_info = {}

            user_info["username"] = self.username
            user_info["user_id"] = self.user_id
            user_info["weibo_num"] = self.weibo_num
            user_info["following"] = self.following
            user_info["followers"] = self.followers

            if self.filter:
                user_info["weibo_type"] = 1 # 1值代表原创微博，0值代表所有微博
            else:
                user_info["weibo_type"] = 0

            detail_list = []
            for i in range(1, self.weibo_num2 + 1):
                detail = {}
                detail["content"] = self.weibo_content[i - 1]
                detail["release_time"] = str(self.publish_time[i - 1])
                detail["like_number"] = self.up_num[i - 1]
                detail["forwarding_number"] = self.retweet_num[i - 1]
                detail["comments_number"] = self.comment_num[i - 1]
                detail_list.append(detail)

            user_info["detail_list"] = detail_list

            file_dir = os.path.split(os.path.realpath(__file__))[0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%s" % self.username + ".json"
            with codecs.open(file_path, 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(user_info, ensure_ascii=False))
            print (u"微博写入文件完毕，保存路径:" + file_path)
        except Exception as e:
            print ("Error: ", e)
            traceback.print_exc()

    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.write_txt()
        except Exception as e:
            print ("Error: ", e)


def main(user_id, filter):
    try:
        wb = Weibo(user_id, filter)
        wb.start()
    except Exception as e:
        print ("Error: ", e)
        traceback.print_exc()


if __name__ == "__main__":
    user_id = ""  # 可以改成任意合法的用户id（爬虫的微博id除外）
    filter = 1  # 0表示爬取全部微博，1表示只爬取原创微博
    main(user_id, filter)
