from sanic.response import json


def success(**kwargs):
    return_data = {
        'error': False
    }
    return_data.update(kwargs)
    return json(return_data)


def error(**kwargs):
    return_data = {
        'error': True
    }
    return_data.update(kwargs)
    return json(return_data)
