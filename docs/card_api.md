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
    "data": {
        "userid": "15110570001",
        "name": "张三",
        "balance": "30.40"
    }
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
| `term_name` | string | 消费终端 |

**返回示例**

```json
{
    "error": false,
    "data": [
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

### Summary

获取指定时间范围内的交易汇总（因为校园卡平台限制最多返回八条，因此可能不全，如果结果少于八条则为全部的。）

**URL**

`/card/summary`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |
| `userid` | string | 用户名（学号） |
| `start_date` | string | 开始时间（YYYYmmdd） |
| `end_date` | string | 结束时间 |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/card/summary \
  --form 'token=<Token>' \
  --form 'userid=15110570001' \
  --form 'start_date=20180910' \
  --form 'end_date=20190101'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `id` | string | 未知含义 |
| `reason` | string | 交易原因 |
| `amount` | string | 交易金额 |
| `ext_1` | string | 未知用途，用于表示一个数字 |
| `ext_2` | string | 同上 |
| `ext_3` | string | 同上 |

**返回示例**

```json
{
    "error": false,
    "data": [
        {
            "id": "100",
            "reason": "终端存款",
            "amount": "463.50",
            "ext_1": "0",
            "ext_2": "0",
            "ext_3": "0"
        },
        {
            "id": "104",
            "reason": "补助存款",
            "amount": "0",
            "ext_1": "0",
            "ext_2": "300",
            "ext_3": "0"
        },
        {
            "id": "157",
            "reason": "支付宝充值领款",
            "amount": "1800",
            "ext_1": "0",
            "ext_2": "0",
            "ext_3": "0"
        },
        {
            "id": "210",
            "reason": "餐费支出",
            "amount": "1845.36",
            "ext_1": "0",
            "ext_2": "246.88",
            "ext_3": "0"
        },
        {
            "id": "211",
            "reason": "淋浴支出",
            "amount": "13.75",
            "ext_1": "0",
            "ext_2": "3.24",
            "ext_3": "0"
        },
        {
            "id": "215",
            "reason": "商场购物",
            "amount": "278.30",
            "ext_1": "0",
            "ext_2": "49.50",
            "ext_3": "0"
        },
        {
            "id": "220",
            "reason": "用水支出",
            "amount": "5.91",
            "ext_1": "0",
            "ext_2": "0.10",
            "ext_3": "0"
        },
        {
            "id": "222",
            "reason": "购热水支出",
            "amount": "3.83",
            "ext_1": "0",
            "ext_2": "0",
            "ext_3": "0"
        }
    ]
}
```
