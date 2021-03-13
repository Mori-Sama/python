from lib import common
from conf import settings
from bin import start
import os
import re
import logging.config

logging.config.dictConfig(settings.LOGGING_DIC)
log1 = logging.getLogger('user_log')


def login_auth(sock):
    def wrapper(f):
        def inner(*args, **kwargs):
            if settings.user_key:
                res = f(*args, **kwargs)
                return res
            else:
                login(sock)

        return inner

    return wrapper


def login(sock):
    username = input('请输入用户名：')
    password = input('请输入密码：')
    user_dict_ = {'username': username, 'password': password}
    common.msg_pack_send(user_dict_, sock)
    key_dict = common.msg_unpack_recv(sock)
    settings.user_key = key_dict['key']
    if not settings.user_key:
        print('用户名或密码错误')
        return 202
    else:
        print('登录成功')
        log1.info(f'{username}登录')
        return 102


@login_auth(start.sock)
def download(sock):
    max_index = common.show_file_list(common.msg_unpack_recv(sock)['file_list'])
    file_number = input('请输入文件序号：').strip()
    if file_number == 'q':
        print('退出下载')
        return 102
    file_number = int(file_number)
    # if file_number > max_index or file_number < 0:
    #     print('请输入正确的序号！')
    #     return 202
    user_dict_ = {'user_key': settings.user_key, 'file_number': file_number}
    common.msg_pack_send(user_dict_, sock)
    file_dict = common.msg_unpack_recv(sock)
    file_path = input('请输入存储路径：（不输入则使用默认路径）')
    if not file_path:
        file_path = os.path.join(settings.FILE_PATH, file_dict['filename'])
    else:
        file_path = os.path.join(file_path, file_dict['filename'])
    with open(file_path, mode='wb') as f:
        n = 0
        while n < file_dict['filesize']:
            msg = sock.recv(1024)
            f.write(msg)
            n += len(msg)
            print('\r', f'已下载{round(n / file_dict["filesize"], 2) * 100}%')
        print('下载完成！')
    log1.info(f'下载文件{file_dict["filename"]}到{file_path}')
    return 102


@login_auth(start.sock)
def upload(sock):
    file_path = input('请输入上传文件的完整路径：(默认上传至当前文件夹)')
    filesize = os.path.getsize(file_path)
    filename = file_path.split('\\')[-1]
    file_dict = {'user_key': settings.user_key, 'filename': filename, 'filesize': filesize}
    common.msg_pack_send(file_dict, sock)
    n = 0
    with open(file_path, mode='rb') as f:
        while 1:
            msg = f.read(1024)
            n += len(msg)
            if msg:
                sock.send(msg)
                print('\r', f'正在上传{round(n / filesize, 2) * 100}%')
            else:
                log1.info(f'上传文件{filename}')
                print('上传完成！')
                return 102


@login_auth(start.sock)
def switch(sock):
    common.show_file_list(common.msg_unpack_recv(sock)['file_list'])
    file_number = int(input('请输入文件夹名(序号)').strip())
    user_operation = {'file_number': file_number, 'user_key': settings.user_key}
    common.msg_pack_send(user_operation, sock)
    file_dict = common.msg_unpack_recv(sock)
    if file_dict['status']:
        common.show_file_list(file_dict['file_list'])
        return 102
    else:
        print('请输入正确的序号！')
        return 202


@login_auth(start.sock)
def create_dir(sock):
    dir_name = input('请输入文件夹名：')
    if dir_name == 'q':
        return 102
    dir_dict = {'user_key': settings.user_key, 'dir_name': dir_name}
    common.msg_pack_send(dir_dict, sock)
    status = common.msg_unpack_recv(sock)
    if status['status']:
        print('创建成功！')
        for i in status['file_list']:
            print(i)
        return 102
    else:
        print('创建失败！')
        return 202


def register(sock):
    username = input('请输入用户名：')
    if username == 'q':
        return 102
    password = input('请输入密码：')
    if len(password) < 8 or len(password) > 16:
        print('密码长度不符合规范！')
        return 301
    elif re.search('[~!@#$%^&*()_+=“‘《》<>?/\\-]', password):
        print('密码含有非法字符！')
        return 301
    re_password = input('请确认密码：')
    if re_password == password:
        user_dict = {'username': username, 'password': password}
        common.msg_pack_send(user_dict, sock)
        if common.msg_unpack_recv(sock)['status']:
            print('注册成功！')
            return 102
        else:
            print('用户名重复')
            return 301
    else:
        print('两次密码不一致！')
        return 301


operation_dict = {
    1: login,
    2: register,
    3: download,
    4: upload,
    5: switch,
    6: create_dir,
}
