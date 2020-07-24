# -*-coding: utf-8 -*-
"""
author: Tongxin Wong, Jie Liu
create time: 2020-07-19
update time: 2020-07-24
"""

from flask import Flask, request, jsonify
import web
import TextRank
import opinion_perception

app = Flask(__name__)

# 加载字典
# 加载模型
dictionary, tfidf_vectors = TextRank.load_source()
# 加载url列表
url_list = TextRank.get_url_list()

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
    data = TextRank.Get_sample_news(query_line, url_list, dictionary, tfidf_vectors)
    return jsonify(data)

@app.route('/api/update_hot_topic', methods=['POST'])
def update_hot_topic():
    opinion_perception.update_hot_topic()
    # 因为上面函数的执行时间可能过长，nginx会返回502
    data = {
        'code': 200
    }
    return jsonify(data)

@app.route('/api/hot_topic', methods=['GET'])
def hot_topic():
    data = opinion_perception.get_classified_hot_topic()
    return jsonify(data)

@app.route('/api/news_comment', methods=['GET'])
def news_comment():
    newsid = request.args.get('newsid')
    data = opinion_perception.get_news_comment(newsid)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
