import os
from db import db_handler
from conf import settings
import json

def show_kind():
    res = os.listdir(settings.COMMODITY_DATA_PAYH)
    n = 0
    for i in res:
        name,_ = i.split('.')
        print(f'序号[{n}]-名称[{name}]')
        n += 1
    return res

def show_list(kind):
    res = os.listdir(settings.COMMODITY_DATA_PAYH)
    lis = res[kind]
    list_path = os.path.join(settings.COMMODITY_DATA_PAYH,lis)
    n = 0
    with open(list_path,mode='r',encoding='utf-8') as f:
        commodities = json.loads(f.read())
    for i in commodities:
        name,price = i
        print(f'序号[{n}]-名称[{name}]-价格[{price}]')
        n += 1
    return commodities


def add_commodity_car(username,shopping_car):
    user_dict = db_handler.select(username)
    car_dic = user_dict['shop_car']
    for i in shopping_car:
        item,price = i
        car_dic.setdefault(item, [price,0])[1] = car_dic.setdefault(item, [price,0])[1] + 1
    db_handler.save(user_dict)
    return 1

