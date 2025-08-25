# Tushare数据

Toggle navigation

# [![tushare](/static/frontend/images/logo.png?v=39c50795cb540b4463114d1bf3135d6e)](/)

*   [首页](/)
*   [平台介绍](/document/1)
*   [数据接口](/document/2)
*   [资讯数据](/news/sina)
*   [数据工具](/webclient)
*   [![](/static/frontend/images/user1.png?v=66b9eed0d587f983d2dab0e994180317)186 \*\*\* 001](#)
    *   [个人主页](/user/center)
    *   退出登录

*   [平台介绍](/document/1?doc_id=5)
*   [操作手册](/document/1?doc_id=37)
    *   [用户注册](/document/1?doc_id=38)
    *   [获取token](/document/1?doc_id=39)
    *   [调取数据](/document/1?doc_id=40)
*   [获取方式](/document/1?doc_id=129)
*   [踩坑记录](/document/1?doc_id=229)
*   [平台服务](/document/1?doc_id=10)
*   [相关工具](/document/1?doc_id=30)
*   [培训课程](/document/1?doc_id=167)
*   [机构招聘](/document/1?doc_id=205)
*   [高校服务](/document/1?doc_id=306)
*   [专业微群](/document/1?doc_id=270)
*   [社区捐助](/document/1?doc_id=243)

## 调取pro版数据

* * *

下面介绍两种常用的数据调取方式：

*   通过tushare python包
*   使用http协议直接获取

注：pro版数据接口采用语言无关的http协议实现，但也提供了多种语言的[SDK数据获取](https://tushare.pro/document/1?doc_id=129)。

### 前提条件

1、已经注册了tushare社区用户 【[注册用户](https://tushare.pro/register)】  
2、已经获取到tushare token凭证 【[获取token](https://tushare.pro/document/1?doc_id=39)】

### Python SDK

#### 下载SDK

下载并安装最新版tushare SDK 【[安装和升级方法](https://tushare.pro/document/1?doc_id=7)】

**导入tushare**

```python
import tushare as ts
```

这里注意， tushare版本需大于1.2.10

**设置token**

```python
ts.set_token('your token here')
```

以上方法只需要在第一次或者token失效后调用，完成调取tushare数据凭证的设置，正常情况下不需要重复设置。也可以忽略此步骤，直接用pro\_api('your token')完成初始化

**初始化pro接口**

```python
pro = ts.pro_api()
```

如果上一步骤ts.set\_token('your token')无效或不想保存token到本地，也可以在初始化接口里直接设置token:

```python
pro = ts.pro_api('your token')
```

**数据调取**

以获取交易日历信息为例：

```python
df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
```

或者

```python
df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
```

调取结果：

```
    exchange  cal_date    is_open pretrade_date
0          SSE       20180901        0      20180831
1          SSE       20180902        0      20180831
2          SSE       20180908        0      20180907
3          SSE       20180909        0      20180907
4          SSE       20180915        0      20180914
5          SSE       20180916        0      20180914
6          SSE       20180922        0      20180921
7          SSE       20180923        0      20180921
8          SSE       20180924        0      20180921
9          SSE       20180929        0      20180928
10         SSE       20180930        0      20180928
11         SSE       20181001        0      20180928
```

### HTTP协议方式

http restful 采用post方式，通过json body传入接口参数，请求地址为[http://api.tushare.pro](http://api.tushare.pro)

#### 输入参数

*   api\_name，接口名称；
*   token，用于识别唯一用户的标识；
*   params，接口参数，如daily接口中start\_date和end\_date；
*   fields，字段列表，用于接口获取指定的字段，以逗号分隔，如"open,high,low,close"；

#### 输出参数

*   code: 接口返回码，2002表示权限问题。
*   msg: 错误信息；
*   data: 具体数据，成功的请求包含fields和items字段，fields与items数据一一对齐；

#### 示例

采用命令行工具curl的请求示例如下：

```bash
curl -X POST -d '{"api_name": "trade_cal", "token": "xxxxxxxx", "params": {"exchange":"", "start_date":"20180901", "end_date":"20181001", "is_open":"0"}, "fields": "exchange,cal_date,is_open,pretrade_date"}' http://api.tushare.pro
```

返回结果：

```
{
        "code":0,
        "msg":null,
        "data":{
                "fields":[
                        "exchange",
                        "cal_date",
                        "is_open",
                        "pretrade_date"
                ],
                "items":[
                        [
                                "SSE",
                                "20180901",
                                0,
                                "20180831"
                        ],
                        [
                                "SSE",
                                "20180902",
                                0,
                                "20180831"
                        ],
                        [
                                "SSE",
                                "20180908",
                                0,
                                "20180907"
                        ],

            ...

                        [
                                "SSE",
                                "20180929",
                                0,
                                "20180928"
                        ],
                        [
                                "SSE",
                                "20180930",
                                0,
                                "20180928"
                        ],
                        [
                                "SSE",
                                "20181001",
                                0,
                                "20180928"
                        ]
                ]
        }
}
```

![](/static/frontend/images/wechat_public.png?v=847e8d705d3a409d000dce413ab5c257)

使用文档

*   [平台介绍](/document/1)
*   [数据接口](/document/2)
*   [区块链](/document/41)
*   [资讯数据](/news)

关注我们

*   QQ群: 958517905
*   公众号：waditu
*   Github：[https://github.com/waditu](https://github.com/waditu)
*   雪 球：[https://xueqiu.com/u/9103835084](https://xueqiu.com/u/9103835084)
*   微 博：[https://weibo.com/u/1304687120](https://weibo.com/u/1304687120)

© 2018 Tushare ["沪ICP备2020031644号"](https://beian.miit.gov.cn)

[置顶](#page)