from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from sanic.exceptions import Unauthorized

from spider.ehall.auth_ehall import auth_ehall


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


async def energy(cookies: dict, floor: str, room: str):
    """ 获取宿舍电量 """
    async with aiohttp.ClientSession() as session:
        await auth_ehall(session, cookies)

        async with session.get(f'http://hqfw.sdut.edu.cn/login_ehall.aspx') as resp:
            text = await resp.text()

        if '"lklogin">[欢迎您,' not in text:
            raise Unauthorized('登录失败，可能是\n1. 登录凭证过期\n2. 您主动退出了登录\n3. 您修改了账号密码')
        data = await do_search(session, floor, room)

    return data
