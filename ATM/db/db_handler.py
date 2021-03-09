# 数据处理层
import json
import os
from conf import settings

def select(username):
    user_path = os.path.join(
    settings.USER_DATA_PATH,f'{username}.json'
    )
    if os.path.exists(user_path):
        with open(user_path,mode='r',encoding='utf-8') as f:
            user_dict = json.loads(f.read())
        return user_dict


def save(user_dict):
    user_path = os.path.join(
    settings.USER_DATA_PATH,f'{user_dict["username"]}.json'
    )
    with open(user_path,mode='w',encoding='utf-8') as f:
        x = json.dumps(user_dict,ensure_ascii=False) # ensure_ascii的作用是修改展示模式，false表示不用二进制显示
        f.write(x)

def select_admin(username):
    admin_path = os.path.join(
        settings.ADMIN_DATA_PATH,f'{username}.json'
    )
    if os.path.exists(admin_path):
        with open(admin_path,mode='r',encoding='utf-8') as f:
            user_dict = json.loads(f.read())
        return user_dict
