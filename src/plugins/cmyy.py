from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import Arg, CommandArg, ArgPlainText


data_path = 'src/data/cmyy.txt'


cmyy = on_command('cmyy', rule=to_me(), aliases={'柴米油盐', '柴米', '小柴'}, priority=5)
index = 0

@cmyy.got('order', prompt='这里是小柴!请问有什么可以帮您的?\n0.显示物品清单\n1.添加物品\n2.修改物品数量\n3.删除物品\n')
async def do_order(choice: str = ArgPlainText('order')):
    # 0.显示物品清单
    if index == 0:
        pass
    if choice == '0':
        await display_list()
        result = ''

    # 1.添加物品
    elif choice == '1':
        await cmyy.send('要添加的物品为')
        target = await got_message()
        await cmyy.send('添加物品的数量为')
        times = await got_message()
        object_list = open(data_path, 'a', encoding='utf-8')
        object_list.write('{} {}\n'.format(target, times))
        await display_list()
        result = '添加成功!'

    # 2.修改物品数量
    elif choice == '2':
        await cmyy.send('要修改的物品为')
        target = await got_message()
        f = open(data_path, 'r', encoding='utf-8')
        object_list = f.readlines()
        f = open(data_path, 'w', encoding='utf-8')
        result = '修改失败，物品不存在'
        for i in object_list:
            i = i[0:-1]
            if target == i.split()[0]:
                await cmyy.send('要改成多少？')
                change = await got_message()
                i = i.split()[0] + ' ' + change
                result = '物品数量修改成功'
            f.write('{}\n'.format(i))
        await display_list()


    # 3.删除物品
    elif choice == '3':
        await cmyy.send('要删除的物品为')
        target = await got_message()
        f = open(data_path, 'r', encoding='utf-8')
        object_list = f.readlines()
        f = open(data_path, 'w', encoding='utf-8')
        result = '删除失败，物品不存在'
        for i in object_list:
            i = i[0:-1]
            if target == i.split()[0]:
                result = '删除成功'
                continue
            f.write('{}\n'.format(i))
        await display_list()

    # 非特定输入
    else:
        result = '输入错误,请重试'

    await cmyy.finish(result)

# @cmyy.got('message')
async def got_message(reply: str = ArgPlainText('message'))-> str:
    # 返回用户输入
    return reply

# 显示物品清单
async def display_list():
    object_list = open(data_path, 'r', encoding='utf-8')
    object_list = object_list.readlines()
    sum = ''
    for i in object_list:
        sum = sum + i
    await cmyy.send(sum)