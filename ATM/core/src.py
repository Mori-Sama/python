'''
用户视图层
'''
import re
import hashlib
import json
import os
from interface import user_interface,bank_interface,shop_interface
from lib import common

login_user = 0

# 注册
def register():
    while 1:
        username = input('请输入用户名：\n>>>')
        if username.upper() == 'Q':
            break 
        password = input('请输入密码：\n>>>')
        re_password = input('请确认密码输入：\n>>>')
        if re.search('\d',password) and re.search('[a-zA-Z]',password):
            if re_password == password:
                num,msg = user_interface.register_interface(username,password)
                if num:
                    print(msg)
                    break
                else:print(msg)
        else:
            print('密码必须由数字字母组成')

# 登录
def login():
    while 1:
        username = input('请输入用户名：\n>>>')
        password = input('请输入密码：\n>>>')
        num,msg = user_interface.login_interface(username,password)
        if num:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)
            break

# 查看余额
@common.login_auth
def check_balance():
    balance = user_interface.check_bal_interface(login_user)
    print(f'用户{login_user}的余额为：{balance}')

# 提现
@common.login_auth
def withdraw():
    while 1:
        balance = user_interface.check_bal_interface(login_user)
        num_money = input('请输入金额：\n>>>').strip()
        if num_money.isdigit():
            num_money = float(num_money)
            if 100 < num_money < balance:
                _,msg = bank_interface.withdraw_interface(login_user,num_money)
                print(msg)
                break
            else:
                print('您输入的金额过小或余额不足')
                continue

# 还款
@common.login_auth
def repay():
    while 1:
        re_num = input('请输入金额：\n>>>').strip()
        if re_num.isdigit():
            re_num = float(re_num)
            if re_num > 0:
                _,msg = bank_interface.repay_interface(login_user,re_num)
                print(msg)
                break
            else:print('请输入正确的数字！')
        else:
            print('请输入数字')

# 转账
@common.login_auth
def transfer():
    t_username = input('请输入转账账户：\n>>>').strip()
    num = input('请输入转账金额：\n>>>').strip()
    if num.isdigit():
        num = float(num)
        flag,msg = bank_interface.transfer_interface(login_user,t_username,num)
        if flag:print(msg)
        else:print(msg)
    else:print('请输入数字！')

# 查看流水
@common.login_auth
def check_flow():
    flow = user_interface.check_flow_interface(login_user)
    for i in flow:
        print(i)

@common.login_auth
def shopping():
    while 1:
        shopping_car = []
        res = shop_interface.show_kind()
        kind = input('请输入您要查看的商品目录号：\n>>>').strip()
        while 1:
            if kind.isdigit():
                kind = int(kind)
                if kind in range(len(res)):
                    lis = shop_interface.show_list(kind)
                    num = input('请输入您要购买的商品序号(多次输入请以空格隔开,多次购买请重复输入)').strip().split(' ')
                    for i in num:
                        if i.isdigit():
                            i = int(i)
                            if i in range(len(lis)):
                                shopping_car.append(lis[i])
                                choice = input('输入y将当前产品加入购物车，输入n退出')
                                if choice == 'y':
                                    shop_interface.add_commodity_car(login_user,shopping_car)
                                    break
                                else:break
                            else:
                                shopping_car = []
                                print('请输入有效序号')
                                break
                        else:
                            print('请输入数字')
                            break
                else:print('请输入有效的序号')
            else:print('请输入数字')



@common.login_auth
def check_shop_car():
    flag,msg = bank_interface.commodity_statement(login_user)
    if flag:print(msg)
    else:print(msg)

def admin():
    username = input('请输入管理员账户：\n>>>')
    password = input('请输入管理员密码：\n>>>')
    flag,msg = user_interface.admin_interface(username,password)
    if flag:
        while 1:
            print('1、添加账户\n2、修改账户额度\n3、冻结账号\n4、注销')
            num = input('请输入操作序号：\n>>>').strip()
            if num == '1':register()
            elif num == '2':
                while 1:
                    user = input('请输入账户名称：\n>>>')
                    num_money = input('请输入额度：\n>>>').strip()
                    if num_money.isdigit():
                        num_money = float(num_money)
                        flag,msg = user_interface.admin_change_interface(user,num_money)
                        if flag:
                            print(msg)
                            break
                        else:print(msg)
                    else:print('请输入数字')
            elif num == '3':
                while 1:
                    user = input('请输入账户名称：\n>>>')
                    num = input('请输入操作：\n冻结请输入1\n解冻请输入0\n>>>').strip()
                    if num.isdigit():
                        flag,msg = user_interface.admin_lock_interface(user,num)
                        if flag:
                            print(msg) 
                            break
                        else:print(msg)
            elif num == '4':break
            else:print('请输入正确的序号')

func_dict = {
    '1':register,
    '2':login,
    '3':check_balance,
    '4':withdraw,
    '5':repay,
    '6':transfer,
    '7':check_flow,
    '8':shopping,
    '9':check_shop_car,
    '10':admin,
}

# 视图层主程序
def run():
    while 1:
        print('''
     ------ATM SYSTEM-------
            1、注册
            2、登录
            3、查看余额
            4、提现
            5、还款
            6、转账
            7、查询流水
            8、购物
            9、查看购物车
            10、管理员登入
        ''')
        choice = input('请输入功能编号：\n>>>').strip()
        if choice not in func_dict:
            print('请输入正确的功能编号')
            continue
        func_dict[choice]()
    pass