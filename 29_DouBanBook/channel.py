# -*- coding:utf-8 -*-

import requests                       #用来请求网页
from bs4 import BeautifulSoup         #解析网页
import time          #设置延时时间，防止爬取过于频繁被封IP号
import re            #正则表达式库
import pymysql       #由于爬取的数据太多，我们要把他存入MySQL数据库中，这个库用于连接数据库
import random        #这个库里用到了产生随机数的randint函数，和上面的time搭配，使爬取间隔时间随机

url="https://book.douban.com/tag/?icn=index-nav"
wb_data=requests.get(url)                #请求网址
soup=BeautifulSoup(wb_data.text,"lxml")  #解析网页信息

tags=soup.select("#content > div > div.article > div > div > table > tbody > tr > td > a")
     #根据CSS路径查找标签信息，CSS路径获取方法，右键-检查-copy selector，tags返回的是一个列表

for tag in tags:    
	tag=tag.get_text()    #将列表中的每一个标签信息提取出来
	helf="https://book.douban.com/tag/"   
	  #观察一下豆瓣的网址，基本都是这部分加上标签信息，所以我们要组装网址，用于爬取标签详情页
	url=helf+str(tag)  
	print(url)    #网址组装完毕，输出

channel = '''
	https://book.douban.com/tag/小说
	https://book.douban.com/tag/外国文学
	https://book.douban.com/tag/文学
	https://book.douban.com/tag/随笔
	https://book.douban.com/tag/中国文学
	https://book.douban.com/tag/经典
	https://book.douban.com/tag/日本文学
	https://book.douban.com/tag/散文
	https://book.douban.com/tag/村上春树
	https://book.douban.com/tag/诗歌
	https://book.douban.com/tag/童话
	https://book.douban.com/tag/王小波
	https://book.douban.com/tag/杂文
	https://book.douban.com/tag/古典文学
	https://book.douban.com/tag/儿童文学
	https://book.douban.com/tag/名著
	https://book.douban.com/tag/张爱玲
	https://book.douban.com/tag/余华
	https://book.douban.com/tag/当代文学
	https://book.douban.com/tag/钱钟书
	https://book.douban.com/tag/外国名著
	https://book.douban.com/tag/鲁迅
	https://book.douban.com/tag/诗词
	https://book.douban.com/tag/茨威格
	https://book.douban.com/tag/米兰·昆德拉
	https://book.douban.com/tag/杜拉斯
	https://book.douban.com/tag/港台
	https://book.douban.com/tag/漫画
	https://book.douban.com/tag/绘本
	https://book.douban.com/tag/推理
	https://book.douban.com/tag/青春
	https://book.douban.com/tag/东野圭吾
	https://book.douban.com/tag/科幻
	https://book.douban.com/tag/言情
	https://book.douban.com/tag/悬疑
	https://book.douban.com/tag/武侠
	https://book.douban.com/tag/奇幻
	https://book.douban.com/tag/日本漫画
	https://book.douban.com/tag/韩寒
	https://book.douban.com/tag/耽美
	https://book.douban.com/tag/亦舒
	https://book.douban.com/tag/推理小说
	https://book.douban.com/tag/三毛
	https://book.douban.com/tag/网络小说
	https://book.douban.com/tag/安妮宝贝
	https://book.douban.com/tag/郭敬明
	https://book.douban.com/tag/穿越
	https://book.douban.com/tag/金庸
	https://book.douban.com/tag/轻小说
	https://book.douban.com/tag/阿加莎·克里斯蒂
	https://book.douban.com/tag/几米
	https://book.douban.com/tag/科幻小说
	https://book.douban.com/tag/青春文学
	https://book.douban.com/tag/魔幻
	https://book.douban.com/tag/张小娴
	https://book.douban.com/tag/幾米
	https://book.douban.com/tag/J.K.罗琳
	https://book.douban.com/tag/高木直子
	https://book.douban.com/tag/古龙
	https://book.douban.com/tag/沧月
	https://book.douban.com/tag/落落
	https://book.douban.com/tag/张悦然
	https://book.douban.com/tag/校园
	https://book.douban.com/tag/历史
	https://book.douban.com/tag/心理学
	https://book.douban.com/tag/哲学
	https://book.douban.com/tag/传记
	https://book.douban.com/tag/文化
	https://book.douban.com/tag/社会学
	https://book.douban.com/tag/艺术
	https://book.douban.com/tag/设计
	https://book.douban.com/tag/社会
	https://book.douban.com/tag/政治
	https://book.douban.com/tag/建筑
	https://book.douban.com/tag/宗教
	https://book.douban.com/tag/电影
	https://book.douban.com/tag/数学
	https://book.douban.com/tag/政治学
	https://book.douban.com/tag/回忆录
	https://book.douban.com/tag/中国历史
	https://book.douban.com/tag/思想
	https://book.douban.com/tag/国学
	https://book.douban.com/tag/音乐
	https://book.douban.com/tag/人文
	https://book.douban.com/tag/人物传记
	https://book.douban.com/tag/绘画
	https://book.douban.com/tag/戏剧
	https://book.douban.com/tag/艺术史
	https://book.douban.com/tag/佛教
	https://book.douban.com/tag/军事
	https://book.douban.com/tag/西方哲学
	https://book.douban.com/tag/二战
	https://book.douban.com/tag/近代史
	https://book.douban.com/tag/考古
	https://book.douban.com/tag/自由主义
	https://book.douban.com/tag/美术
	https://book.douban.com/tag/爱情
	https://book.douban.com/tag/旅行
	https://book.douban.com/tag/生活
	https://book.douban.com/tag/成长
	https://book.douban.com/tag/励志
	https://book.douban.com/tag/心理
	https://book.douban.com/tag/摄影
	https://book.douban.com/tag/女性
	https://book.douban.com/tag/职场
	https://book.douban.com/tag/美食
	https://book.douban.com/tag/教育
	https://book.douban.com/tag/游记
	https://book.douban.com/tag/灵修
	https://book.douban.com/tag/健康
	https://book.douban.com/tag/情感
	https://book.douban.com/tag/手工
	https://book.douban.com/tag/两性
	https://book.douban.com/tag/养生
	https://book.douban.com/tag/人际关系
	https://book.douban.com/tag/家居
	https://book.douban.com/tag/自助游
	https://book.douban.com/tag/经济学
	https://book.douban.com/tag/管理
	https://book.douban.com/tag/经济
	https://book.douban.com/tag/商业
	https://book.douban.com/tag/金融
	https://book.douban.com/tag/投资
	https://book.douban.com/tag/营销
	https://book.douban.com/tag/创业
	https://book.douban.com/tag/理财
	https://book.douban.com/tag/广告
	https://book.douban.com/tag/股票
	https://book.douban.com/tag/企业史
	https://book.douban.com/tag/策划
	https://book.douban.com/tag/科普
	https://book.douban.com/tag/互联网
	https://book.douban.com/tag/编程
	https://book.douban.com/tag/科学
	https://book.douban.com/tag/交互设计
	https://book.douban.com/tag/用户体验
	https://book.douban.com/tag/算法
	https://book.douban.com/tag/web
	https://book.douban.com/tag/科技
	https://book.douban.com/tag/UE
	https://book.douban.com/tag/通信
	https://book.douban.com/tag/交互
	https://book.douban.com/tag/UCD
	https://book.douban.com/tag/神经网络
	https://book.douban.com/tag/程序
'''

