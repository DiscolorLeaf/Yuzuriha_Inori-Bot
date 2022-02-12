from nonebot import on_message
from nonebot.adapters.cqhttp import MessageSegment, Message
from nonebot.rule import startswith
from .pixiv_ import get_picture


sese = on_message(rule=startswith('涩涩'), priority=10)


@sese.handle()
async def handle_func():
    p = await get_picture()
    if not p:
        return False
    sese.block = True
    url = f'https://www.pixiv.net/artworks/{p.id}'
    msg: Message = MessageSegment.text(url) + MessageSegment.image(file=p.pic)
    await sese.finish(msg)
