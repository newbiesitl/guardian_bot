import asyncio
import time

async def t1():
    time.sleep(2)
    print('t1')
async def t2():
    time.sleep(1)
    print('t2')
async def main():
    t11 = asyncio.create_task(t1())
    t22 = asyncio.create_task(t2())
    await t11
    await t22

asyncio.run(main())