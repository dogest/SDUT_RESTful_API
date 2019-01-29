import json
import time

import aiohttp

from spider.edu_manage.auth_edu_manage import auth_edu_manage


def make_grade(score_data: list):
    """ 计算绩点 """
    # 计算依据：http://210.44.176.116/cjcx/，学分计算方法

    unique_dict = {}
    for item in score_data:
        # 只计算非公选课成绩
        # TODO: 此处存疑
        if item['course_nature'].strip() == '公选课' or item['course_nature'].strip() == '创新创业':
            continue
        course_id = item['course_id']
        point = float(item['point'])
        # 同样的课程只计算分数最高的一次
        if 'course_id' not in unique_dict or unique_dict[course_id]['point'] < point:
            unique_dict[course_id] = item

    # 课程学分绩点＝课程绩点 × 课程学分
    # 平均学分绩点＝(∑课程学分绩点) / (∑课程学分)
    all_grade = 0
    all_score = 0
    for course_id in unique_dict:
        # 此处使用 point 进行计算
        point = float(unique_dict[course_id]['point'])
        score = float(unique_dict[course_id]['score'])
        if point != 0:
            grade = 60 + (point - 1) * 10
            all_grade += grade * score
        all_score += score

    return (all_grade / all_score)


async def score(cookies: dict, userid: str):
    """ 获取用户成绩 """
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_edu_manage(session, cookies)

        data = {
            'xh_id': userid,
            'xnm': '',
            'xqm': '',
            '_search': 'false',
            'nd': str(int(time.time() * 1000)),
            'queryModel.showCount': '1000',
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '1'
        }
        async with session.post(f'http://210.44.191.125/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N100801&su={userid}', data=data) as resp:
            text = await resp.text()

        score_data = []
        items = json.loads(text)['items']
        for item in items:
            grade = item.get('cj', '')
            year = item.get('xnm', '')
            school_year = item.get('xnmmc', '')
            semester = item.get('xqmmc', '')
            course_id = item.get('kch_id', '')
            course_code = item.get('kch', '')
            course_name = item.get('kcmc', '')
            college = item.get('jgmc', '')
            major = item.get('zymc', '')
            teacher_college = item.get('kkbmmc', '')
            course_type = item.get('kcbj', '')
            name = item.get('xm', '')
            userid = item.get('xh', '')
            sex = item.get('xb', '')
            score = item.get('xf', '')
            point = item.get('jd', '')
            state = item.get('ksxz', '')
            course_category = item.get('kclbmc', '')
            course_nature = item.get('kcxzmc', '')
            class_ = item.get('bj', '')
            teacher = item.get('jsxm', '')

            score_data.append({
                'college': college,
                'major': major,
                'class': class_,
                'name': name,
                'userid': userid,
                'sex': sex,

                'year': year,
                'school_year': school_year,
                'semester': semester,

                'course_id': course_id,
                'course_code': course_code,
                'course_name': course_name,
                'teacher': teacher,
                'teacher_college': teacher_college,
                'course_type': course_type,
                'course_category': course_category,
                'course_nature': course_nature,
                'state': state,

                'score': score,
                'grade': grade,
                'point': point,
            })

    return {
        'grade': make_grade(score_data),
        'message': '绩点仅供参考，如果需要确切的值请自行计算。',
        'scores': score_data,
    }
