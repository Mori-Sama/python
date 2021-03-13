import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import socketserver
from lib import common
from db import databases
import datetime
import os
from conf import settings


class MyRequestHandle(socketserver.BaseRequestHandler):

    def __init__(self,*args,**kwargs):
        # 用来判断用户是否为正常登录
        self.key = '别看了'
        # 当前用户所处的文件夹位置
        self.current = settings.DIR_PATH
        # self.current = r'C:\Users\Zhao\Desktop\python'
        # 每个用户拥有的文件夹，格式为用户名加上默认路径（未实现）
        # self.user_dir = settings.DIR_PATH
        # 继承父类必须放在下面，不然很可能会出现调用不到自定义属性的错误
        super().__init__(*args, **kwargs)

    def handle(self):
        conn = self.request
        operation_dict = {
            1: 'login',
            2: 'register',
            3: 'download',
            4: 'upload',
            5: 'switch',
            6: 'create_dir',
        }
        while 1:
            sync_dict = common.msg_unpack_recv(conn)
            sync = sync_dict['sync']
            if sync == 0:
                break
            getattr(self,f'{operation_dict[sync]}')()


    def login(self):
        print(self.key)
        print(self.current)
        user_dict = common.msg_unpack_recv(self.request)
        password = common.ency(user_dict['password'])
        flag = databases.select(user_dict['username'])
        if flag:
            if flag['password'] == password:
                self.key = common.ency(f'{datetime.datetime.now()}')
                return common.msg_pack_send({'key':self.key},self.request)
            else:return common.msg_pack_send({'key':0},self.request)
        else:return common.msg_pack_send({'key':0},self.request)

    def download(self):
        current_dir, file_list = common.show_dir_list(settings.DIR_PATH)
        self.current = current_dir
        file_dict = {'file_list':file_list}
        common.msg_pack_send(file_dict,self.request)
        file_msg = common.msg_unpack_recv(self.request)
        if self.key == file_msg['user_key']:
            filename = file_list[file_msg['file_number']]
            path = os.path.join(current_dir,filename)
            file_dict = {'filename':filename,'filesize':os.path.getsize(path)}
            common.msg_pack_send(file_dict,self.request)
            with open(path,mode='rb') as f:
                while 1:
                    msg = f.read(1024)
                    if msg:
                        self.request.send(msg)
                    else:
                        break
        else:
            return 505

    def upload(self):
        file_dict = common.msg_unpack_recv(self.request)
        path = os.path.join(self.current, file_dict['filename'])
        filesize = file_dict['filesize']
        n = 0
        with open(path,mode='wb') as f:
            while n < filesize:
                msg = self.request.recv(1024)
                f.write(msg)
                n += len(msg)

    def switch(self):
        current_dir, file_list = common.show_dir_list(self.current)
        file_dict = {'file_list':file_list}
        common.msg_pack_send(file_dict, self.request)
        file_dict = common.msg_unpack_recv(self.request)
        if file_dict['user_key'] == self.key:
            dirname = file_list[file_dict['file_number']]
            if os.path.isdir(os.path.join(self.current,dirname)):
                self.current = os.path.join(self.current,dirname)
                _,file_list = common.show_dir_list(self.current)
                dir_dict = {'status':1,'file_list':file_list}
                common.msg_pack_send(dir_dict,self.request)
            else:common.msg_pack_send({'status':0},self.request)
        else:return 505

    def create_dir(self):
        dir_dict = common.msg_unpack_recv(self.request)
        current_dir, file_list = common.show_dir_list(self.current)
        if self.key == dir_dict['user_key']:
            if dir_dict['dirname'] not in file_list:
                os.mkdir(os.path.join(self.current,dir_dict['dirname']))
                common.msg_pack_send({'status':1,'file_list':file_list},self.request)
            else:common.msg_pack_send({'status':0},self.request)
        else:common.msg_pack_send({'status':0},self.request)

    def register(self):
        user_dict = common.msg_unpack_recv(self.request)
        username = user_dict['username']
        if databases.select(username):
            common.msg_pack_send({'status':0},self.request)
        else:
            password = common.ency(user_dict['password'])
            databases.create(username,password)
            common.msg_pack_send({'status':1},self.request)


s = socketserver.ThreadingTCPServer(('127.0.0.1',9000),MyRequestHandle)
s.serve_forever()