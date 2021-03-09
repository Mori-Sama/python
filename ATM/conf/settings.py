import os
BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)
USER_DATA_PATH = os.path.join(
    BASE_PATH,'db','user_data'
)
ADMIN_DATA_PATH = os.path.join(
    BASE_PATH,'db','admin_data'
)
COMMODITY_DATA_PAYH = os.path.join(
    BASE_PATH,'db','commodity_data'
)


import logging.config   #不能只导入logging

BASE_DIR=os.path.dirname(os.path.dirname(__file__))
# DB_PATH=os.path.join(BASE_DIR,'db')
# DB_PATH=r'%s\db' %BASE_DIR

# 定义日志文件的路径
LOG_PATH=os.path.join(BASE_DIR,'log','access.log')
# LOG_PATH=r'%s\log\access.log' %BASE_DIR
# BOSS_LOG_PATH=r'%s\log\boss.log' %BASE_DIR

# 自定义三种日志输出格式———————————————————————————————————————————————————————————————
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
# 自定义日志输出格式————————————————————————————————————————————————————————————————————

logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
logfile_name = 'all2.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    # 禁用已经存在的logger实例
    'disable_existing_loggers': False, 
    # 定义日志 格式化的 工具
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'id_simple': {
            'format': id_simple_format
        },
    },
    # 过滤
    'filters': {},  # jango此处不同
    'handlers': {
        #打印到终端的日志
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，轮转保存
            'formatter': 'standard',
            'filename': logfile_path, # 日志文件路径
            'maxBytes': 1024*1024*5,  # 一份日志大小5M
            'backupCount': 5, # 最多保存多少份
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
 
    },
    # logger实例
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['stream', 'access'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        # logging.getLogger(__name__)拿到的logger配置       
        # 这样我们再取logger对象时logging.getLogger(__name__)，不同的文件__name__不同，这保证了打印日志时标识信息不同，
        # 但是拿着该名字去loggers里找key名时却发现找不到，于是默认使用key=''的配置
    },
}






if __name__ == "__main__":
    print(USER_DATA_PATH)
    print(ADMIN_DATA_PATH)