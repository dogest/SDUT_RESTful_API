import json
import time

import aiohttp
from sanic.exceptions import ServerError, Unauthorized

from spider.ehall.auth_server import auth_server, auth_server_load_cookies


async def auth_ehall(session: aiohttp.ClientSession, cookies: dict):
    """ 登录到 ehall 平台 """
    # 载入 Cookies
    auth_server_load_cookies(session, cookies)

    async with session.get('http://ehall.sdut.edu.cn/login?service=http://ehall.sdut.edu.cn/new/ehall.html') as resp:
        url = str(resp.url)

    if url == 'http://ehall.sdut.edu.cn/new/ehall.html':
        return True
    else:
        if '?ticket=' in url:
            raise ServerError('认证错误，请重试')
        print(url)
        raise Unauthorized('登录失败，可能是\n1. 登录凭证过期\n2. 您主动退出了登录\n3. 您修改了账号密码')


async def user_info(cookies: dict):
    """ 获取用户基本信息 """
    async with aiohttp.ClientSession() as session:
        # 登录到 ehall
        await auth_ehall(session, cookies)

        async with session.get(f'http://ehall.sdut.edu.cn/jsonp/userDesktopInfo.json?amp_jsonp_callback=f&_={int(time.time() * 1000)}') as resp:
            text = await resp.text()

        data = json.loads(text[2:-1])
        if not data['hasLogin']:
            raise Unauthorized('登录凭证已失效。')

        user_info_data = {
            'name': data.get('userName'),
            'userid': data.get('userId'),
            'department': data.get('userDepartment')
        }
    return user_info_data
