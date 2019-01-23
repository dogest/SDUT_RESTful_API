import aiohttp
from sanic import Sanic
from sanic.response import json

from exception import ex
from spider.public.energy import energy
from utils import success

app = Sanic(__name__)

app.blueprint(ex)


@app.listener('before_server_start')
async def init(app, loop):
    """ 初始化 """
    app.config.aiohttp_session = aiohttp.ClientSession(loop=loop)


@app.listener('after_server_stop')
async def finish(app, loop):
    """ 关闭 """
    loop.run_until_complete(app.config.aiohttp_session.close())
    loop.close()


@app.route('/')
async def index(request):
    return success(data={'Hello': 'World'})


@app.route('/public/energy', methods=['POST'])
async def public_energy(request):
    """ 查询电量 """
    floor = request.form.get('floor')
    room = request.form.get('room')
    data = await energy(app.config.aiohttp_session, floor, room)
    return success(data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
