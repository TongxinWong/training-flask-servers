#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/7/20 14:01
#@Author  :LJ 
#@FileName: TextRank.py

#@Software: PyCharm

import requests
import json
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import numpy as np
# 新闻信息
'''
时政 高层：210802,1001,14576,34948
财经 产经：210803,1004,413883
股票 能源：67815,71661
社会 法治：210804,1008,42510
国际 军事：210805,1011,1002
教科 文卫：210806,1006,1007,1013,14739
台湾 港澳：210807,14657,42272
观点 理论：210808,40531,1003
传媒 舆情：210809,14677,209043
体育 娱乐：22176,210810,14820,1012
电视 图片：210811,174585,1016
游戏 动漫：210812,40130,122366
环保 IT：1010,1009
家电 通信：41390,183008
食品 房产：215731,194441
人工智能：422228
微博快报 微博访谈：347079,347759
人民创投：405954
东京速递：368583
知识产权：179663
'''

# 使用的标签列表,不含图片频道
tag_values = ["210802,1001,14576,34948", "210803,1004,413883", "67815,71661",
              "210804,1008,42510", "210805,1011,1002", "210806,1006,1007,1013,14739",
              "210807,14657,42272", "210808,40531,1003, ""210809,14677,209043", "22176,210810,14820,1012",
              "210812,40130,122366", "1010,1009", "41390,183008", "215731,194441",
              "422228", "179663"]

# 根据标签提取出url
def get_hot_news(tag_values):
    # 爬取人民网热点新闻，参数为当前时间戳
    url = 'http://news.people.com.cn/210801/211150/index.js?_=' + str(int(round(time.time() * 1000)))

    # 设置浏览器用户代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    # 编码格式为utf-8
    response.encoding = 'utf-8'

    # 查询新闻的结点
    selected_node_list = []
    for value in tag_values:
        selected_node_list.extend(value.split(','))

    res_data = json.loads(response.text)
    all_news_list = res_data['items']

    selected_news_list = []
    for news in all_news_list:
        if news['nodeId'] in selected_node_list:
            selected_news_list.append(news)
    # 返回前二百五十条热点新闻
    data = {
        'items': selected_news_list[0:300]
    }

    # 获取收集到的url
    url_list = []

    i = 1
    for item in data["items"]:
        # 读取200 条数据
        if (i%250!=0):
            if item["url"] not in url_list:
                url_list.append(item["url"])
                i += 1
        else:
            break
    # return data
    return url_list

def get_news_url(news_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(news_url, headers=headers, timeout=5)       # 设置超时参数，5s则连接超时
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, "html.parser")

    # 获取正文内容
    main_contents = soup.find('div', 'box_con')

    # 解析新闻正文
    if main_contents!=None and main_contents.find_all('p')!=None:
        # 让获取的url都能在后面得到解析
        try:
            # 检查是否能正确通过这种方式获取标题
            filename = soup.find('h1').text

            contents = " "
            for para in main_contents.find_all('p'):
                contents += para.text
        # 无法有效解析信息
        except AttributeError:
            return ' '
        # 出现超时错误
        except requests.exceptions.ReadTimeout:
            return ' '
        else:
            return news_url

# 爬取数据
def get_news():
    url_list = []   # 用于获取所有url, 原始url
    url_arr = []       # 加载已有可用url列表
    with open('./Model/news_url_list.csv.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for url in reader:
            url = url[0]
            if url != 'url' and 'http://' not in url:
                url_arr.append(url)
    # 开始爬取...
    for i in range(0, len(tag_values)):
        tag_value = [tag_values[i]]
        url_list.extend(get_hot_news(tag_value))
    # 用于控制读取速率
    i = 0
    for news_url in url_list:
        i += 1
        if (i % 100) == 0:
            # 延迟10s读取数据
            time.sleep(5)
        else:
            url = get_news_url(news_url)
            # 筛选出可解析的url
            if url != ' ' and url not in url_arr:
                url_arr.append(url)
    # 保存url信息
    save_url(url_arr)


# 以下步骤用来保存url信息
def save_url(url_arr):
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'url': url_arr})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("./Model/news_url_list.csv", index=False, sep=',')

# 爬取数据
# get_news()

