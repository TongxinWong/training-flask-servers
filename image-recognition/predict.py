# -*-coding: utf-8 -*-
"""
author: Tongxin Wong Based on code from Internet
create time: 2020-07-14
update time: 2020-07-15
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from utils import image_processing
resize_width = 160
resize_height = 160

def face_recognition_image(face_detect, face_net, compared_face_path, idcard_face_path):
    # 初始化mtcnn人脸检测
    # face_detect = face_recognition.Facedetection()
    # 初始化facenet
    # face_net = face_recognition.facenetEmbedding(model_path)

    # 人脸数据是否有效
    valid = False

    compared_face = image_processing.read_image(compared_face_path)
    # 获取 判断标识 bounding_box crop_image
    bboxes, landmarks = face_detect.detect_face(compared_face)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")

    if bboxes == [] or landmarks == []:
        return valid, '未检测到人脸'
    elif len(bboxes) > 1:
        return valid, '检测到多张人脸'

    compared_face_images = image_processing.get_bboxes_image(compared_face, bboxes, resize_height, resize_width)
    compared_face_images = image_processing.get_prewhiten_images(compared_face_images)
    compared_face_emb = face_net.get_embedding(compared_face_images)

    idcard_face = image_processing.read_image(idcard_face_path)
    # 获取 判断标识 bounding_box crop_image
    bboxes, landmarks = face_detect.detect_face(idcard_face)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")

    if bboxes == [] or landmarks == []:
        return valid, '证件人脸识别错误，请重新上传'
    elif len(bboxes) > 1:
        return valid, '证件人脸识别错误，请重新上传'

    valid = True
    idcard_face_images = image_processing.get_bboxes_image(idcard_face, bboxes, resize_height, resize_width)
    idcard_face_images = image_processing.get_prewhiten_images(idcard_face_images)
    idcard_face_emb = face_net.get_embedding(idcard_face_images)

    compare_res = compare_embadding(compared_face_emb, idcard_face_emb)
    return valid, compare_res

def compare_embadding(compared_face_emb, idcard_face_emb, threshold=0.68):

    dist = np.sqrt(np.sum(np.square(np.subtract(compared_face_emb[0, :], idcard_face_emb[0, :]))))

    if (dist > threshold):
        return '认证失败'

    return '认证成功'