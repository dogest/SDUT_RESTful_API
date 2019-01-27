import json

import aiohttp

from spider.ehall.auth_ehall import auth_ehall


async def health(cookies: dict):
    """ 获取用户宿舍卫生 """
    async with aiohttp.ClientSession() as session:
        await auth_ehall(session, cookies)

        await session.get('http://ehall.sdut.edu.cn/appShow?appId=4606888687682093')

        async with session.get('http://ehall.sdut.edu.cn/xsfw/sys/sswsapp/modules/dorm_health_student/sswsxs_sswsxsbg.do?pageSize=100&pageNumber=1') as resp:
            text = await resp.text()
        rdata = json.loads(text)
        rlist = []
        for i in rdata['datas']['sswsxs_sswsxsbg']['rows']:
            d = {
                'floor': i['SSLMC'],
                'room': i['FJH'],
                'week': i['ZC'],
                'date': i['JCRQ'],
                'score': i['FS']
            }
            rlist.append(d)
    return rlist
