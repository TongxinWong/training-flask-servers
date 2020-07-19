# -*-coding: utf-8 -*-
"""
author: Tongxin Wong
create time: 2020-07-14
update time: 2020-07-16
"""

from flask import Flask, request, jsonify
from urllib.request import urlretrieve
import face_recognition
import predict
import paddlehub as hub
import image_ocr

app = Flask(__name__)

model_path = 'models/20180408-102900'
# 初始化mtcnn人脸检测
face_detect = face_recognition.Facedetection()
# 初始化facenet
face_net = face_recognition.facenetEmbedding(model_path)
# 加载移动端预训练模型
ocr_module = hub.Module(name='chinese_ocr_db_crnn_mobile')

@app.route('/api/fr/compare', methods=['POST'])
def compare():
    # 根据url下载证件照和待检测照片
    received_data = request.get_json()
    idcard_face_url = received_data['idcard_face_url']
    compared_face_url = received_data['compared_face_url']

    idcard_face_path = './static/images/idcard_face.' + idcard_face_url[-3:]
    urlretrieve(idcard_face_url, idcard_face_path)

    compared_face_path = './static/images/compared_face.' + compared_face_url[-3:]
    urlretrieve(compared_face_url, compared_face_path)

    # 进行人脸比对
    valid, res = predict.face_recognition_image(face_detect, face_net, compared_face_path, idcard_face_path)

    if valid:
        if res == '认证成功':
            data = {
                'code': 200,
                'status': 1,
                'info': res
            }
            return jsonify(data)
        else:
            data = {
                'code': 200,
                'status': 0,
                'info': res
            }
            return jsonify(data)
    else:
        data = {
            'code': 400,
            'info': res
        }
        return jsonify(data)

@app.route('/api/ocr', methods=['POST'])
def ocr():
    # 根据url下载待提取文字图片
    received_data = request.get_json()
    ocr_image_url = received_data['ocr_image_url']

    ocr_image_path = './static/images/ocr_image.' + ocr_image_url[-3:]
    urlretrieve(ocr_image_url, ocr_image_path)

    data = image_ocr.character_recognition(ocr_module, ocr_image_path)
    return jsonify(data)




if __name__ == '__main__':
    app.run()
