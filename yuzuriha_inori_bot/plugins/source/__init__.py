from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

get_source = on_command(cmd='祈妹源码')

pluginNames = ['pixiv', 'source']  # 可用插件参数列表
listList = ['list', '插件']  # 用于查询插件参数的参数列表


@get_source.handle()
async def send_url(bot: Bot, event: Event):
    cmd = str(event.get_message()).strip()  # 首次发送命令时跟随的参数
    args = cmd.replace(cmd.split(' ', 1)[0], '').strip()
    if args == '':
        msg = 'https://github.com/DiscolorLeaf/Yuzuriha_Inori-Bot/tree/master'
    elif args in listList:
        msg = '插件列表:'
        for plugin in pluginNames:
            msg += '\n' + plugin
    elif args in pluginNames:
        msg = 'https://github.com/DiscolorLeaf/Yuzuriha_Inori-Bot/tree/master/yuzuriha_inori_bot/plugins/' + args
    else:
        msg = '参数错误'
    await get_source.finish(msg)
