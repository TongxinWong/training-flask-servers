# -*-coding: utf-8 -*-
"""
author: Tongxin Wong, Jie Liu
create time: 2020-07-19
update time: 2020-07-23
"""

from flask import Flask, request, jsonify
import web
import TextRank
import opinion_perception

app = Flask(__name__)

# 加载字典
# 加载模型
dictionary, tfidf_vectors = TextRank.load_source()

@app.route('/api/hot_news', methods=['POST'])
def hot_news():
    received_data = request.get_json()
    tag_values = received_data['tag_values']
    data = web.get_hot_news(tag_values)
    return jsonify(data)

@app.route('/api/news_content', methods=['POST'])
def news_content():
    received_data = request.get_json()
    news_url = received_data['news_url']
    data = web.get_news_content(news_url)
    return jsonify(data)
    
@app.route('/api/search', methods=['GET'])
def search_news():
    # 获取查询字段
    query_line = request.args.get("query")
    # 返回url
    data = TextRank.Get_sample_news(query_line, dictionary, tfidf_vectors)
    return jsonify(data)

@app.route('/api/hot_topic', methods=['GET'])
def hot_topic():
    data = opinion_perception.get_hot_topic()
    return jsonify(data)

@app.route('/api/sentiment_classify', methods=['GET'])
def sentiment_classify():
    data = opinion_perception.news_sentiment_classify(opinion_perception.get_top_comments_news())
    return jsonify(data)

if __name__ == '__main__':
    app.run()
