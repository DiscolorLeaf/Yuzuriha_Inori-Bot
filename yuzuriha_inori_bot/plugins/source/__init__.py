import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment, Message

get_source = on_command(cmd='祈妹源码')

pluginNames = ['pixiv', 'source']  # 可用插件参数列表
listList = ['list', '插件']  # 用于查询插件参数的参数列表


@get_source.handle()
async def send_url(bot: Bot, event: Event):
    code = ''

    cmd = str(event.get_message()).strip()  # 首次发送命令时跟随的参数
    args = cmd.replace(cmd.split(' ', 1)[0], '').strip()
    args = args.split(' ', 1)

    if args[0] == '':
        data = 'https://github.com/DiscolorLeaf/Yuzuriha_Inori-Bot/tree/master'
    elif args[0] in listList:
        data = '插件列表:'
        for plugin in pluginNames:
            data += '\n' + plugin
    elif args[0] in pluginNames:
        data = 'https://github.com/DiscolorLeaf/Yuzuriha_Inori-Bot/tree/master/yuzuriha_inori_bot/plugins/' + args[0]
        if len(args) == 2:
            if args[1] == 'showcode':
                code = await get_page(args[0])
            else:
                data = '参数错误'
    else:
        data = '参数错误'

    msg: Message = MessageSegment.text(data + '\n') + MessageSegment.text(code)
    await get_source.finish(msg)


async def get_page(name):
    code = ''

    dir_base = 'yuzuriha_inori_bot/plugins/'+name
    for _, _, files in os.walk(dir_base):
        for file in files:
            file_base = dir_base + '/' + file
            data = open(file_base, 'r', encoding='UTF-8')
            code += '\n\n------------------------------------\n\n'
            code += 'FILENAME: ' + file + '\n\n'
            code += data.read()
        break

    return code
