# training-flask-servers
Flask servers for summer training in 2020

+ image-recognition：基于图像识别的人脸比对认证和OCR文字识别模块

  >使用[facenet](https://github.com/davidsandberg/facenet)预处理模型[20180408-102900](https://drive.google.com/open?id=1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz)，下载后解压到models文件夹

+ hot-news：社会新闻资讯查询及舆情感知（新闻评论情感分析）模块（主要新闻数据来自人民网和新浪网)

  > 更改新闻数据保存方式，由文本文件改为使用csv文件保存新闻链接
  >
  > hot-news/model_training文件夹下为使用PaddlePaddle进行情感分析模型训练的代码和[外卖评价数据集](https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/waimai_10k/waimai_10k.csv)以及[酒店评论数据集](https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/ChnSentiCorp_htl_all/ChnSentiCorp_htl_all.csv)，模型训练使用的是外卖评价数据集，包含4000条正向评论和7987条负向评论，acc在测试集上为0.845
  >
  > 项目使用百度的senta进行新闻评论的情感分析