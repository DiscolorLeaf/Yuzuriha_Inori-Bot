from nonebot import on_command, CommandSession
import requests
import json
import jsonpath


@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    city = session.current_arg_text.strip()
    if not city:
        city = (await session.aget(prompt='你想查询哪个城市的天气呢？')).strip()
        while not city:
            city = (await session.aget(prompt='要查询的城市名称不能为空呢，请重新输入')).strip()
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)


async def get_weather_of_city(city: str) -> str:
    cityweather = await get_weather(city)
    data = f'{cityweather[0]}\n{city}的天气是\n{cityweather[1]} {cityweather[2]}°C\n湿度{cityweather[3]}%\n{cityweather[4]} 风力{cityweather[5]}级'
    return data


async def get_weather(cityname):
    citycode = await get_citycode(cityname)
    #citycode = str(101230201)
    r = requests.get(
        f'https://devapi.qweather.com/v7/weather/now?location={citycode}&key=')
    r.encoding = 'utf-8'
    return r.json()['updateTime'], r.json()['now']['text'], r.json()['now']['temp'], r.json()['now']['humidity'], \
           r.json()['now']['windDir'], r.json()['now']['windScale']


async def get_citycode(cityname):
    citys = open('plugins/weather/city.json', 'r', encoding='UTF-8')
    citys = json.load(citys)
    citycode = jsonpath.jsonpath(citys, f'$..市[?(@.cityname == "{cityname}")].citycode]')[0]
    return citycode

