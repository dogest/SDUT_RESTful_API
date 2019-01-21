"""
$ ./http_load -rate 1000 -seconds 5 urls
4682 fetches, 929 max parallel, 1.02068e+06 bytes, in 5.00004 seconds
218 mean bytes/connection
936.392 fetches/sec, 204133 bytes/sec
msecs/connect: 0.63282 mean, 3.237 max, 0.058 min
msecs/first-response: 586.754 mean, 3457.12 max, 244.35 min
HTTP response codes:
  code 200 -- 4682

从测试结果可见，请求第三方网站数据对 QPS 基本没有任何影响，在 1000 rate 下我们能做到 936 fetches/sec，基本来说已经跑满了。
再多的测试其实已经没有必要了，对这个网站来说，不大可能存在 1k/s 这种规模的并发请求……（毕竟全校才只有四万人）
而且 http_load 最大支持 1000
"""
import aiohttp
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.listener('before_server_start')
async def init(app, loop):
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)


@app.listener('after_server_stop')
async def finish(app, loop):
    loop.run_until_complete(app.session.close())
    loop.close()


@app.route("/")
async def test(request):
    url = "http://httpbin.org/get"
    async with app.aiohttp_session.get(url) as response:
        resp = await response.json()
        return json(resp)


app.run(host="0.0.0.0", port=8000, debug=True)
