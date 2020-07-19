# -*-coding: utf-8 -*-
"""
author: Tongxin Wong
create time: 2020-07-19
update time: 2020-07-19
"""

from flask import Flask, request, jsonify
import web

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
