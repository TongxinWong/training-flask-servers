社会新闻资讯查询及舆情感知数据接口

### 请求新闻数据并根据选中标签进行筛选

#### 标签与value对应关系
+ 时政 高层：210802,1001,14576,34948
+ 财经 产经：210803,1004,413883
+ 股票 能源：67815,71661
+ 社会 法治：210804,1008,42510
+ 国际 军事：210805,1011,1002
+ 教科 文卫：210806,1006,1007,1013,14739
+ 台湾 港澳：210807,14657,42272
+ 观点 理论：210808,40531,1003
+ 传媒 舆情：210809,14677,209043
+ 体育 娱乐：22176,210810,14820,1012
+ 电视 图片：210811,174585,1016
+ 游戏 动漫：210812,40130,122366
+ 环保 IT：1010,1009
+ 家电 通信：41390,183008
+ 食品 房产：215731,194441
+ 人工智能：422228
+ 微博快报 微博访谈：347079,347759
+ 人民创投：405954
+ 东京速递：368583
+ 知识产权：179663

请求方式：POST
请求URL：http://8.129.210.219/api/hot_news

请求数据格式：json

tag_values：标签值列表
~~fresh：是否刷新（若刷新则更新缓存，待定）~~
~~是否使用分页查询~~

```json
{
    "tag_values": [
    "210802,1001,14576,34948",
    "210803,1004,413883",
    "67815,71661"
    ]
}
```
返回数据格式：json

暂时只返回前十条新闻数据

```json
{
    "items":[
        {
            "id":"31788772",
            "title":"证监会就证券期货违法行为行政处罚办法公开征求意见 ",
            "url":"http://money.people.com.cn/n1/2020/0719/c42877-31788772.html",
            "date":"2020-07-19 09:42:30",
            "nodeId":"67815",
            "imgCount":"0"
        },
        {
            "id":"31788699",
            "title":"影院重启或迎"报复性观影"?专家:亟需高质"头部影片"带动",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788699.html",
            "date":"2020-07-19 08:13:07",
            "nodeId":"1004",
            "imgCount":"0"
        },
        {
            "id":"31788698",
            "title":"借呗和微粒贷借钱不得超20万？答案来了",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788698.html",
            "date":"2020-07-19 08:12:18",
            "nodeId":"1004",
            "imgCount":"1"
        },
        {
            "id":"31788697",
            "title":"上半年人均可支配收入排行榜：京沪超3.4万 你赚多少？",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788697.html",
            "date":"2020-07-19 08:11:24",
            "nodeId":"1004",
            "imgCount":"2"
        },
        {
            "id":"31788696",
            "title":"31省份上半年房地产开发投资排行：粤苏浙稳坐“前三”",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788696.html",
            "date":"2020-07-19 08:10:42",
            "nodeId":"1004",
            "imgCount":"2"
        },
        {
            "id":"31788693",
            "title":"欧盟峰会首日：“恢复基金”谈判陷僵局",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788693.html",
            "date":"2020-07-19 08:08:46",
            "nodeId":"1004",
            "imgCount":"1"
        },
        {
            "id":"31788692",
            "title":"国际货币基金组织预计 美国经济二季度萎缩37%",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788692.html",
            "date":"2020-07-19 08:08:14",
            "nodeId":"1004",
            "imgCount":"2"
        },
        {
            "id":"31788691",
            "title":"过紧日子 晒明白账 中央部门连续10年向社会公开决算",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788691.html",
            "date":"2020-07-19 08:06:10",
            "nodeId":"1004",
            "imgCount":"0"
        },
        {
            "id":"31788690",
            "title":"做好“六稳”工作 落实“六保”：政策送温暖 企业增活力",
            "url":"http://finance.people.com.cn/n1/2020/0719/c1004-31788690.html",
            "date":"2020-07-19 08:05:37",
            "nodeId":"1004",
            "imgCount":"0"
        },
        {
            "id":"31788627",
            "title":"全国人大常委会启动慈善法执法检查",
            "url":"http://politics.people.com.cn/n1/2020/0719/c1001-31788627.html",
            "date":"2020-07-19 05:01:15",
            "nodeId":"1001",
            "imgCount":"0"
        }
    ]
}
```

