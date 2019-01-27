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
