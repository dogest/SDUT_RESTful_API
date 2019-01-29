## Score

### Score

查询成绩与绩点

**URL**

`/score`

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
  --url http://127.0.0.1:8000/score \
  --form 'token=<Token>' \
  --form 'userid=<userid>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `grade` | float | 绩点（仅供参考） |
| `scores` | list | 成绩详情 |
| `message` | string | 提示信息（告诉你绩点仅供参考） |

**返回示例**

太长了，自己请求看吧
