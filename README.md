# SDUT RESTful API

一些有关于 SDUT 的 API 封装

## 警告

测试账号已经被[山东理工大学网上服务大厅](http://ehall.sdut.edu.cn/new/ehall.html)封禁，在没有试探出对方的封禁规则前，请不要使用山东理工大学网上服务大厅的任何接口。

以下是不经过山东理工大学网上服务大厅的接口列表：

- `/user`
  - `/user/token`
- `/library`
  - `/library/borrow`
- `/score`
- `/public/energy`
- `/course`
  - `/course/schedule`
  - `/course/reminder`

[山东理工大学网络教学综合平台](http://etc.sdut.edu.cn/meol/homepage/common/)的接口还未开发完成，因此实际可用的只有：图书借阅、成绩与绩点、宿舍电量查询。

另外，本人的爬取行为在某种意义上得到了山东理工大学后勤服务中心与山东理工大学图书馆的授权，此处对这些组织表示感谢，同时对因为我的爬虫而给相应网站造成的影响表示歉意。

我现在已经不在校内了，无法去依次拜访学校内各个组织来获得授权，因此现在只能以这种未授权爬虫的形式获得数据，并且有较高的被封禁风险。

本项目的目标在于为同学们提供便利，如果学校内有组织愿意开放数据来开发方便同学们生活使用的系统，我愿意放弃我自己的项目。并且如果有可以用得到我的地方，我也定将略尽绵力。

PS：在 2018 年夏，我与老师一同去山东理工大学信息楼获得了爬取山东理工大学网上服务大厅的**口头**授权，仅存的证据只有我与老师的聊天与通话记录，没有直接的证据。

## Usage

[API 文档](docs/api.md)

## Run WebServer

```bash
$ python3 -m venv venv
$ source venv/bin/activate
# 安装依赖包
(venv)$ pip install -r requirements.txt

(venv)$ python api.py
```

## Deploying

```bash
nohup gunicorn api:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker --max-requests 1000 &
```

## TODO

因为放假期间没有通知和作业以及课程表可以测试，因此 `course` 的功能暂缓开发。

### 需要登录的查询

- <del>`/user`</del>
  - <del>`/user/token`</del>
  - <del>`/user/info`</del>
- <del>`/library`</del>
  - <del>`/library/borrow`</del>
- <del>`/card`</del>
  - <del>`/card/balance`</del>
  - <del>`/card/consume`</del>
  - <del>`/card/summary`</del>
- <del>`/dormitory`</del>
  - <del>`/dormitory/info`</del>
  - <del>`/dormitory/health`</del>
  - <del>`/dormitory/energy`</del>(use `/public/energy`)
- <del>`/score`</del>
- `/course`
  - `/course/schedule`
  - `/course/reminder`

### 不需要登录的查询

- <del>`/public/energy`</del>
