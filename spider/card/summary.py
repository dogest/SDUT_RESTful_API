import datetime

import aiohttp
from bs4 import BeautifulSoup

from spider.card.auth_card import auth_card
from spider.ehall.auth_ehall import auth_ehall


async def summary(cookies: dict, userid: str, start_date: str = None, end_date: str = None):
    """ 获取用户校园卡消费汇总信息 """
    # 校园卡平台只能通过 IP 访问，因此这里要使用 Unsafe CookieJar
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_ehall(session, cookies)
        await auth_card(session)

        if end_date is None:
            end_date = datetime.date.today().strftime("%Y%m%d")
        # 默认查询一周
        if start_date is None:
            start_date = (datetime.date.today() -
                          datetime.timedelta(days=7)).strftime("%Y%m%d")

        url = f'http://211.64.27.136/SelfSearch/EcardInfo/CustStateInfo_Seach.aspx?outid={userid}'
        async with session.get(url) as resp:
            text = await resp.text()
        soup = BeautifulSoup(text, 'html.parser')
        ipts = soup.find_all('input')

        # 将要提交的值填充
        data = {
            'ctl00$ContentPlaceHolder1$CustStateInfoAscx1$ScriptManager1': 'ctl00$ContentPlaceHolder1$CustStateInfoAscx1$ScriptManager1|ctl00$ContentPlaceHolder1$CustStateInfoAscx1$btnSeach',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00$ContentPlaceHolder1$CustStateInfoAscx1$btnSeach': ''
        }
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')
        data['ctl00$ContentPlaceHolder1$CustStateInfoAscx1$sDateTime'] = start_date
        data['ctl00$ContentPlaceHolder1$CustStateInfoAscx1$eDateTime'] = end_date

        async with session.post(url, data=data) as resp:
            text = await resp.text()
        if '没有查询到相关数据！！无返回结果！' in text:
            return []
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table').find_all('table')[3]
        trs = table.find_all('tr')
        rdata = []
        for tr in trs[2:]:
            tds = tr.find_all('td')
            rdata.append({
                'id': tds[0].string,
                'reason': tds[1].string,
                'amount': tds[2].string,
                'ext_1': tds[3].string,
                'ext_2': tds[4].string,
                'ext_3': tds[5].string,
            })
    return rdata
