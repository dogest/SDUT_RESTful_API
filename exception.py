from sanic import Blueprint
from sanic.exceptions import NotFound, Unauthorized, ServerError
from sanic.response import json

from utils import error, success

ex = Blueprint('exception')


@ex.exception(Unauthorized)
async def unauthorized(request, exception):
    """ 用于处理账号错误 """
    return error(message=f'{exception}', status=401)


@ex.exception(ServerError)
async def server_error(request, exception):
    """ 用于处理系统错误 """
    return error(message=f'{exception}', status=500)


@ex.exception(NotFound)
async def not_found(request, exception):
    """ 处理 404 """
    return error(message=f'URL {request.url} Not Found')
