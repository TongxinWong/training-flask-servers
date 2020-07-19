# -*-coding: utf-8 -*-
"""
author: Tongxin Wong
create time: 2020-07-16
update time: 2020-07-16
"""

import cv2

def character_recognition(ocr_module, ocr_image_path):
    np_images = [cv2.imread(ocr_image_path)]

    results = ocr_module.recognize_text(
        images=np_images,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        visualization=False,  # 是否将识别结果保存为图片文件；
        box_thresh=0.5,  # 检测文本框置信度的阈值；
        text_thresh=0.5)  # 识别中文文本置信度的阈值；

    data = results[0]['data']
    text_count = len(data)
    text_list = []
    for info in data:
        text_list.append(info['text'])

    res = {
        'data': {
            'text_count': text_count,
            'text': text_list
        }
    }
    return res
