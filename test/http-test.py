"""
异步请求 httpbin 网站，可以看出，在异步的情况下，可以真正并发的发起多个请求
整个程序的运行时间是最慢的一个请求返回的时间
"""
import asyncio
import time

import aiohttp


async def countdown():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            # print(resp.status)
            # print(await resp.text())
            await resp.text()


def test_async(cnt):
    tasks = [
        asyncio.ensure_future(countdown()) for _ in range(cnt)
    ]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    t = time.time()
    test_async(1)
    print(time.time() - t)  # 0.5760209560394287

    t = time.time()
    test_async(5)
    print(time.time() - t)  # 0.506770133972168

    t = time.time()
    test_async(10)
    print(time.time() - t)  # 0.5766081809997559

    loop.close()
