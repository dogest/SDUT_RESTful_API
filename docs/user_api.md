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

### Exist

判断指定的 Token 在服务器上是否还存在（存在不代表保证可用）。

**URL**

`/user/token/exists`

**请求类型**

`POST`

**请求参数**

| 参数 | 类型 | 含义 |
| ---- | ---- | - |
| `token` | string | Token |


**请求示例**

```bash
curl http://<url>/user/token/exist --request POST --form 'token=<token>'
```

**返回参数**

| 字段    | 类型   | 含义  |
| ------- | ------ | ----- |
| `token` | string | Token |

**返回示例**

```json
{
    "error": false,
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
    "data": {
        "name": "张三",
        "userid": "15110570001",
        "department": "计算机科学与技术学院"
    }
}
```
