import aiohttp
from sanic.exceptions import Unauthorized

from spider.ehall.auth_server import auth_server, auth_server_load_cookies


async def auth_edu_manage(session: aiohttp.ClientSession, cookies: dict):
    """ 登录到山东理工大学教学综合信息服务平台 """
    # 载入 Cookies
    auth_server_load_cookies(session, cookies)

    async with session.get('http://210.44.191.125/jwglxt/jziotlogin') as resp:
        url = str(resp.url)

    if url.startswith('http://210.44.191.125/jwglxt/xtgl/index_initMenu.html'):
        return True
    else:
        raise Unauthorized('登录失败，可能是\n1. 登录凭证过期\n2. 您主动退出了登录\n3. 您修改了账号密码')
