from nonebot import on_command
from nonebot.adapters.cqhttp import MessageSegment, Message, GroupMessageEvent, GroupRecallNoticeEvent, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import startswith, keyword
from nonebot.adapters.onebot.v11 import Bot
from .pixiv_ import get_picture

status = True

approve = on_command(cmd='可以涩涩', permission=SUPERUSER)
forbid = on_command(cmd='不准涩涩', permission=SUPERUSER)


@forbid.handle()
@approve.handle()
async def set_status(bot: Bot, event: MessageEvent):
    command = event.get_plaintext()
    global status
    if command == '可以涩涩':
        status = True
        await approve.send('集,拜托了,请使用我吧!')
    elif command == '不准涩涩':
        status = False
        await forbid.send('涩涩已关闭')


sese = on_command(cmd='涩涩', aliases={'祈妹涩涩', '楪祈涩涩'}, priority=10)


@sese.handle()
async def send_picture(bot: Bot, event: MessageEvent):
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
        msg: Message = MessageSegment.text('不可以涩涩哦') + MessageSegment.image(
            file='https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwww.pianshen.com%2Fimages%2F420%2F7daaed279358c25bbbbab825165ad564.JPEG&refer=http%3A%2F%2Fwww.pianshen.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1647344584&t=b4d67053a250cf5a3690fe621863d99d')
        await sese.finish(msg)
