from nonebot import on_message
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, GroupRecallNoticeEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import startswith, keyword
from nonebot.adapters.onebot.v11 import Bot
from .pixiv_ import get_picture

status = True


forbid = on_message(rule=keyword('可以涩涩', '不准涩涩'), permission=SUPERUSER)


@forbid.handle()
async def set_status(bot: Bot, event: GroupMessageEvent):
    command = event.get_plaintext()
    global status
    if command == '可以涩涩':
        status = True
        await forbid.send('集,拜托了,请使用我吧!')
    else:
        status = False
        await forbid.send('。。。')


sese = on_message(rule=startswith('涩涩'), priority=10)


@sese.handle()
async def send_picture(bot: Bot, event: GroupMessageEvent):
    global status, msg_list
    if status:
        p = await get_picture()
        if not p:
            return False
        sese.block = True
        url = f'https://www.pixiv.net/artworks/{p.id}'
        msg: Message = MessageSegment.text(url) + MessageSegment.image(file=p.pic)
        await sese.finish(msg)
    else:
        await sese.send('不可以涩涩哦')
