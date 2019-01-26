import asyncio

import aiohttp
from sanic.exceptions import Unauthorized
from bs4 import BeautifulSoup


async def auth_cookie(username: str, password: str):
    """ 获取一个 SDUT AuthServer 的 Cookie（七天有效期） """
    async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
        # 获取页面参数
        async with session.get('http://authserver.sdut.edu.cn/authserver/login') as resp:
            text = await resp.text()

        soup = BeautifulSoup(text, 'html.parser')
        ipts = soup.form.find_all('input')
        data = {
            'username': username,
            'password': password,
            'rememberMe': 'on',  # 七天内记住我
        }
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')

        # 提交登录
        # TODO: 手动处理跳转
        async with session.post('http://authserver.sdut.edu.cn/authserver/login', data=data) as resp:
            text = await resp.text()
            url = resp.url

        # 若页面跳转至首页，则说明登录成功
        if url == 'http://authserver.sdut.edu.cn/authserver/index.do':
            return True
        # 若页面跳转回登录界面，则说明登录失败(用户名或密码错误)
        if url == 'http://authserver.sdut.edu.cn/authserver/login':
            raise Unauthorized('用户名或密码错误')


if __name__ == '__main__':
    import os
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(auth_cookie(os.environ.get(
            'username'), os.environ.get('password')))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
