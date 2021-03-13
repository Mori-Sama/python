import os
# 存储登录状态码
user_key = 0

# 文件下载默认路径
FILE_PATH = r'C:\Users\Zhao\Desktop\c和c++'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOG_PATH = os.path.join(BASE_DIR, 'log', 'access.log')


standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'


logfile_dir = os.path.dirname(os.path.abspath(__file__))
logfile_name = 'all2.log'
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

logfile_path = os.path.join(logfile_dir, logfile_name)

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
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
    'filters': {},
    'handlers': {
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logfile_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'encoding': 'utf-8',
        },

    },
    'loggers': {
        'user_log': {
            'handlers': ['stream', 'access'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

