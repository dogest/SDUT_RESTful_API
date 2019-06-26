import aiohttp
from sanic.exceptions import Forbidden, Unauthorized, ServerError

from spider.ehall.auth_server import auth_server, auth_server_load_cookies


async def auth_edu_manage(session: aiohttp.ClientSession, cookies: dict):
    """ 登录到山东理工大学教学综合信息服务平台 """
    # 载入 Cookies
    auth_server_load_cookies(session, cookies)

    async with session.get('http://210.44.191.125/sso/jziotlogin', allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')

    async with session.get(next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
    async with session.get(next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
    async with session.get(next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
    async with session.get(next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
    async with session.get('http://210.44.191.125' + next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
    async with session.get('http://210.44.191.125' + next_url, allow_redirects=False) as resp:
        next_url = resp.headers.get('Location')
        text = await resp.text()
        url = str(resp.url)

    if '当前登录用户不允许访问目标应用' in text:
        raise Forbidden('当前登录用户不允许访问目标应用')

    if url.startswith('http://210.44.191.125/jwglxt/xtgl/index_initMenu.html'):
        return True
    else:
        if '?ticket=' in url:
            raise ServerError('认证错误，请重试')
        print(url)
        raise Unauthorized('登录失败，可能是\n1. 登录凭证过期\n2. 您主动退出了登录\n3. 您修改了账号密码')
