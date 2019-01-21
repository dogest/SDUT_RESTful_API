from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import NotFound

app = Sanic()


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


@app.route('/user/401')
async def user_401(request):
    return json({'error': 1}, 401)


@app.route('/user/403')
async def user_403(request):
    return json({'error': 1}, 403)


@app.exception(NotFound)
async def ignore_404s(request, exception):
    return json({'error': 1, 'message': f'{request.url} not found'}, 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
