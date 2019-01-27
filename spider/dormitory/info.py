import aiohttp
import json
from spider.ehall.auth_ehall import auth_ehall


def trans_floor(floor: str):
    """ 将宿舍数据转换为后续查询的样式 """
    floor_dict = {
        '东区1号公寓': 'E01#',
        '东区2号公寓': 'E02#',
        '东区4号公寓': 'E04#',
        '东区6号公寓': 'E06#',
        '东区8号公寓': 'E08#',
        '东区9号公寓': 'E09#',
        '东区10号公寓': 'E10#',
        '1号公寓北楼': '01#北',
        '1号公寓南楼': '01#南',
        '2号公寓北楼': '02#北',
        '2号公寓南楼': '02#南',
        '3号公寓北楼': '03#北',
        '3号公寓南楼': '03#南',
        '4号公寓北楼': '04#北',
        '4号公寓南楼': '04#南',
        '5号公寓': '05#',
        '6号公寓': '06#',
        '7号公寓': '07#',
        '8号公寓': '08#',
        '9号公寓': '09#',
        '10号公寓': '10#',
        '11号公寓': '11#',
        '12号公寓': '12#',
        '13号公寓北楼': '13#北',
        '13号公寓南楼': '13#南',
        '14号公寓': '14#',
        '15号公寓': '15#',
        '16号公寓': '16#',
        '17号公寓': '17#',
        '18号公寓': '18#',
        '19号公寓': '19#',
        '20号公寓': '20#',
        '21号公寓': '21#',
        '22号公寓': '22#',
        '研究生北楼': '研男#',
        '研究生南楼': '研女#',
        '研究生A楼': 'A-',
        '研究生C楼': 'C-',
    }
    return floor_dict[floor]


async def info(cookies: dict):
    """ 获取用户宿舍基本信息 """
    async with aiohttp.ClientSession() as session:
        await auth_ehall(session, cookies)

        # 注册 app
        await session.get('http://ehall.sdut.edu.cn/appShow?appId=4618295887225301')
        data = {
            'requestParamStr': '{"bh":1}'
        }

        async with session.post('http://ehall.sdut.edu.cn/xsfw/sys/sswjapp/modules/stu/queryDiscipline.do', data=data) as resp:
            text = await resp.text()

        rdata = json.loads(text)
    campus = rdata['data']['XQMC']
    floor = rdata['data']['SSLMC']
    room = rdata['data']['FJH']
    raw_floor = trans_floor(floor)

    return {
        'campus': campus,
        'floor': floor,
        'room': room,
        'raw_floor': raw_floor
    }
