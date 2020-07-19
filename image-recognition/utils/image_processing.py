# -*-coding: utf-8 -*-
"""
author: Tongxin Wong Based on code from Internet
create time: 2020-07-14
update time: 2020-07-14
"""

import cv2
import numpy as np

def get_prewhiten_image(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y

def image_normalization(image,mean=None,std=None):
    # 不能写成:image=image/255
    image = np.array(image, dtype=np.float32)
    image = image / 255.0
    if mean is not None:
        image=np.subtract(image, mean)
    if std is not None:
        np.multiply(image, 1 / std)
    return image

def get_prewhiten_images(images_list,normalization=False):
    out_images=[]
    for image in images_list:
        if normalization:
            image=image_normalization(image)
        image=get_prewhiten_image(image)
        out_images.append(image)
    return out_images

def read_image(filename, resize_height=None, resize_width=None, normalization=False,colorSpace='RGB'):
    '''
    读取图片数据,默认返回的是uint8,[0,255]
    :param filename:
    :param resize_height:
    :param resize_width:
    :param normalization:是否归一化到[0.,1.0]
    :param colorSpace 输出格式：RGB or BGR
    :return: 返回的图片数据
    '''

    bgr_image = cv2.imread(filename)
    # bgr_image = cv2.imread(filename,cv2.IMREAD_IGNORE_ORIENTATION|cv2.IMREAD_COLOR)
    if bgr_image is None:
        print("Warning:不存在:{}", filename)
        return None
    if len(bgr_image.shape) == 2:  # 若是灰度图则转为三通道
        print("Warning:gray image", filename)
        bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2BGR)

    if colorSpace=='RGB':
        image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # 将BGR转为RGB
    elif colorSpace=="BGR":
        image=bgr_image
    else:
        exit(0)
    # show_image(filename,image)
    # image=Image.open(filename)
    image = resize_image(image,resize_height,resize_width)
    image = np.asanyarray(image)
    if normalization:
        image=image_normalization(image)
    # show_image("src resize image",image)
    return image

def resize_image(image,resize_height, resize_width):
    '''
    :param image:
    :param resize_height:
    :param resize_width:
    :return:
    '''
    image_shape=np.shape(image)
    height=image_shape[0]
    width=image_shape[1]
    if (resize_height is None) and (resize_width is None):# 错误写法：resize_height and resize_width is None
        return image
    if resize_height is None:
        resize_height=int(height*resize_width/width)
    elif resize_width is None:
        resize_width=int(width*resize_height/height)
    image = cv2.resize(image, dsize=(resize_width, resize_height))
    return image
def scale_image(image,scale):
    '''
    :param image:
    :param scale: (scale_w,scale_h)
    :return:
    '''
    image = cv2.resize(image,dsize=None, fx=scale[0],fy=scale[1])
    return image

def get_rect_image(image,rect):
    '''
    :param image:
    :param rect: [x,y,w,h]
    :return:
    '''
    shape=image.shape#h,w
    height=shape[0]
    width=shape[1]
    image_rect=(0,0,width,height)
    rect=get_rect_intersection(rect, image_rect)
    x, y, w, h=rect
    cut_img = image[y:(y+ h),x:(x+w)]
    return cut_img



def get_rects_image(image,rects_list,resize_height=None, resize_width=None):
    rect_images = []
    for rect in rects_list:
        roi=get_rect_image(image, rect)
        roi=resize_image(roi, resize_height, resize_width)
        rect_images.append(roi)
    return rect_images

def get_bboxes_image(image,bboxes_list,resize_height=None, resize_width=None):
    rects_list=bboxes2rects(bboxes_list)
    rect_images = get_rects_image(image,rects_list,resize_height, resize_width)
    return rect_images

def bboxes2rects(bboxes_list):
    '''
    将bboxes=[x1,y1,x2,y2] 转为rect=[x1,y1,w,h]
    :param bboxes_list:
    :return:
    '''
    rects_list=[]
    for bbox in bboxes_list:
        x1, y1, x2, y2=bbox
        rect=[ x1, y1,(x2-x1),(y2-y1)]
        rects_list.append(rect)
    return rects_list

def rects2bboxes(rects_list):
    '''
    将rect=[x1,y1,w,h]转为bboxes=[x1,y1,x2,y2]
    :param rects_list:
    :return:
    '''
    bboxes_list=[]
    for rect in rects_list:
        x1, y1, w, h = rect
        x2=x1+w
        y2=y1+h
        b=(x1,y1,x2,y2)
        bboxes_list.append(b)
    return bboxes_list

def scale_rect(orig_rect,orig_shape,dest_shape):
    '''
    对图像进行缩放时，对应的rectangle也要进行缩放
    :param orig_rect: 原始图像的rect=[x,y,w,h]
    :param orig_shape: 原始图像的维度shape=[h,w]
    :param dest_shape: 缩放后图像的维度shape=[h,w]
    :return: 经过缩放后的rectangle
    '''
    new_x=int(orig_rect[0]*dest_shape[1]/orig_shape[1])
    new_y=int(orig_rect[1]*dest_shape[0]/orig_shape[0])
    new_w=int(orig_rect[2]*dest_shape[1]/orig_shape[1])
    new_h=int(orig_rect[3]*dest_shape[0]/orig_shape[0])
    dest_rect=[new_x,new_y,new_w,new_h]
    return dest_rect
def get_rect_intersection(rec1,rec2):
    '''
    计算两个rect的交集坐标
    :param rec1:
    :param rec2:
    :return:
    '''
    cx1, cy1, cx2, cy2 = rects2bboxes([rec1])[0]
    gx1, gy1, gx2, gy2 = rects2bboxes([rec2])[0]
    x1 = max(cx1, gx1)
    y1 = max(cy1, gy1)
    x2 = min(cx2, gx2)
    y2 = min(cy2, gy2)
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)
    return (x1,y1,w,h)