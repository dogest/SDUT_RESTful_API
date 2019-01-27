## Public

### Energy

**URL**

`/public/energy`

**请求类型**

`POST`

**请求参数**

| 参数    | 类型   | 含义                                          |
| ------- | ------ | --------------------------------------------- |
| `floor` | string | 公寓号（可用列表见[公寓列表](floor_list.md)） |
| `room`  | string | 房间号                                        |

**请求示例**

```bash
curl http://<url>/public/energy --request POST --form 'floor=01#南' --form 'room=101'
```

**返回参数**

| 字段     | 类型   | 含义                                |
| -------- | ------ | ----------------------------------- |
| ` room`  | string | 请求的房间                          |
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
        "room": "06#627",
        "date": "2019-01-23 18:35:14",
        "energy": "2.45",
        "lower": "1",
        "upper": "2",
        "status": "正常用电"
    }
}
```
