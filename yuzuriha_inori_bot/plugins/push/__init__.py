from nonebot import require, get_bot, get_driver
from nonebot.adapters.onebot.v11 import MessageSegment, Message

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def push_notice(text,user_id):
    msg: Message = MessageSegment.text('Warning ') + MessageSegment.text(text)
    await get_bot().call_api('send_private_msg', **{'message': msg, 'user_id': user_id})
