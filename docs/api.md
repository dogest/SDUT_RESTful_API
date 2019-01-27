# API 文档

## 全局状态

- HTTP 200: OK，请求成功
- HTTP 401: 账号认证未通过，请检查账号密码
- HTTP 403: 账号无权限，请确认使用的账号有对应的权限
- HTTP 500: 服务器错误，如果多次出现，请联系开发者解决

## Public API

[public_api.md](public_api.md)

## User

### Token

使用[山东理工大学统一登录平台](http://authserver.sdut.edu.cn/authserver/login)的账号与密码来申请一个七天可用的 Token，以供后续其他请求使用。

**注意**

短时间内多次请求此 API 可能会导致账号被 ban，从而无法登录。

如果账号密码正确的话，那么每次请求返回的 Token 在七天内都可以使用。

**URL**

`/user/token`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `username` | string | 用户名（学号） |
| `password` | string | 密码 |


**请求示例**

```bash
curl http://<url>/user/token --request POST --form 'username=<username>' --form 'password=<password>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `token` | string | Token |

**返回示例**

```json
{
    "error": false,
    "token": "SDUTAPI_aaaa-bbbb-cccc-dddd"
}
```

### Info

请求用户的基本信息。


**URL**

`/user/info`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl http://<url>/user/info --request POST --form 'token=<token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `name` | string | 用户的姓名 |
| `userid` | string | 用户的学号 |
| `department` | string | 用户的部门/学院 |

**返回示例**

```json
{
    "error": false,
    "user": {
        "name": "张三",
        "userid": "15110570001",
        "department": "计算机科学与技术学院"
    }
}
```

## Library

### Borrow

获取用户图书借阅的详情

**URL**

`/library/borrow`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/library/borrow \
  --form 'token=<Token>'
```

**返回参数**

当前借阅 info

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `title` | string | 图书名 |
| `author` | string | 图书作者 |
| `borrow_date` | string(xxxx-yy-zz) | 借阅时间 |
| `back_date` | string | 应还时间 |
| `borrow_cnt` | string | 续借次数 |
| `site` | string | 借书地址 |

历史借阅 history

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `title` | string | 图书名 |
| `author` | string | 图书作者 |
| `borrow_date` | string(xxxx-yy-zz) | 借阅时间 |
| `back_date` | string | 还书时间 |
| `bar_code` | string | bar_code |
| `book_url` | string | 在山东理工大学图书馆网站中的链接 |
| `site` | string | 借书地址 |

**返回示例**

```json
{
    "error": false,
    "info": [],
    "history": [
        {
            "bar_code": "1957178",
            "title": "ACM国际大学生程序设计竞赛:题目与解读",
            "book_url": "http://222.206.65.12/opac/item.php?marc_no=0000616967",
            "author": "俞勇主编",
            "borrow_date": "2016-11-19",
            "back_date": "2016-11-27",
            "site": "逸夫馆三层西区"
        },
        {
            "bar_code": "1554967",
            "title": "洛丽塔",
            "book_url": "http://222.206.65.12/opac/item.php?marc_no=0000428895",
            "author": "弗拉基米尔·纳博科夫[著]",
            "borrow_date": "2015-09-29",
            "back_date": "2015-10-08",
            "site": "逸夫馆二层西区"
        }
    ]
}
```

## Card

### Balance

查询用户的校园卡余额

**URL**

`/card/balance`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/card/balance \
  --form 'token=<Token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `userid` | string | 用户名（学号） |
| `name` | string | 用户姓名 |
| `balance` | string | 校园卡余额 |

**返回示例**

```json
{
    "error": false,
    "userid": "15110570001",
    "name": "张三",
    "balance": "30.40"
}
```

### Consume

用户最近的交易详情

**URL**

`/card/consume`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |
| `userid` | string | 用户名（学号） |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/card/consume \
  --form 'token=<Token>' \
  --form 'userid=15110570001'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `time` | string | 消费时间(YYYY-mm-dd HH:MM) |
| `reason` | string | 消费原因 |
| `amount` | string | 消费金额 |
| `balance` | string | 消费后余额 |
| `position` | string | 消费位置 |
| `trem_name` | string | 消费终端 |

**返回示例**

```json
{
    "error": false,
    "consume": [
        {
            "time": "2019-01-18 17:36",
            "reason": "用水支出",
            "amount": "0.13",
            "balance": "32.46",
            "position": "图书馆直饮水采集",
            "term_name": "图书馆直饮水004"
        },
        {
            "time": "2019-01-18 17:34",
            "reason": "商场购物",
            "amount": "6.50",
            "balance": "32.59",
            "position": "消费TCP采集",
            "term_name": "图书馆咖啡厅"
        },
        {
            "time": "2019-01-18 17:31",
            "reason": "商场购物",
            "amount": "7",
            "balance": "39.09",
            "position": "消费TCP采集",
            "term_name": "图书馆文具店（西校）"
        },
        {
            "time": "2019-01-18 17:27",
            "reason": "商场购物",
            "amount": "3",
            "balance": "46.09",
            "position": "消费TCP采集",
            "term_name": "泰瑞文具"
        }
    ]
}
```
