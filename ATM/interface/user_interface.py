import os
from db import db_handler
from lib import common
import hashlib

def register_interface(username,password,balance=15000):
    dic = db_handler.select(username)
    if dic:
        return 0,'用户名已存在！'
    else:
        password = common.get_pwd_md5(password)
        user_dict = {
            'username':username,
            'password':password,
            'balance':balance,
            'flow':[],
            'shop_car':{},
            'locked':0
        }
        db_handler.save(user_dict)
        return 1,'注册成功！'

def login_interface(username,password):
    password = common.get_pwd_md5(password)
    user_dict = db_handler.select(username)
    if user_dict:
        if user_dict['locked'] == '0':
            if user_dict['password'] == password:
                return 1,'欢迎来访！'
            else:return 0,'密码错误！'
        else:return 0,'该账户已经冻结'
    else:return 0,'用户名不存在'

def check_bal_interface(username):
    dic = db_handler.select(username)
    return dic['balance']
    
def check_flow_interface(username):
    user_dict = db_handler.select(username)
    return user_dict['flow']

def admin_interface(username,password):
    user_dict = db_handler.select_admin(username)
    if user_dict:
        if username == user_dict['username'] and password == user_dict['password']:
            return 1,'管理员账户登录'
        else:return 0,'密码错误'
    else:return 0,'管理员不存在'

def admin_change_interface(username,num):
    user_dict = db_handler.select(username)
    if user_dict:
        user_dict['balance'] = num
        db_handler.save(user_dict)
        return 1,'修改额度成功'
    else:return 0,'该账户不存在'

def admin_lock_interface(username,num):
    user_dict = db_handler.select(username)
    if user_dict:
        user_dict['locked'] = num
        db_handler.save(user_dict)
        return 1,'操作成功'
    else:return 0,'该账户不存在'