### 根据新闻URL获取新闻主要内容

请求方式：POST
请求URL：http://8.129.210.219/api/news_content

请求数据格式：json

news_url：新闻链接

```json
{
    "news_url": "http://finance.people.com.cn/n1/2020/0719/c1004-31788697.html"
}
```

返回数据格式：json

```json
{
    "title": "上半年人均可支配收入排行榜：京沪超3.4万 你赚多少？--财经--人民网 ",
    "date": "2020年07月19日08:11",
    "media_source": "中新经纬",
    "contents": [
    {
    "type": "text",
    "is_center": false,
    "is_strong": false,
    "text": "中新经纬客户端7月19日电 (熊思怡)日前，国家统计局网站公布2020年上半年31省份居民人均可支配收入显示，上海、北京人均可支配收入突破3.4万，另有8省份上半年人均可支配收入超全国平均线。"
    },
    {
    "type": "img",
    "img_url": "http://finance.people.com.cnhttp://www.people.com.cn/mediafile/pic/20200719/47/5681516794433528199.jpg"
    }
    ]
}
```
### 新闻检索
#### 通过查询字段获取新闻简要信息

请求方式：GET 

请求URL：http://8.129.210.219/api/search?query=''

请求数据格式：string

eg. query =美国疫情

```json
{
    "items": [
        {
            "dateTime": "2020年07月22日05:28",
            "title": "让乡亲收获更多幸福感（走向我们的小康生活）",
            "url": "http://society.people.com.cn/n1/2020/0722/c1008-31792409.html"
        },
        {
            "dateTime": "2020年07月22日08:30",
            "title": "关于依法保障和服务疫情防控常态化条件下经济社会发展的指导意见",
            "url": "http://yuqing.people.com.cn/n1/2020/0722/c429253-31792937.html"
        },
        {
            "dateTime": "2020年07月23日09:32",
            "title": "埃及出兵利比亚箭已上弦",
            "url": "http://military.people.com.cn/n1/2020/0723/c1011-31794889.html"
        },
        {
            "dateTime": "2020年07月22日05:27",
            "title": "人民日报民生观：敢担当 响当当",
            "url": "http://opinion.people.com.cn/n1/2020/0722/c1003-31792399.html"
        }
    ]
  }
```

### 舆情感知

#### 获取社会热点话题

请求方式：GET
请求URL：http://8.129.210.219/api/hot_topic

返回数据格式：json

hot_count：热度

newsid：新闻id

sentiment：网民评论情绪 1：正面，0：一般（中性），-1：负面

