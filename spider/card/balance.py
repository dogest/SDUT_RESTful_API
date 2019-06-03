import time
import json

import aiohttp
from bs4 import BeautifulSoup

from spider.card.auth_card import auth_card
from spider.ehall.auth_ehall import auth_ehall


async def balance(cookies: dict):
    """ 获取用户校园卡余额信息 """
    # 校园卡平台只能通过 IP 访问，因此这里要使用 Unsafe CookieJar
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_ehall(session, cookies)
        # 校园卡平台无法访问，换用其他接口
        # await auth_card(session)

        url = f'http://ehall.sdut.edu.cn/jsonp/personalRemind/view.do?amp_jsonp_callback=callback&_={int(time.time() * 1000)}'

        async with session.get(url) as resp:
            text = await resp.text()
        json_data = json.loads(text[9:-1])

        bal = '获取失败'
        userid = '获取失败'
        for item in json_data['infoList']:
            if item['title'] == '一卡通信息':
                bal = item['imptInfo'][5:-1]
                userid = item['subTitle'][3:]
                break

        data = {
            'userid': userid,
            'balance': bal
        }
    return data
