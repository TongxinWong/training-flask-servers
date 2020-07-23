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
# 用于去除只出现一次的词
from collections import defaultdict
import re
import pandas as pd
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# 用于去除只是用一次的词，目前暂时没用到
# frequency = defaultdict(int)


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 使用百度停用词
stopwords = stopwordslist('./Model/baidu_stopwords.txt')

# 设置jieba停用词性
stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']  # 停用词性
# stop_flag = []

path = "./news_list"  # 文件夹目录
filesnames = os.listdir(path) #得到文件夹下的所有文件名称

# 依据文件名得到标题
def getFileName(filename):
    re.sub(r'.txt', '',  filename)
    return filename

# 获取目录下所有文件路径
def getFilePath(path, filenames):
    change_filenames = []
    for filename in filenames:
        filename = path + "/" + filename
        change_filenames.append(filename)

    print(change_filenames)
    return change_filenames

filePaths = getFilePath(path, filesnames)
print(filePaths)

# 对字段进行分词，用于检索
def tokenzation_str(query_line):
    result = []
    # 这里生成了一个迭代器，使用for循环提取其中信息
    querys = jieba.cut(query_line, HMM=True)
    for query in querys:
        if query not in stopwords:
            result.append(query)
    print(result)
    return result

# 对一篇新闻分词，去停用词, 用于模型制作
def tokenization(filename):
    result = []
    print(filename)
    with open(filename, 'r', encoding='utf8') as f:
        text = f.read()
        words = pseg.cut(text)
    print(text)
    print(words)
    # 去除停用词
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    print(result)
    # 去除只出现一次的词,暂时还未用上

    return result

# 根据文件名获取url
def get_url(filename):
    with open(filename, 'r', encoding='utf8') as f:

        lines = f.readlines()
        for line in lines:
            if "<url>" in line:
                url = re.findall(r".*<url>(.*)</url>", line)[0]
                return url

# 根据url获取dateTime和title
def get_info(news_url):
    parsed_res = urlparse(news_url)

    # 解析出host url
    host_url = parsed_res.netloc

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(news_url, headers=headers)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, "html.parser")

    text_title = soup.find('div', 'clearfix w1000_320 text_title')
    source = text_title.find('div', 'fl')


    # 文件名命名为标题名
    title = soup.find('h1').text
    # print(soup.find('div', 'f1').text)  会报错
    # 获取新闻时间
    datetime = source.text[0:16]
    # datetime = soup.find('div', 'f1').text.split("来源")[0]
    return title, datetime

# 获取对应的url列表csv文件
def get_url_list(filePaths):
    news_url_list = []

    for filePath in filePaths:
        print("尝试打开文本")
        with open(filePath, 'r', encoding='utf8') as f:
            print("打开文本成功")
            lines = f.readlines()
            for line in lines:
                if "<url>" in line:
                    url = re.findall(r".*<url>(.*)</url>", line)[0]
                    print(url)
                    news_url_list.append(url)
                    break
    print(len(news_url_list))
    print(news_url_list)
    dataframe = pd.DataFrame({'url': news_url_list})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    # dataframe.to_csv("news_url.csv", index=False, sep=',')
    dataframe.to_csv("news_list_url_test.csv", index=False, sep=',')
    print("保存结束")

# 获取模型
def GetModel():
    # 读取文章，作为corpus语料库
    corpus = []
    for each in filePaths:
        corpus.append(tokenization(each))
    print(len(corpus))
    print(corpus)

    # 建立词袋模型
    dictionary = corpora.Dictionary(corpus)
    print(dictionary)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]

    print(len(doc_vectors))
    print(doc_vectors)

    # 建立TF-IDF模型
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    print(len(tfidf_vectors))
    print(len(tfidf_vectors[0]))

    # 存储语料库
    # corpora.MmCorpus.serialize('/corpus.mm', corpus)
    # 保存模型
    tfidf_vectors.save("./Model/tfidf_vectors.model")
    # 保存字典
    dictionary.save("./Model/dictionary.dic")

# 获取对应的新闻信息
def Get_sample_news(query_line, dictionary, tfidf_vectors):
    url_list = []
    # 利用刚刚的词袋模型字典，将查询字符串映射到字典的向量空间，以进行下一步的相似度计算。
    query = tokenzation_str(query_line)
    query_bow = dictionary.doc2bow(query)
    print(len(query_bow))
    print(query_bow)

    # 构建相似度矩阵，并进行新文本向量query_bow与该矩阵的相似度计算。
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[query_bow]
    print(len(list(enumerate(sims))))
    print(list(enumerate(sims)))

    # 排序输出
    scores = sorted(enumerate(sims), key=lambda item: -item[1])  # 排序
    print(scores)
    print("前10条最大匹配概率及索引为：")
    items = []
    for i in range(0, 10):
        index = scores[i][0]
        url = get_url(filePaths[index])     # 得到对应url
        title, dateTime = get_info(url)     # 根据url得到新闻对应时间和标题
        # title = filesnames[index].split('.')[0]  # 获取不加后缀的文件名

        print(scores[i][1], index, "title:  ", title, "url:", url)  # 输出分值
        url_list.append(url)
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
    print(data)
    return data

# 初始资源加载函数
def load_source():
    print("加载资源中....")
    # 加载字典
    dictionary = corpora.Dictionary.load("./Model/dictionary.dic")
    # 加载模型
    tfidf_vectors = TfidfModel.load("./Model/tfidf_vectors.model")
    # 加载语料库
    # corpus = corpora.MmCorpus('/corpus.mm')
    # 加载url列表
    url_list = []
    # url_lists = csv.reader(open("news_list_url_test.csv", encoding='utf-8'))
    # print(url_lists)
    # for url in url_lists:
    #     url_list.append(url)
    print("加载完成")
    return dictionary, tfidf_vectors

# 获取模型
# GetModel()

# query_line = "高考考试成绩"
# dictionary, tfidf_vectors = load_source()
# # 根据模型测试
# Get_sample_news(query_line, dictionary, tfidf_vectors)
