import aiohttp
from bs4 import BeautifulSoup
from sanic.exceptions import Unauthorized

from spider.ehall.auth_ehall import auth_ehall


async def borrow_info(session: aiohttp.ClientSession):
    """ 获取当前借书详情 """
    async with session.get('http://222.206.65.12/reader/book_lst.php') as resp:
        text = await resp.text()
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find('table')
    rdata = []
    trs = table.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        if len(tds) < 5:  # 判断是否有书
            break
        rdata.append({
            'title': tds[1].find('a').string,  # 图书名
            'author': tds[1].text[len(tds[1].find('a').string) + 3:],  # 作者
            'borrow_date': tds[2].string.split()[0],  # 借书日期(xxxx-yy-zz)
            'back_date': tds[3].string.split()[0],  # 应还日期(xxxx-yy-zz)
            'borrow_cnt': tds[4].string,  # 续借次数
            'site': tds[5].string  # 借书地点
        })
    return rdata


async def borrow_history(session: aiohttp.ClientSession):
    """ 获取历史借书详情 """
    data = {
        'para_string': 'all',
        'topage': '1'
    }
    async with session.post('http://222.206.65.12/reader/book_hist.php', data=data) as resp:
        text = await resp.text()

    if '您的该项记录为空' in text:
        return []
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find('table')
    rdata = []
    trs = table.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        if len(tds) < 5:
            break
        rdata.append({
            'bar_code': tds[1].string,
            'title': tds[2].string,
            'book_url': 'http://222.206.65.12' + tds[2].find('a').get('href')[2:],
            'author': tds[3].string,
            'borrow_date': tds[4].string,
            'back_date': tds[5].string,
            'site': tds[6].string
        })
    return rdata


async def borrow(cookies: dict):
    """ 获取用户图书借阅信息 """
    # 图书馆只能通过 IP 访问，因此这里要使用 Unsafe CookieJar
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        await auth_ehall(session, cookies)

        # 通过统一登录平台登录至图书馆
        async with session.get('http://authserver.sdut.edu.cn/authserver/login?service=http%3A%2F%2F222.206.65.12%2Freader%2Fhwthau.php') as resp:
            url = str(resp.url)
        if url != 'http://222.206.65.12/reader/redr_info.php':
            raise Unauthorized('登录凭证已失效。')

        data = {}
        data['info'] = await borrow_info(session)
        data['history'] = await borrow_history(session)

    return data
