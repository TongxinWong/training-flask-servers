#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/7/21 1:01
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
    print(data)
    # 获取收集到的url
    url_list = []
    print(data["items"])
    i = 1
    for item in data["items"]:
        # 读取200 条数据
        if (i%250!=0):
            if item["url"] not in url_list:
                print(item)
                url_list.append(item["url"])
                i += 1
        else:
            break
    print(url_list)
    print(len(url_list))
    # return data
    return url_list

# 获取新闻主要内容
def get_news_content(news_url):
    parsed_res = urlparse(news_url)
    # 解析出host url，用于图片绝对地址的生成
    host_url = parsed_res.netloc
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(news_url, headers=headers)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, "html.parser")
    news_info = {}
    # 添加新闻title
    news_info['title'] = soup.title.text

    text_title = soup.find('div', 'clearfix w1000_320 text_title')
    source = text_title.find('div', 'fl')
    # 添加新闻时间
    news_info['date'] = source.text[0:16]
    media_source = source.find('a')
    # 添加新闻来源
    news_info['media_source'] = media_source.text
    # 解析新闻正文
    main_contents = soup.find('div', 'box_con')
    contents = []
    for para in main_contents.find_all('p'):
        if para.string == None:
            # 处理图片或非p标签文字（图片标题或其他）
            if para.find('img') == None:
                # 处理非p标签文字
                para_content = {
                    'type': 'text',
                    'is_center': False,
                    'is_strong': False,
                    'text': para.text
                }
                # 判断是否居中
                if 'align' in para.attrs.keys():
                    if para.attrs['align'] == 'center':
                        para_content['is_center'] = True
                # 判断是否加粗
                if para.find('strong') != None:
                    para_content['is_strong'] = True
                contents.append(para_content)
            else:
                # 处理图片，提取url
                para_content = {
                    'type': 'img'
                }
                img_url = para.find('img').attrs['src']
                # 将图片的相对url转为绝对url
                if img_url.find(host_url) < 0:
                    img_url = 'http://' + host_url + img_url
                para_content['img_url'] = img_url
                contents.append(para_content)
        else:
            # 一般性的段落文字
            para_content = {
                'type': 'text',
                'is_center': False,
                'is_strong': False,
                'text': para.string
            }
            # 判断是否居中
            if 'align' in para.attrs.keys():
                if para.attrs['align'] == 'center':
                    para_content['is_center'] = True
            contents.append(para_content)
    news_info['contents'] = contents
    return news_info

def get_news_url(news_url):
    print(news_url)

    parsed_res = urlparse(news_url)

    # 解析出host url，用于图片绝对地址的生成
    host_url = parsed_res.netloc
    print(host_url)

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
            print("try")
            # 检查是否能正确通过这种方式获取标题
            filename = soup.find('h1').text
            print(filename)

            contents = " "
            for para in main_contents.find_all('p'):
                contents += para.text

        except AttributeError:
            print("文件读取格式出错!")
            return ' '
        except requests.exceptions.ReadTimeout:
            print("出现超时异常!")
            return ' '
        else:
            return news_url
    else:
        print("格式不符合要求!")
# 爬取数据
def get_news():
    url_list = []   # 用于获取所有url
    # 加载已有可用url列表
    url_arr = []
    with open('./Model/news_url.csv.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for url in reader:
            url = url[0]
            if url != 'url' and 'http://' not in url:
                url_arr.append(url)

    length = len(url_arr)
    print(url_arr)
    print(length)

    print("爬取中...")
    for i in range(0, len(tag_values)):
        tag_value = [tag_values[i]]
        url_list.extend(get_hot_news(tag_value))

    print(len(url_list))

    i = 0
    for news_url in url_list:
        i += 1
        if (i % 100) == 0:
            print("此时读取了", i, "次数据")
            # 延迟10s读取数据
            print("从方法中获取的url长度：", len(url_arr)-length)
            time.sleep(5)
        else:
            url = get_news_url(news_url)
            # 筛选出可解析的url
            if url != ' ' and url not in url_arr:
                url_arr.append(url)
    print("从方法中获取的url长度：", len(url_arr)-length)
    print(url_arr)

    print("一共读取数据：", i)
    save_url(url_arr)
    print("保存数据成功")

# 以下步骤用来保存url信息
def save_url(url_arr):
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'url': url_arr})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("./Model/news_url.csv", index=False, sep=',')

# 爬取数据
# get_news()
