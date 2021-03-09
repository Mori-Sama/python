import re
from core import src
import logging
import hashlib
from conf import settings
def get_pwd_md5(password):
    m = hashlib.md5('zhaoxulu'.encode('utf-8'))
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    return password

def login_auth(func):
    def inner(*args,**kwargs):
        if src.login_user:
            res = func(*args,**kwargs)
            return res
        else:
            print('请先登录')
            src.login()
    return inner
def get_logger(log_type):
    pass
