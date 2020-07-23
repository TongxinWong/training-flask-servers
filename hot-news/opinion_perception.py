# -*-coding: utf-8 -*-
"""
author: Tongxin Wong
create time: 2020-07-23
update time: 2020-07-23
"""
import requests
import json
import time
import re
import paddlehub as hub

# 返回热点话题使用新浪（comment5评论页面的新闻列表数据channel=sh）的数据
# 新闻评论情感分析使用新浪评论数前20的社会新闻，获取新闻id后再请求评论数据进行分析
# 根据分析速度决定是否使用数据库保存已分析好的新闻数据

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}

# 返回热点话题
def get_hot_topic():
    # 新浪社会新闻url
    sina_news_url = 'http://comment5.news.sina.com.cn/hotnews/info?format=json&channel=sh&hotid=sh_day'
    sina_response = requests.get(sina_news_url, headers=headers)
    sina_response.encoding = 'GBK'
    json_res = json.loads(sina_response.text)
    hot_topic = []
    # 取出每个新闻数据的hot_count，title和time
    for news in json_res['result']['hotnews']:
        news_info = {}
        news_info['hot_count'] = news['hot_count']
        news_info['title'] = news['title']
        news_info['time'] = news['time']
        hot_topic.append(news_info)
        
    data = {
        'hot_topic': hot_topic
    }
    return data

# 返回新浪评论数前20的社会新闻，包含newsid
def get_top_comments_news():
    # 获取今日日期
    top_time = time.strftime('%Y%m%d', time.localtime())
    # 新浪评论前20社会新闻url
    sina_top_comments_url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=shxwpl&top_time=' + top_time + '&top_show_num=20&top_order=DESC&js_var=news_'
    sina_comments_response = requests.get(sina_top_comments_url, headers = headers)
    # 取出返回内容中的json数据
    json_res = json.loads(sina_comments_response.text[12:-2])
    top_comments_news = []
    # 取出新闻的title和newsid
    for news in json_res['data']:
        news_info = {}
        news_info['title'] = news['title']
        news_info['newsid'] = news['ext5'][3:]
        top_comments_news.append(news_info) 
    return top_comments_news

# 对传入的新闻评论列表进行分析得出正负面分类结果
# 返回值：正面1，中性0，负面-1
def comments_sentiment_classify(comments):
    # 加载senta模型 
    senta = hub.Module(name="senta_bilstm")
    probs = 0.
    # 模型输入
    input_content = {}
    # 热评列表
    hot_comments_list = comments['hot_comments']
    # 普通评论列表
    com_comments_list = comments['com_comments']
    # 计算评论数量，将热评数量x2（给予热评更高的权重）
    comments_num = len(hot_comments_list) * 2 + len(com_comments_list)
    # 如果评论数量为0，返回中性结果
    if comments_num == 0:
        return 0
    # 使用senta进行情感分析
    # 只有在有数据时才进行分析
    if len(hot_comments_list) != 0:
        input_content = {'text': hot_comments_list}
        hot_results = senta.sentiment_classify(data=input_content)
        for result in hot_results:
            probs += result['positive_probs'] * 2
    
    if len(com_comments_list) != 0:
        input_content = {'text': com_comments_list}
        com_results = senta.sentiment_classify(data=input_content)
        for result in com_results:
            probs += result['positive_probs']
    
    positive_probs = round(probs / comments_num, 2)
    
    # 根据不同的值返回分类结果
    if positive_probs > 0.55:
        return 1
    elif positive_probs < 0.45:
        return -1
    else:
        return 0

# 对新闻的评论情感分析感知舆情
def news_sentiment_classify(top_comments_news):       
    # 正面新闻
    pos_news = []
    # 一般新闻（中性）
    neu_news = []
    # 负面新闻
    neg_news = []
    # 评论请求url
    base_url = 'http://comment5.news.sina.com.cn/page/info?format=json&channel=sh&newsid='
    for news in top_comments_news:
        # 根据newsid获取新闻评论
        comments = {}
        # 热评列表
        hot_comments_list = []
        # 普通评论列表
        com_comments_list = []
        newsid = news['newsid']
        comments_url = base_url + newsid
        comments_response = requests.get(comments_url, headers=headers)
        json_res = json.loads(comments_response.text)
        # 取出普通评论和最热评论列表
        hotlist = json_res['result']['hot_list']
        cmntlist = json_res['result']['cmntlist']
        
        for hot_comment in hotlist:
            # 使用正则表达式去除[可爱]等表情
            content = re.sub('\[.*?\]', '', hot_comment['content'])
            hot_comments_list.append(content)
            
        for com_comment in cmntlist:
            content = re.sub('\[.*?\]', '', com_comment['content'])
            com_comments_list.append(content)
            
        comments['hot_comments'] = hot_comments_list
        comments['com_comments'] = com_comments_list
        # 对新闻评论进行情感分析
        classify_res = comments_sentiment_classify(comments)
        del news['newsid']
        news['comments'] = comments
        
        if classify_res == 1:
            pos_news.append(news)
        elif classify_res == 0:
            neu_news.append(news)
        elif classify_res == -1:
            neg_news.append(news)
    data = {
        'pos_news': pos_news,
        'neu_news': neu_news,
        'neg_news': neg_news
    }
    return data