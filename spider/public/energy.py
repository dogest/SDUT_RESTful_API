import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup


async def login(session: aiohttp.ClientSession):
    """ 登录到后勤服务平台 """
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


async def do_search(session: aiohttp.ClientSession, floor: str, room: str):
    """ 查询电量 """
    async with session.get('http://hqfw.sdut.edu.cn/stu_elc.aspx') as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, 'html.parser')
    ipts = soup.find_all('input')
    data = {}
    for ipt in ipts:
        if ipt.get('value'):
            data[ipt.get('name')] = ipt.get('value')
    data['ctl00$MainContent$campus'] = '0' if room[0] == 'E' else '1'
    data['ctl00$MainContent$buildingwest'] = floor
    data['ctl00$MainContent$roomnumber'] = room

    async with session.post('http://hqfw.sdut.edu.cn/stu_elc.aspx', data=data) as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, 'html.parser')
    text_area = soup.find(id='MainContent_TextBox1')

    text_area = text_area.string
    values = text_area.split('\n')

    rdata = {}
    for value in values:
        value = value.strip()
        if value.startswith('您所查询的房间为：'):
            rdata['room'] = value[9:-1]
        elif value.startswith('根据您的用电规律'):
            _s = value[16:-2].split(' - ')
            rdata['lower'] = _s[0]
            rdata['upper'] = _s[1]
        elif value.startswith('当前用电状态为：'):
            rdata['status'] = value[8:-1]
        elif value.startswith('在'):
            _a, _b = value.split('，')
            _d = _a[1:-1]
            _e = _b[6:-2]
            rdata['date'] = datetime.strptime(
                _d, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            rdata['energy'] = _e
    return rdata


async def energy(floor: str, room: str):
    """
    查询宿舍剩余电量
    Usage: energy('06#', '627')
    """
    async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
        await login(session)
        data = await do_search(session, floor, room)

    return data

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(energy('06#', '627'))
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
