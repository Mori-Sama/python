import time
from db import db_handler
def withdraw_interface(username,num):
    user_dict = db_handler.select(username)
    balance = float(user_dict['balance'])
    user_dict['balance'] = balance - num*1.05
    flow = f'用户{username}提现成功！手续费：[{num*0.05}$]-提现金额：[{num}$]-时间[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]'
    user_dict['flow'].append(flow)
    db_handler.save(user_dict)
    return 1,flow

def repay_interface(username,num):
    user_dict = db_handler.select(username)
    balance = float(user_dict['balance'])
    user_dict['balance'] = balance + num
    flow = f'用户{username}还款成功！还款金额：[{num}$]-时间[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]'
    user_dict['flow'].append(flow)
    db_handler.save(user_dict)
    return 1,flow

def transfer_interface(username,t_username,num):
    user_dict = db_handler.select(username)
    user_balance = float(user_dict['balance'])
    t_user_dict = db_handler.select(t_username)
    if t_user_dict:
        t_user_balance = float(t_user_dict['balance'])
        if user_balance >= num:
            user_dict['balance'] = user_balance - num
            t_user_dict['balance'] = t_user_balance + num
            flow = f'向{t_username}账户转账成功！转账金额：[{num}$]-时间[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]'
            t_flow = f'{username}账户向您转账，转账金额：[{num}$]-时间[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]'
            user_dict['flow'].append(flow)
            t_user_dict['flow'].append(t_flow)
            db_handler.save(user_dict)
            db_handler.save(t_user_dict)
            return 1,flow
        else:
            return 0,'当前账户余额不足'
    else:
        return 0,'目标账户不存在！'


def commodity_statement(username):
    user_dict = db_handler.select(username)
    lis = user_dict['shop_car']
    balance = user_dict['balance']
    commodity_value = 0
    for i in lis:
        commodity_value += lis[i][0]*lis[i][1]
        print(f'商品名[{i}]-数量[{lis[i][1]}]-价格[{lis[i][0]*lis[i][1]}]')
    print(f'总价格[{commodity_value}]')
    num = input('是否确认购买(输入y确认，n退出)').strip()
    if num == 'y':
        if balance >= commodity_value:
            user_dict['balance'] -= commodity_value
            user_dict['shop_car'] = {}
            db_handler.save(user_dict)
            return 1,'购买成功'
        else:return 0,'账户余额不足'
    else:return 0,'用户放弃购买'