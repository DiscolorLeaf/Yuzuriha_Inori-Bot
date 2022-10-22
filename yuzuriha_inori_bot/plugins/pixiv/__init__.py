from nonebot import on_command
from nonebot.adapters.cqhttp import MessageSegment, Message
from nonebot.permission import SUPERUSER
from .pixiv_ import get_picture

enable = True

approve = on_command(cmd='pic enable', aliases={'pic en'}, permission=SUPERUSER)
forbid = on_command(cmd='pic disable', aliases={'pic dis'}, permission=SUPERUSER)


@approve.handle()
async def set_approve():
    global enable
    enable = True
    await approve.send('picget is now enabled')


@forbid.handle()
async def set_forbid():
    global enable
    enable = False
    await forbid.send('picget is now disabled')


picture = on_command(cmd='picget', priority=10)


@picture.handle()
async def send_picture():
    global enable
    if enable:
        p = await get_picture()
        if not p:
            return False
        picture.block = True
        msg: Message = MessageSegment.text(p.__str__()) + MessageSegment.image(file=p.pic)
        await picture.finish(msg)
    else:
        msg: Message = Message(MessageSegment.text('request is denied'))
        await picture.finish(msg)
