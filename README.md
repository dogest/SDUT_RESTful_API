# SDUT RESTful API

一些有关于 SDUT 的 API 封装

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

### Gunicorn

```bash
nohup gunicorn api:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker --max-requests 1000 &
```

### Supervisor

你需要先将配置写入 `/etc/supervisord.conf`：

```conf
[program:SDUT_RESTful_API]
command=/path/to/SDUT_RESTful_API/venv/bin/gunicorn api:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker --max-requests 1000
directory=/path/to/SDUT_RESTful_API
stdout_logfile=/path/to/SDUT_RESTful_API/stdout.log
stderr_logfile=/path/to/SDUT_RESTful_API/stderr.log
redirect_stderr=True
environment=PRODUCTION=1
```

然后启动它：

```bash
$ sudo supervisorctl reread  # 如果这句执行失败的话，可以尝试重启 `sudo supervisord`
$ sudo supervisorctl update
$ sudo supervisorctl start SDUT_RESTful_API
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
- <del>`/schedule`</del>

### 不需要登录的查询

- <del>`/public/energy`</del>
