import aiohttp
from sanic.exceptions import Unauthorized

from spider.ehall.auth_server import auth_server, auth_server_load_cookies


async def auth_ehall(session: aiohttp.ClientSession, cookies: dict):
    """ 登录到 ehall 平台 """
    # 载入 Cookies
    auth_server_load_cookies(session, cookies)

    async with session.get('http://ehall.sdut.edu.cn/login?service=http://ehall.sdut.edu.cn/new/ehall.html', allow_redirects=False) as resp:
        url = str(resp.url)

    if url == 'http://ehall.sdut.edu.cn/new/ehall.html':
        return True
    else:
        raise Unauthorized('登录失败，可能是\n1. 登录凭证过期\n2. 您主动退出了登录\n3. 您修改了账号密码')
