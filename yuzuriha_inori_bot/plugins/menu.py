from nonebot import on_command
from nonebot.rule import to_me


menu = on_command("menu", rule=to_me(), aliases={"功能菜单", "功能查询"}, priority=5)

@menu.handle()
async def show_menu():
    result = "0.功能查询 指令：功能菜单/功能查询\n1.天气查询 指令：天气/天气预报\n2.发涩图 指令：涩涩\n"
    await menu.finish(result)