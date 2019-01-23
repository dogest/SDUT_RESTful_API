from sanic import Blueprint
from sanic.exceptions import NotFound
from sanic.response import json

from utils import error, success

ex = Blueprint('exception')


@ex.exception(NotFound)
async def not_found(request, exception):
    return error(message=f'URL {request.url} Not Found')
