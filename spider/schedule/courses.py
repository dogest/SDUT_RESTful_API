import aiohttp
from bs4 import BeautifulSoup
from sanic.exceptions import Unauthorized
import json

from spider.ehall.auth_ehall import auth_ehall


async def courses(cookies: dict):
    """ 获取用户基本课程信息 """
    async with aiohttp.ClientSession() as session:
        await auth_ehall(session, cookies)

        async with session.get(f'http://ehall.sdut.edu.cn/publicapp/sys/mykbxt/myTimeTable/queryThisWeekCourses.do') as resp:
            text = await resp.text()

        data = json.loads(text)

    return data
