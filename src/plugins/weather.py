from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import requests
import json


data_path = "src/data/city.json"
weather = on_command("weather", rule=to_me(), aliases={"天气", "天气预报"}, priority=5)


# @weather.handle()
# async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
#     plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
#     if plain_text:
#         matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值

# city: Message = Arg(),
@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(city_name: str = ArgPlainText("city")):
    city_weather = await get_weather(city_name)
    await weather.finish(city_weather)


# 在这里编写获取天气信息的函数
async def get_weather(city: str) -> str:
    # 这里简单返回一个字符串

    ''' 读取城市代码 '''
    file = open(data_path, 'r', encoding='utf-8')
    city_code_list = json.load(file)
    city_code_list = city_code_list['城市代码']

    ''' 目标城市 '''
    target = city
    for i in city_code_list:
        # print(type(i))
        city_list = i['市']  # i 为字典，返回值为列表
        for j in city_list:  # city为列表，成员 j 为字典
            name = j['市名']
            if target == name:  # 找到了
                target = j['编码']

    ''' API查询 '''
    url = 'https://devapi.qweather.com/v7/weather/now?'
    city_code = 'location={}'.format(target)
    api_key = '&key=bcd8d58195b140048c70440b6d00f113'
    API = url + city_code + api_key

    data = requests.get(API)
    data.encoding = 'utf-8'
    data = json.loads(data.text)
    data = data['now']
    # print(f"{target}温度为{data['temp']}℃, 天气:{data['text']}, 风向:{data['windDir']}")
    return f"{city}温度{data['temp']}℃, 天气{data['text']}, 风向{data['windDir']}"