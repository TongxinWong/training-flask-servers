#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/7/21 1:01
#@Author  :LJ 
#@FileName: TextRank.py

#@Software: PyCharm
import csv
import jieba
import jieba.posseg as pseg
import os
from gensim import corpora, models, similarities
from gensim.models import TfidfModel, doc2vec
import re
import pandas as pd
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import numpy as np


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 使用百度停用词
stopwords = stopwordslist('./Model/baidu_stopwords.txt')

# 设置jieba停用词性
stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']


# 根据url列表获取新闻正文内容
def get_news_content(news_url):
    # 设置头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    response = requests.get(news_url, headers=headers)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, "html.parser")

    # 解析新闻正文
    main_contents = soup.find('div', 'box_con')

    try:
        contents = " "
        for para in main_contents.find_all('p'):
            contents += para.text
    except AttributeError:
        return ' '
    else:
        return contents

# 对字段进行分词，用于检索
def tokenzation_str(query_line):
    result = []
    # 这里生成了一个迭代器，使用for循环提取其中信息
    querys = jieba.cut(query_line, HMM=True)
    for query in querys:
        if query not in stopwords:
            result.append(query)

    return result

# 对获取的新闻内容分词，去停用词, 用于模型制作
def tokenization(content):
    result = []
    # 获取迭代分词
    words = pseg.cut(content)
    # 去除停用词
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)

    return result


# 根据url获取dateTime和title
def get_info(news_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(news_url, headers=headers)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, "html.parser")

    # 获取标题栏信息
    text_title = soup.find('div', 'clearfix w1000_320 text_title')
    source = text_title.find('div', 'fl')


    # 文件名命名为标题名
    title = soup.find('h1').text
    # print(soup.find('div', 'f1').text)  会报错
    # 获取新闻时间
    datetime = source.text[0:16]
    return title, datetime

# 获取对应的url列表csv文件
def get_url_list():
    # 加载url列表
    url_list = []
    with open('./Model/news_url.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for url in reader:
            url = url[0]
            if url != 'url':
                url_list.append(url)
    return url_list


# 获取模型
def GetModel(url_list):
    # 读取文章，作为corpus语料库
    corpus = []
    for url in url_list:
        content = get_news_content(url)
        corpus.append(tokenization(content))

    # 建立词袋模型
    dictionary = corpora.Dictionary(corpus)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]

    # 建立TF-IDF模型
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]

    # 存储语料库
    # corpora.MmCorpus.serialize('/corpus.mm', corpus)
    # 保存模型
    tfidf_vectors.save("./Model/tfidf_vectors.model")
    # 保存字典
    dictionary.save("./Model/dictionary.dic")

# 获取对应的新闻信息
def Get_sample_news(query_line, url_list, dictionary, tfidf_vectors):
    # 利用刚刚的词袋模型字典，将查询字符串映射到字典的向量空间，以进行下一步的相似度计算。
    query = tokenzation_str(query_line)
    query_bow = dictionary.doc2bow(query)

    # 构建相似度矩阵，并进行新文本向量query_bow与该矩阵的相似度计算。
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[query_bow]
    # print(len(list(enumerate(sims))))
    # print(list(enumerate(sims)))

    # 排序输出
    scores = sorted(enumerate(sims), key=lambda item: -item[1])  # 排序
    # 该条用于查看返回值 print(scores)

    items = []
    for i in range(0, 10):
        index = scores[i][0]    # 获得索引
        url = url_list[index]     # 得到对应url
        title, dateTime = get_info(url)     # 根据url得到新闻对应时间和标题

        item = {
            'url': url,
            'title': title,
            'dateTime': dateTime
        }
        items.append(item)
    # 返回前10条新闻地址
    data = {
        'items': items
    }

    return data

# 初始资源加载函数
def load_source():
    # 加载字典
    dictionary = corpora.Dictionary.load("./Model/dictionary.dic")
    # 加载模型
    tfidf_vectors = TfidfModel.load("./Model/tfidf_vectors.model")
    # 加载语料库
    # corpus = corpora.MmCorpus('/corpus.mm')
    return dictionary, tfidf_vectors


# 获取模型
# GetModel(url_list)


