import asyncio

import aiohttp
from bs4 import BeautifulSoup
from sanic.exceptions import Forbidden, ServerError, Unauthorized
from yarl import URL

from spider.ua import ua


def auth_server_dump_cookies(session: aiohttp.ClientSession) -> dict:
    """ 导出 AuthServer 的 Cookies """
    cookies = {}
    for _key, cookie in session.cookie_jar.filter_cookies('http://authserver.sdut.edu.cn').items():
        cookies[cookie.key] = cookie.value
    return cookies


def auth_server_load_cookies(session: aiohttp.ClientSession, cookies: dict):
    """ 导入 Authserver 的 Cookies """
    session.cookie_jar.update_cookies(
        cookies, URL('http://authserver.sdut.edu.cn'))


async def auth_server(session: aiohttp.ClientSession, username: str, password: str):
    """ 登录到 SDUT AuthServer（七天有效期） """
    # 获取页面参数
    async with session.get('http://authserver.sdut.edu.cn/authserver/login') as resp:
        text = await resp.text()
        cookies = resp.cookies
    soup = BeautifulSoup(text, 'html.parser')
    ipts = soup.form.find_all('input')
    data = {
        'username': username,
        'password': password,
        'rememberMe': 'on',  # 七天内记住我
    }
    headers = {
        'User-Agent': ua.random,
    }
    for ipt in ipts:
        if ipt.get('value'):
            data[ipt.get('name')] = ipt.get('value')

    JSESSIONID_auth = cookies.get('JSESSIONID_auth').value

    # 提交登录
    # 山东理工大学统一登录平台有一处 Set-Cookie 错误，Python 没有对错误的格式进行兼容
    # 手动处理第一次跳转，处理格式兼容
    async with session.post(f'http://authserver.sdut.edu.cn/authserver/login;{JSESSIONID_auth}', data=data, headers=headers, allow_redirects=False) as resp:
        headers = resp.headers

        next_url = headers.get('Location')

        for key in headers:
            if key.lower() == 'set-cookie' and headers[key].startswith('CASTGC'):
                castgc = headers[key].split(';')[0][7:]
                session.cookie_jar.update_cookies(
                    {'CASTGC': castgc}, URL('http://authserver.sdut.edu.cn/authserver'))
                break
        else:
            raise Unauthorized(
                '获取 Cookie 失败，请检查用户名与密码。如果问题持续出现，请联系作者。')

    # 手动进行后续的跳转
    async with session.get(next_url) as resp:
        text = await resp.text()
        url = str(resp.url)

    # 若页面跳转至首页，则说明登录成功
    if url == 'http://authserver.sdut.edu.cn/authserver/index.do':
        return True
    # 若页面跳转回登录界面，则说明登录失败(用户名或密码错误)
    elif url == 'http://authserver.sdut.edu.cn/authserver/login':
        raise Unauthorized('用户名或密码错误')
    elif url == 'http://authserver.sdut.edu.cn/authserver/pcImproveInfo.do':
        raise Forbidden('需要修改初始密码后使用')
    else:
        raise ServerError('发生意料之外的错误，如果问题持续出现，请联系作者。')


if __name__ == '__main__':
    import os
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(auth_server(
            aiohttp.ClientSession(),
            os.environ.get('username'),
            os.environ.get('password')))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
