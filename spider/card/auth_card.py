import json

import aiohttp
from sanic.exceptions import Unauthorized


async def auth_card(session: aiohttp.ClientSession):
    """ 登录到校园卡网站 """
    # 通过统一登录平台登录至校园卡网站
    async with session.get('http://ehall.sdut.edu.cn/publicapp/sys/xkpyktjc/single_sign.do') as resp:
        text = await resp.text()
    data = json.loads(text)
    async with session.post(data['url'], data=data) as resp:
        url = str(resp.url)
    if url != 'http://211.64.27.136/SelfSearch/Default.aspx':
        raise Unauthorized('登录凭证已失效。')
    return True
