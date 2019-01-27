import asyncio
import json as python_json
import uuid

import aiohttp
import aioredis
from sanic import Sanic
from sanic.exceptions import Unauthorized
from sanic.request import Request
from sanic.response import json

from exception import ex
from spider.ehall import auth_ehall
from spider.ehall.auth_server import auth_server, auth_server_dump_cookies
from spider.library.borrow import borrow
from spider.public.energy import energy
from utils import success

app = Sanic(__name__)

# 载入错误处理蓝图
app.blueprint(ex)


@app.listener('before_server_start')
async def init(app, loop):
    app.config.redis = await aioredis.create_redis_pool('redis://localhost', loop=loop)


@app.listener('after_server_stop')
async def finish(app, loop):
    loop.run_until_complete(app.config.redis.close())
    await app.config.redis.wait_closed()
    loop.close()


async def get_cookies(request: Request) -> dict:
    """ 通过 Token 获取 Cookies """
    token = request.form.get('token')

    # 获取 cookies
    cookies_str = await app.config.redis.get(token)
    if not cookies_str:
        raise Unauthorized('Token 凭证不存在，可能已经过期了（有效期七天）')
    cookies = python_json.loads(cookies_str)
    return cookies


@app.route('/')
async def index(request: Request):
    return success(data={'Hello': 'World'})


@app.route('/user/token', methods=['POST'])
async def token(request: Request):
    """ 登录，获取 cookies，创建 token，存入数据库并返回 """
    username = request.form.get('username')
    password = request.form.get('password')

    async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
        # 登录至 AuthServer，如果登录失败则会触发登录失败 401
        await auth_server(session, username, password)
        cookies = auth_server_dump_cookies(session)

    # 生成 token
    token = 'SDUTAPI_' + str(uuid.uuid4())
    cookies_str = python_json.dumps(cookies)

    # 将 token 与 cookies 存入 redis，七天有效
    await app.config.redis.setex(token, 7 * 24 * 60 * 60, cookies_str)

    # 返回 token
    return success(token=token)


@app.route('/user/info', methods=['POST'])
async def user_info(request: Request):
    """ 返回用户基本信息 """
    cookies = await get_cookies(request)
    user_info_data = await auth_ehall.user_info(cookies)

    return success(user=user_info_data)


@app.route('/library/borrow', methods=['POST'])
async def library_borrow(request: Request):
    """ 返回用户图书借阅情况 """
    cookies = await get_cookies(request)
    borrow_data = await borrow(cookies)

    return success(info=borrow_data['info'], history=borrow_data['history'])


@app.route('/public/energy', methods=['POST'])
async def public_energy(request: Request):
    """ 查询电量 """
    floor = request.form.get('floor')
    room = request.form.get('room')
    data = await energy(floor, room)
    return success(data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
