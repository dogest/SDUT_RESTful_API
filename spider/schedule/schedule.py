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


def sort_schedule(raw_data: list) -> list:
    """ 按照上课时间对课程排序 """
    return sorted(
        raw_data,
        key=lambda item: (
            int(item['day_of_week']),
            int(item['duration_of_class'].split('-')[0])
        )
    )


def list_duration_range(duration_str: str) -> list:
    """
    将字符串的上课时间信息解析为列表
    >>> list_duration_range('1-2')
    [1, 2]
    >>> list_duration_range('10-17')
    [10, 11, 12, 13, 14, 15, 16, 17]
    >>> list_duration_range('9')
    [9]
    >>> list_duration_range('10-12(双)')
    [10, 12]
    >>> list_duration_range('1-3,7-9')
    [1, 2, 3, 7, 8, 9]
    >>> list_duration_range('10-12(双),13-17')
    [10, 12, 13, 14, 15, 16, 17]
    """
    rlist = []
    # 首先按照逗号分割多个情况
    if ',' in duration_str:
        durations = duration_str.split(',')
    else:
        durations = [duration_str]
    # 判断是否为单双周的课程
    for item in durations:
        if '-' not in item:
            rlist.append(int(item))
            continue
        if '(单)' in item:
            item = item[:-3]
            l, r = [int(x) for x in item.split('-')]
            if l % 2 == 0:
                l += 1
            rlist += list(range(int(l), int(r) + 1, 2))
        elif '(双)' in item:
            item = item[:-3]
            l, r = [int(x) for x in item.split('-')]
            if l % 2 != 0:
                l += 1
            rlist += list(range(int(l), int(r) + 1, 2))
        else:
            l, r = [int(x) for x in item.split('-')]
            rlist += list(range(int(l), int(r) + 1))
    return rlist


def fields_map(raw_data: dict) -> dict:
    """ 将教务管理系统的拼音字段转换为英文字段 """
    data = {}

    data['schedule'] = []
    for item in raw_data['kbList']:
        t = {}
        t['duration_of_class'] = item['jcor']
        t['duration_of_class_list'] = list_duration_range(
            t['duration_of_class'])
        t['duration_of_week'] = item['zcd'].replace('周', '')
        t['duration_of_week_list'] = list_duration_range(t['duration_of_week'])
        t['classroom'] = item['cdmc']
        t['class_name'] = item['kcmc']
        t['day_of_week'] = item['xqj']
        t['teacher_name'] = item['xm']
        data['schedule'].append(t)
    data['schedule'] = sort_schedule(data['schedule'])

    data['extra'] = []
    for item in raw_data['sjkList']:
        t = {}
        t['class_name'] = item['kcmc']
        t['teacher_name'] = item['xm']
        t['duration_of_week'] = item['qsjsz'].replace('周', '')
        t['duration_of_week_list'] = list_duration_range(t['duration_of_week'])
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
