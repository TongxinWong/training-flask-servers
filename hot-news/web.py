# -*-coding: utf-8 -*-
"""
author: Tongxin Wong
create time: 2020-07-19
update time: 2020-07-19
"""

import requests
import json
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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
    # 返回前十条热点新闻
    data = {
        'items': selected_news_list[0:10]
    }
    return data

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
