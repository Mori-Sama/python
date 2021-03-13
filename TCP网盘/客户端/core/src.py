from interface import user_interface as U
from lib import common
from bin import start
from conf import settings

def show_menu():
    print("""请输入对应的操作序号
    1.登录
    2.注册
    3.下载
    4.上传
    5.切换文件夹
    6.创建文件夹
    0.退出
    """)


def status_code(status,x,n=0):
    # 1**:成功执行信息
    if status == 102:
        pass
    # 2**:重新执行当前函数
    elif status == 202:
        n = 1
        while 1:
            status = U.operation_dict[x](start.sock)
            n += 1
            if status == 102:break
            if n == 3:
                print('你是蠢吗？？？？')
                break
    # 3**:循环，直到用户退出
    elif status == 301:
        while 1:
            status = U.operation_dict[x](start.sock)
            if status == 102:break


def run():
    while 1:
        show_menu()
        x = input('>>>').strip()
        if x == '0':
            break
        if x.isdigit() and len(x) == 1:
            x = int(x)
            if settings.user_key:
                common.send_sync(start.sock, x)
                status = U.operation_dict[x](start.sock)
                status_code(status, x)
            else:
                common.send_sync(start.sock, 1)
                status = U.operation_dict[x](start.sock)
                status_code(status, x)





