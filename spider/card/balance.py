import aiohttp
from bs4 import BeautifulSoup

from spider.card.auth_card import auth_card
from spider.ehall.auth_ehall import auth_ehall


async def balance(cookies: dict):
    """ 获取用户校园卡余额信息 """
    # 校园卡平台只能通过 IP 访问，因此这里要使用 Unsafe CookieJar
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_ehall(session, cookies)
        await auth_card(session)

        async with session.get('http://211.64.27.136/SelfSearch/EcardInfo/UserBaseInfo_Seach.aspx') as resp:
            text = await resp.text()
        soup = BeautifulSoup(text, 'html.parser')
        ipts = soup.find_all('input')
        data = {
            'userid': ipts[3].get('value'),
            'name': ipts[4].get('value'),
            'balance': ipts[9].get('value')[:-2].strip()
        }
    return data
