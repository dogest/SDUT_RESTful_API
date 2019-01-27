import aiohttp
from bs4 import BeautifulSoup

from spider.card.auth_card import auth_card
from spider.ehall.auth_ehall import auth_ehall


async def consume(cookies: dict, userid: str):
    """ 获取用户校园卡最近消费信息 """
    # 校园卡平台只能通过 IP 访问，因此这里要使用 Unsafe CookieJar
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_ehall(session, cookies)
        await auth_card(session)

        async with session.get(f'http://211.64.27.136/SelfSearch/EcardInfo/CONSUMEINFO_SEACH.ASPX?outid={userid}') as resp:
            text = await resp.text()
        soup = BeautifulSoup(text, 'html.parser')
        ipts = soup.find_all('input')
        data = {
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$ScriptManager1': 'ctl00$ContentPlaceHolder1$ConsumeAscx1$ScriptManager1|ctl00$ContentPlaceHolder1$ConsumeAscx1$btnSeach',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$btnSeach': ''
        }
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')

        async with session.post(f'http://211.64.27.136/SelfSearch/EcardInfo/CONSUMEINFO_SEACH.ASPX?outid={userid}', data=data) as resp:
            text = await resp.text()

        if '没有查询到相关数据' in text:
            return []
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table').find_all('table')[3]
        trs = table.find_all('tr')
        rdata = []
        for tr in trs[2:]:
            tds = tr.find_all('td')
            time_s = tds[0].string.split('/')
            if len(time_s[1]) < 2:
                time_s[1] = '0' + time_s[1]
            _d, _t = time_s[2].split()
            if len(_d) < 2:
                _d = '0' + _d
            if len(_t) < 8:
                _t = '0' + _t
            time = '{y}-{m}-{d} {t}'.format(y=time_s[0],
                                            m=time_s[1], d=_d, t=_t)

            rdata.append({
                'time': time[:-3],  # 交易时间
                'reason': tds[1].string,  # 科目描述
                'amount': tds[2].string,  # 交易金额
                'balance': tds[4].string,  # 余额
                'position': tds[7].string,  # 工作站
                'term_name': tds[8].string  # 交易终端
            })
    return rdata
