## Schedule

### API

查询课程表

**URL**

`/schedule`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```
curl --request POST \
  --url http://127.0.0.1:8000/schedule \
  --form 'token=<Token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `userid` | string | 用户名（学号） |
| `name` | string | 用户姓名 |
| `schedule` | list | 课程信息 |
| `extra` | list | 其他课程 |
| `note` | list | 备注 |
| `separator` | list | 课程名中符号的含义 |
| `year` | string | 当前学年 |
| `semester` | string | 当前学期 |
| `current_week` | integer | 当前教学周 |

**返回示例**

```
{
    "error": false,
    "data": {
        "schedule": [
            {
                "duration_of_class": "1-4",
                "duration_of_week": "7-12周",
                "classroom": "教3302(西)",
                "class_name": "大学英语读写(A)Ⅳ",
                "day_of_week": "7",
                "teacher_name": "江金谛"
            }
        ],
        "extra": [
            {
                "class_name": "计算机专业毕业实践与毕业设计(A)●",
                "teacher_name": "吴志勇",
                "duration_of_week": "1-17周"
            }
        ],
        "note": [
            {
                "content": "校本部体育课第一次上课在第二体育场集合"
            }
        ],
        "separator": [
            {
                "key": "☆",
                "value": "讲课"
            },
            {
                "key": "●",
                "value": "实践"
            },
            {
                "key": "○",
                "value": "上机"
            },
            {
                "key": "★",
                "value": "实验"
            }
        ],
        "name": "张三",
        "userid": "1511000000",
        "year": "2018",
        "semester": "2",
        "current_week": 7
    }
}
```
