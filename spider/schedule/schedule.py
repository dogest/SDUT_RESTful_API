import aiohttp
from bs4 import BeautifulSoup
from sanic.exceptions import Unauthorized
import json

from spider.ehall.auth_ehall import auth_ehall
from spider.edu_manage.auth_edu_manage import auth_edu_manage


async def courses(cookies: dict, year: str, semester: str):
    """ 获取用户详细课程信息 """
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_edu_manage(session, cookies)

        semester = '3' if semester == '1' else '12'

        async with session.get(f'http://210.44.191.125/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151&xnm={year}&xqm={semester}') as resp:
            text = await resp.text()

        data = fields_map(json.loads(text))

    return data


def fields_map(raw_data: dict) -> dict:
    """ 将教务管理系统的拼音字段转换为英文字段 """
    data = {}

    data['schedule'] = []
    for item in raw_data['kbList']:
        t = {}
        t['duration_of_class'] = item['jcor']
        t['duration_of_week'] = item['zcd']
        t['classroom'] = item['cdmc']
        t['class_name'] = item['kcmc']
        t['day_of_week'] = item['xqj']
        t['teacher_name'] = item['xm']
        data['schedule'].append(t)

    data['extra'] = []
    for item in raw_data['sjkList']:
        t = {}
        t['class_name'] = item['kcmc']
        t['teacher_name'] = item['xm']
        t['duration_of_week'] = item['qsjsz']
        data['extra'].append(t)

    data['note'] = []
    for item in raw_data['xqbzxxszList']:
        t = {}
        t['content'] = item['bzxx']
        data['note'].append(t)

    data['separator'] = []
    for item in raw_data['xsbjList']:
        t = {}
        t['key'] = item['xslxbj']
        t['value'] = item['xsmc']
        data['separator'].append(t)

    data['name'] = raw_data['xsxx']['XM']
    data['userid'] = raw_data['xsxx']['XH']
    data['year'] = raw_data['xsxx']['XNM']
    data['semester'] = raw_data['xsxx']['XQMMC']

    return data
