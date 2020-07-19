图像识别部分数据处理接口
===

### 人证核验

请求方式：POST
请求URL：http://120.25.24.74/api/fr/compare

请求数据格式：json

idcard_face_url：证件照链接

compared_face_url：待检测照片链接

```json
{
    "idcard_face_url": "https://s1.ax1x.com/2020/07/15/Uwq2wT.md.jpg",
    "compared_face_url": "https://s1.ax1x.com/2020/07/15/Uwb3rV.md.png"
}
```



返回数据格式：json
code状态码，200代表正常，400代表出错

1.正常返回:

```json
{
    "code": 200,
    "status": 1,
    "info": "认证成功"
}
```
或

```json
{
    "code": 200,
    "status": 0,
    "info": "认证失败"
}
```
2.异常返回

```json
{
	"code": 400,
	"info": "未检测到人脸"
}
```
或
```json
{
	"code": 400,
	"info": "检测到多张人脸"
}
```

或

```json
{
	"code": 400,
	"info": "证件人脸识别错误，请重新上传"
}
```

### OCR文字识别

请求方式：POST
请求URL：http://120.25.24.74/api/ocr

请求数据格式：json

ocr_image_url：待提取文字图片链接

```json
{
    "ocr_image_url": "https://s1.ax1x.com/2020/07/16/UBGjDe.jpg"
}
```

返回数据格式：json

```json
{
    "data": {
    "text_count": 2,
    "text": [
    "你好啊夏天",
    "喝一杯压压惊"
    ]
    }
}
```