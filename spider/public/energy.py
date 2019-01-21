import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def login(session: aiohttp.ClientSession):
    # 获取预置在页面上的参数
    async with session.get('http://hqfw.sdut.edu.cn/login.aspx') as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, 'html.parser')
    ipts = soup.find_all('input')
    data = {}
    for ipt in ipts:
        if ipt.get('value'):
            data[ipt.get('name')] = ipt.get('value')
    data['ctl00$MainContent$txtName'] = '刘大钰'
    data['ctl00$MainContent$txtID'] = '15110572023'
    data.pop('ctl00$MainContent$btnCancel')

    async with session.post('http://hqfw.sdut.edu.cn/login.aspx', data=data) as resp:
        text = await resp.text()

    # 如果没有登录成功，则触发异常
    if f'欢迎您,刘大钰同学' not in text:
        # TODO: raise 401 error
        pass


async def energy(session: aiohttp.ClientSession, room):
    await login(session)
    async with session.get('http://hqfw.sdut.edu.cn/') as resp:
        text = await resp.text()
        print(text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
    tasks = [
        asyncio.ensure_future(energy(session, '06#627'))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
