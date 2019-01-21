"""
$ ./http_load -rate 1000 -seconds 5 urls 
4999 fetches, 4 max parallel, 119976 bytes, in 5 seconds
24 mean bytes/connection
999.799 fetches/sec, 23995.2 bytes/sec
msecs/connect: 0.0603129 mean, 0.815 max, 0.03 min
msecs/first-response: 0.585778 mean, 12.512 max, 0.288 min
HTTP response codes:
  code 200 -- 4999

如果使用其他同步框架或语言，就算啥也不干也很难有 1k QPS
更别说这还远远不到它的上限
"""
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import NotFound
import aioredis

app = Sanic(__name__)


@app.listener('before_server_start')
async def init(app, loop):
    app.redis = await aioredis.create_redis_pool('redis://localhost', loop=loop)


@app.listener('after_server_stop')
async def finish(app, loop):
    loop.run_until_complete(app.redis.close())
    await app.redis.wait_closed()
    loop.close()


@app.route('/')
async def test(request):
    value = await app.redis.get('key')
    return json({'value': value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=4)
