from sanic.response import json


def success(**kwargs):
    return_data = {
        'error': False
    }
    return_data.update(kwargs)
    return json(return_data)


def error(status=200, **kwargs):
    return_data = {
        'error': True
    }
    return_data.update(kwargs)
    return json(return_data, status)
