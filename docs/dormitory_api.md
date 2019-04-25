## Dormitory

### Health

查询用户宿舍卫生信息，最多返回 100 条数据。如果总数据量小于 100 条，则全部返回。

**URL**

`/dormitory/health`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/dormitory/health \
  --form 'token=<Token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `floor` | string | 公寓 |
| `room` | string | 宿舍号 |
| `week` | string | 周次 |
| `date` | string | 时间 |
| `score` | int | 分数 |

**返回示例**

```json
{
    "error": false,
    "data": [
        {
            "floor": "6号公寓",
            "room": "6H101",
            "week": "18",
            "date": "2019-01-01",
            "score": 99
        },
        {
            "floor": "6号公寓",
            "room": "6H101",
            "week": "17",
            "date": "2018-12-25",
            "score": 98
        }
    ]
}
```

### Energy

获取宿舍电量，因为对应平台对登录有奇怪的限制（稳定 sleep 10 秒），因此此接口需要 10S+ 才能返回数据

**URL**

`/dormitory/energy`

**请求类型**

`POST`

**请求参数**

| 参数    | 类型   | 含义                                          |
| ------- | ------ | --------------------------------------------- |
| `token` | string | Token |
| `floor` | string | 公寓号（可用列表见[公寓列表](floor_list.md)） |
| `room`  | string | 房间号                                        |

**请求示例**

```bash
curl http://<url>/public/energy --request POST --form 'token=<Token>' --form 'floor=01#南' --form 'room=101'
```

**返回参数**

| 字段     | 类型   | 含义                                |
| -------- | ------ | ----------------------------------- |
| `room`  | string | 请求的房间                          |
| `date`   | string | 上次更新时间(`YYYY-mm-dd HH:MM:SS`) |
| `energy` | string | 剩余电量（结果不能保证为数字类型）  |
| `lower`  | string | 预计可用下限                        |
| `upper`  | string | 预计可用上限                        |
| `status` | string | 当前使用状态（如：正常用电）        |

**返回示例**

```json
{
    "error": false,
    "data": {
        "room": "06#101",
        "date": "2019-01-23 18:35:14",
        "energy": "2.45",
        "lower": "1",
        "upper": "2",
        "status": "正常用电"
    }
}
```
