import asyncio
import re
import httpx
import random
import time

from httpx import Headers


class pic:
    id: int
    title: str
    artist: str
    pic: str
    artwork: str
    tags: list[str]
    page_count: int
    create_date: str


def get_headers(referer: str = ''):
    h = {
        b"Accept": b"*/*",
        b"Accept-Encoding": "gzip, deflate, br",
        b"Connection": b"keep-alive",
        b"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
    }

    if referer != '':
        h['referer'] = referer.encode('utf-8')

    return Headers(h)


async def get_pic(ts=time.time() - 2 * 24 * 3600, failed: int = 0):
    if failed >= 30:
        return False
    url = f'https://pixiviz-api-hk.pwp.link/v1/illust/rank?' \
          f'mode=week&date={time.strftime("%Y-%m-%d", time.localtime(ts))}&page={random.randint(1, 15)}'
    async with httpx.AsyncClient(timeout=None) as client:

        try:
            res = await asyncio.wait_for(client.get(url=url, headers=get_headers('https://pixiviz.xyz/')), 5)
        except asyncio.TimeoutError:
            failed += 1
            return await get_pic(ts - 24 * 3600, failed + 1)

        if res.status_code == 200:
            ret = res.json()
            if not ret['illusts']:
                failed += 1
                return await get_pic(ts - 24 * 3600, failed + 1)
            else:
                return ret
        elif res.status_code >= 500:
            failed += 1
            return await get_pic(ts - 24 * 3600, failed + 1)


async def test_pic(url):
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            res = await asyncio.wait_for(client.get(url=url, headers=get_headers()), 5)
        except asyncio.TimeoutError:
            return False
        if res.status_code != 200:
            return False
        else:
            return True


def pic_filter(pics: list):
    for i, p in enumerate(pics):
        if p['type'] == 'manga':
            pics.pop(i)
    return pics


async def get_picture(ret=None, count: int = 0, failed: int = 0) -> pic:
    if ret is None:
        ret = await get_pic()
        ret = ret['illusts']
        ret = pic_filter(ret)
        count = len(ret)
    single = ret[random.randint(0, count - 1)]

    date: str = single['create_date']
    date = re.match(r'[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+', date).group()
    date = date.replace("-", "/").replace("T", "/").replace(":", "/")

    p = pic()
    p.id = single['id']
    p.title = single['title']
    p.artist = single['user']['name']
    p.pic = f'https://proxy.pixivel.moe/c/540x540_70/img-master/img/{date}/{p.id}_p0_master1200.jpg'
    p.artwork = f'https://www.pixiv.net/artworks/{p.id}'
    p.tags = []
    for tag in single['tags']:
        p.tags.append(tag['name'])
    p.page_count = single['page_count']
    p.create_date = single['create_date']

    if await test_pic(p.pic) is True:
        return p
    else:
        if failed == count:
            raise FailedGetPicError('获取图片链接失败')
        return await get_picture(ret, count, failed + 1)


class FailedGetPicError(Exception):
    def __int__(self, msg: str = ''):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
