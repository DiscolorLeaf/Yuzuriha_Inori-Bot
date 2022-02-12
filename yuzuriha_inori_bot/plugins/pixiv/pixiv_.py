import httpx
from typing import List


class pic:
    id: int
    pic: str  # url for qq find pic
    artwork: str  # url for show in group


async def get_picture(tags='') -> pic:
    url = "http://api.a60.one:404/"
    if tags:
        url += 'get/tags/' + tags
    # url += '?only=true'
    async with httpx.AsyncClient() as client:
        res = await client.get(url)  # , params={'only': True})
        if res.status_code != 200:
            return False
        res = res.json()

    p = pic()
    res = res['data']['imgs'][0]
    p.id = int(res['pic'].split('_')[0])
    p.pic = res['url']
    p.artwork = f'https://www.pixiv.net/artworks/{p.id}'
    return p