```json
{
    "hot_topic": [
        {
            "hot_count": 1470,
            "newsid": "comos-ivhuipn4724222",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "遭家暴跳楼截瘫女子发声：婚前百般体贴  事发后受到公公死亡威胁"
        },
        {
            "hot_count": 339,
            "newsid": "comos-ivhvpwx7174448",
            "sentiment": 0,
            "time": "2020-07-24 16:11:15",
            "title": "男生从清华退学后重读考699分：对此前专业不满意"
        },
        {
            "hot_count": 308,
            "newsid": "comos-ivhvpwx7120821",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州女子“失踪”案探访：警方清理涉案小区化粪池"
        },
        {
            "hot_count": 272,
            "newsid": "comos-ivhvpwx7103006",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州失踪女子已遇害 其丈夫被采取刑事强制措施"
        },
        {
            "hot_count": 237,
            "newsid": "comos-ivhuipn4774123",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "“中科院近百人离职”事前事中事后到底发生了什么？"
        },
        {
            "hot_count": 188,
            "newsid": "comos-ivhvpwx7163583",
            "sentiment": 1,
            "time": "2020-07-24 16:11:15",
            "title": "“一乡村小学9名老师仅教1名学生” 官方回应"
        },
        {
            "hot_count": 149,
            "newsid": "comos-ivhuipn4831665",
            "sentiment": 0,
            "time": "2020-07-24 16:11:15",
            "title": "全聚德全面取消服务费，下调菜品价格"
        },
        {
            "hot_count": 117,
            "newsid": "comos-ivhuipn4825951",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "邻居曝杭州失踪女子丈夫在电梯内用胳膊遮脸说话 物业:他并不在这里工作"
        },
        {
            "hot_count": 38,
            "newsid": "comos-ivhvpwx7080057",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "“继母”让两名情人强奸未成年“继女”终审获刑16年"
        },
        {
            "hot_count": 32,
            "newsid": "comos-ivhvpwx7104900",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "警方通报：来女士丈夫有重大作案嫌疑 面对记者的他太冷静"
        },
        {
            "hot_count": 32,
            "newsid": "comos-ivhuipn4828608",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州失踪女子遇害案七大疑点:凶案第一现场究竟在哪?"
        },
        {
            "hot_count": 30,
            "newsid": "comos-ivhuipn4704287",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "男子吃生牛肉脑内长虫 另外有人全身布满虫卵……"
        },
        {
            "hot_count": 28,
            "newsid": "comos-ivhuipn4854741",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "重返杭州53岁失踪女子遇害案现场：邻居未听到异常响动，嫌疑人许某非物业人员"
        },
        {
            "hot_count": 28,
            "newsid": "comos-ivhuipn4729433",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "女子称不堪家暴跳楼致双下肢截瘫，当地妇联介入"
        },
        {
            "hot_count": 27,
            "newsid": "comos-ivhuipn4879996",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "大连新增9例本土确诊病例 新增27例无症状感染者"
        },
        {
            "hot_count": 24,
            "newsid": "comos-ivhuipn4701795",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "蝙蝠如何扛住新冠等“多重夹击”？科学家破译了它的基因"
        },
        {
            "hot_count": 23,
            "newsid": "comos-ivhvpwx7162312",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "检方回应女子不堪家暴跳楼：公诉已包含跳楼伤害"
        },
        {
            "hot_count": 22,
            "newsid": "comos-ivhvpwx7056350",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "新京报：努某某是“初犯”还是“惯犯”，这点很重要"
        },
        {
            "hot_count": 21,
            "newsid": "comos-ivhvpwx7215609",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "探访杭州失踪女子住所：化粪池距住处50米 家属围着井盖痛哭"
        },
        {
            "hot_count": 20,
            "newsid": "comos-ivhuipn4370129",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "北京业主酒后回小区被查出入证 疯狂暴打保安头部致其昏迷不醒"
        },
        {
            "hot_count": 20,
            "newsid": "comos-ivhuipn4772253",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "伊朗客机遭2架战机侵扰紧急迫降 机舱摇晃多名乘客受伤"
        },
        {
            "hot_count": 19,
            "newsid": "comos-ivhuipn4674729",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "北影第一、中传第一、上戏第一！这个女生火遍全网"
        },
        {
            "hot_count": 19,
            "newsid": "comos-ivhvpwx7165349",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州警方通报“女子失踪案”后 小区门口又现网红直播"
        },
        {
            "hot_count": 18,
            "newsid": "comos-ivhuipn4526762",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "男子自称要在杭州西湖区传播性病 警方：已展开调查"
        },
        {
            "hot_count": 18,
            "newsid": "comos-ivhvpwx7090538",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "女子不堪家暴跳楼致截瘫 没能离成婚还曾遭死亡威胁"
        },
        {
            "hot_count": 18,
            "newsid": "comos-ivhvpwx7210599",
            "sentiment": 1,
            "time": "2020-07-24 16:11:15",
            "title": "福布斯2020年中国慈善榜发布 杨国强家族捐赠15.2亿元位列第二"
        },
        {
            "hot_count": 17,
            "newsid": "comos-ivhuipn4730707",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "浙江离奇失踪19天女子遇害，老公是凶手，化粪池里找到涉案物"
        },
        {
            "hot_count": 16,
            "newsid": "comos-ivhvpwx6956395",
            "sentiment": 1,
            "time": "2020-07-24 16:11:15",
            "title": "12省份今天可查分！速览高考查分表情大合集"
        },
        {
            "hot_count": 16,
            "newsid": "comos-ivhvpwx6768297",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "男子持铁锹暴打老人小孩 老人当场死亡幼女住进ICU"
        },
        {
            "hot_count": 16,
            "newsid": "comos-hsxncvf7894232",
            "sentiment": 1,
            "time": "2020-07-24 16:11:15",
            "title": "11岁就被特招入伍 解放军某防空旅女排长的传奇经历"
        },
        {
            "hot_count": 14,
            "newsid": "comos-ivhuipn4784661",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "法国男子徒手赤脚爬上巴塞罗那31层大楼 未穿戴任何安全措施"
        },
        {
            "hot_count": 14,
            "newsid": "comos-ivhuipn4717060",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "高空抛物伤人物业全楼验DNA:肇事者承担全部检测费用"
        },
        {
            "hot_count": 13,
            "newsid": "comos-ivhvpwx7122683",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "抗疫志愿者之子漏斗胸急需治疗，家属发起网上筹款"
        },
        {
            "hot_count": 12,
            "newsid": "comos-ivhuipn4398685",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "老板遇车祸 其家属竟持铁锹把司机3岁女儿打进ICU 母亲当场死亡"
        },
        {
            "hot_count": 12,
            "newsid": "comos-ivhuipn4720056",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "自由女神像遭闪电击中  网友：上帝的信号"
        },
        {
            "hot_count": 12,
            "newsid": "comos-ivhuipn4693053",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "8旬老太遭儿媳虐待 儿子：谁都不准给饭吃谁给饭谁养"
        },
        {
            "hot_count": 12,
            "newsid": "comos-ivhuipn4693467",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "过路大爷遭大型犬撕咬1分钟  多部位被咬得鲜血直流"
        },
        {
            "hot_count": 12,
            "newsid": "comos-ivhvpwx7165359",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州警方通报＂女子失踪案＂后 小区门口又现网红直播"
        },
        {
            "hot_count": 11,
            "newsid": "comos-ivhuipn4528550",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "多名女生称遭浙大＂强奸案＂主角猥亵 学校了解调查中"
        },
        {
            "hot_count": 11,
            "newsid": "comos-ivhuipn4802636",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "弟弟给姐姐转账1658元后失联 充电器还插在墙上"
        },
        {
            "hot_count": 10,
            "newsid": "comos-ivhvpwx7187734",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "探访独山县:＂天下第一水司楼＂将再度施工 改建成酒店"
        },
        {
            "hot_count": 10,
            "newsid": "comos-ivhvpwx7088213",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "山西文旅厅官员偷拍女租客 已被刑拘"
        },
        {
            "hot_count": 10,
            "newsid": "comos-ivhuipn4832666",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "安徽女子因琐事到邻居家投毒致1死1伤 一审被判无期"
        },
        {
            "hot_count": 9,
            "newsid": "comos-ivhuipn4784282",
            "sentiment": 1,
            "time": "2020-07-24 16:11:15",
            "title": "四川文科学霸高考数学满分 班主任：她是“全才”"
        },
        {
            "hot_count": 9,
            "newsid": "comos-ivhuipn4801416",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "美国一女子被戴手铐时突然掏枪开火 遭两警察击中倒地惨叫不止"
        },
        {
            "hot_count": 9,
            "newsid": "comos-ivhuipn4656656",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州女子失踪第19天：下午1时现场被编织袋围起(图)"
        },
        {
            "hot_count": 9,
            "newsid": "comos-ivhvpwx6891420",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "大学生售卖2只鹦鹉一审获刑6年 女友：已上诉"
        },
        {
            "hot_count": 9,
            "newsid": "comos-ivhuipn4859127",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州失踪女子家属围着井盖痛哭 化粪池距离住处仅50米"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhuipn4817171",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州“失踪女子”遇害:小区保安否认其丈夫在此干物业公司 疑当过兵"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhuipn4825807",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "美航空公司一乘客拒戴口罩被赶下飞机 乘客鼓掌欢呼"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhvpwx7211025",
            "sentiment": -1,
            "time": "2020-07-24 16:11:15",
            "title": "杭州女子失踪案后续：警方到被害人家中取证，小区内传出哭声"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhuipn4728816",
            "sentiment": 0,
            "time": "2020-07-24 16:11:16",
            "title": "甘肃小学9名教师仅教1名学生？教育局：误会了"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhvpwx7079194",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "失踪近20日的来女士到底找到了吗？杭州市公安局江干分局何时发通报？"
        },
        {
            "hot_count": 8,
            "newsid": "comos-ivhvpwx7212800",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "杭州女子失踪案后续：警方到被害人家中取证，小区内传出哭声"
        },
        {
            "hot_count": 7,
            "newsid": "comos-ivhuipn4578869",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "英国流浪汉头部被淋啤酒并被推下河 拍摄者笑声刺耳"
        },
        {
            "hot_count": 7,
            "newsid": "comos-ivhuipn4743465",
            "sentiment": 0,
            "time": "2020-07-24 16:11:16",
            "title": "夜探杭州遇害女子小区：楼道有人值守，大女儿刚刚离开"
        },
        {
            "hot_count": 7,
            "newsid": "comos-ivhuipn4820435",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "西安发生严重车祸十余辆汽车连撞 多辆车变形严重"
        },
        {
            "hot_count": 7,
            "newsid": "comos-ivhvpwx7070925",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "幼童疑似被老师扇巴掌后尿裤子 老师：只拍了肩膀"
        },
        {
            "hot_count": 6,
            "newsid": "comos-ivhuipn4669408",
            "sentiment": -1,
            "time": "2020-07-24 16:11:16",
            "title": "有人作弊被开除学籍 浙江大学竟对强奸犯＂法外开恩＂?"
        }
    ]
}
```

