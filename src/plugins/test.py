from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText


test = on_command("test", rule=to_me(), aliases={"测试"}, priority=5)

@test.got("Input", prompt="你想查询哪个城市的天气呢？")
async def handle_Input(Input: Message = Arg(), Input_name: str = ArgPlainText("Input")):
    if Input_name not in ["北京", "上海"]:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
        # await test.reject(Input.template("你想查询的城市 {city} 暂不支持，请重新输入！"))
        await test.reject("你想查询的城市 {city} 暂不支持，请重新输入！")
    await test.finish("通过")