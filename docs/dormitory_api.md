## Dormitory

### Info

获取用户宿舍基本信息

**URL**

`/dormitory/info`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/dormitory/info \
  --form 'token=<Token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `campus` | string | 校区 |
| `floor` | string | 公寓 |
| `room` | string | 宿舍号 |
| `raw_floor` | string | 可用于[电量查询](public_api.md#Energy)的 floor 格式 |

**返回示例**

```json
{
    "error": false,
    "campus": "西校区",
    "floor": "6号公寓",
    "room": "6H101",
    "raw_floor": "06#"
}
```

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
    "health": [
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