#### 更新社会热点话题

请求方式：POST
请求URL：http://8.129.210.219/api/update_hot_topic

返回数据格式：更新数据以及评论情感分析时间较长，超时nginx可能会返回502，使用POST请求是为了不小心点击该链接导致服务器端数据更新

#### 根据新闻id获取评论内容

请求方式：GET 

请求URL：http://8.129.210.219/api/news_comment?newsid=

例：http://8.129.210.219/api/news_comment?newsid=comos-ivhuipn4724222

```json
{
    "comments": {
        "com_comments": [
            "嫁了个人渣",
            "小孩怎么办呐",
            "公安呢",
            "查",
            "唉！想不开呀",
            "可悲",
            "唉",
            "一日夫妻百日恩，有啥事不能好好说话吗？",
            "厉害的",
            "对威胁她人生命安全的人也应依法处理。",
            "打女人的男人都不是好男人",
            "厉害",
            "婚后",
            "婚前",
            "施暴者必受法律制裁！",
            "家暴",
            "",
            "应给予实施家暴的人应有的惩罚",
            "生命是最珍贵的，活下去就没有解决的问题。",
            "可怜的女人。"
        ],
        "hot_comments": [
            "受害人应该申请防止家暴的人身保护令。警方应该将施暴者绳之以法。",
            "家暴猛于虎",
            "三年高中同学不应该这样啊  这男的演技挺高啊",
            "所以婚前擦亮眼都没用。",
            "赌鬼是没人性的。",
            "董珊珊的前车之鉴啊！你们要有多少个董珊珊的血才能让女人痛痛快快的离婚？！",
            "所以平权仙子天天叫嚣擦亮眼有用吗？拿钢丝球擦好不好？",
            "偏执狂，对你好可能不是因为喜欢你，可能他只是不想输，反而内心觉得你很好得到。",
            "要小心凡事顺从你，对你低三下四卑微到尘埃的人。",
            "法院早点判离婚多好，家暴还不判决立刻离婚就是帮凶"
        ]
    }
}
```