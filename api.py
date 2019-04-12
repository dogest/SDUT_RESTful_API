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
from spider.card import balance, consume, summary
from spider.dormitory import health as dorm_health
from spider.dormitory import info as dorm_info
from spider.schedule.schedule import courses as schedule_courses
from spider.ehall import auth_ehall
from spider.ehall.auth_server import auth_server, auth_server_dump_cookies
from spider.schedule.courses import courses
from spider.library.borrow import borrow
from spider.public.energy import energy
from spider.score import score as stu_score
from utils import error, success

app = Sanic(__name__)

# 载入错误处理蓝图
app.blueprint(ex)


@app.listener('before_server_start')
async def init(app, loop):
    app.config.redis = await aioredis.create_redis_pool('redis://localhost', loop=loop)


@app.listener('after_server_stop')
async def finish(app, loop):
    # loop.run_until_complete(app.config.redis.close())
    await app.config.redis.wait_closed()
    loop.close()


async def get_cookies(request: Request) -> dict:
    """ 通过 Token 获取 Cookies """
    token = request.form.get('token') or request.json.get('token')

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
    username = request.form.get('username') or request.json.get('username')
    password = request.form.get('password') or request.json.get('password')

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


@app.route('/user/token/exist', methods=['POST'])
async def token_exist(request: Request):
    """ 判断本地有没有 token """
    cookies = await get_cookies(request)
    return success(cookies=python_json.dumps(cookies))


@app.route('/user/info', methods=['POST'])
async def user_info(request: Request):
    """ 返回用户基本信息 """
    cookies = await get_cookies(request)
    user_info_data = await auth_ehall.user_info(cookies)

    return success(data=user_info_data)


@app.route('/library/borrow', methods=['POST'])
async def library_borrow(request: Request):
    """ 返回用户图书借阅情况 """
    cookies = await get_cookies(request)
    borrow_data = await borrow(cookies)

    return success(data={'info': borrow_data['info'], 'history': borrow_data['history']})


@app.route('/card/balance', methods=['POST'])
async def card_balance(request: Request):
    """ 返回用户校园卡余额 """
    cookies = await get_cookies(request)
    balance_data = await balance.balance(cookies)

    return success(data=balance_data)


@app.route('/card/consume', methods=['POST'])
async def card_consume(request: Request):
    """ 返回用户校园卡最近交易 """
    cookies = await get_cookies(request)
    userid = request.form.get('userid') or request.json.get('userid')
    if not userid:
        return error(message='请提供 userid!')
    consume_data = await consume.consume(cookies, userid)

    return success(data=consume_data)


@app.route('/card/summary', methods=['POST'])
async def card_summary(request: Request):
    """ 返回用户校园卡交易汇总 """
    cookies = await get_cookies(request)
    userid = request.form.get('userid') or request.json.get('userid')
    start_date = request.form.get(
        'start_date') or request.json.get('start_date')
    end_date = request.form.get('end_date') or request.json.get('end_date')
    if not userid:
        return error(status=400, message='请提供 userid!')
    summary_data = await summary.summary(cookies, userid, start_date, end_date)

    return success(data=summary_data)


@app.route('/dormitory/info', methods=['POST'])
async def dormitory_info(request: Request):
    """ 返回用户宿舍基本信息 """
    cookies = await get_cookies(request)
    info_data = await dorm_info.info(cookies)

    return success(data=info_data)


@app.route('/dormitory/health', methods=['POST'])
async def dormitory_health(request: Request):
    """ 返回用户宿舍卫生信息 """
    cookies = await get_cookies(request)
    health_data = await dorm_health.health(cookies)

    return success(data=health_data)


@app.route('/score', methods=['POST'])
async def score(request: Request):
    """ 返回用户成绩与绩点 """
    cookies = await get_cookies(request)

    userid = request.form.get('userid') or request.json.get('userid')
    if userid is None:
        return error(status=400, message='请提供 userid!')
    score_data = await stu_score.score(cookies, userid)

    return success(data=score_data)


@app.route('/public/energy', methods=['POST'])
async def public_energy(request: Request):
    """ 查询电量 """
    floor = request.form.get('floor') or request.json.get('floor')
    room = request.form.get('room') or request.json.get('room')
    data = await energy(floor, room)
    return success(data=data)


@app.route('/schedule', methods=['POST'])
async def schedule(request: Request):
    """ 查询课程表 """
    cookies = await get_cookies(request)
    week_data = await courses(cookies)
    year, _, semester = week_data['schoolYearTerm'].split('-')
    data = await schedule_courses(cookies, year, semester)
    data['current_week'] = week_data['weekOfTerm']
    return success(data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
