# 程序入口
import sys
import os
# 添加解释器的环境变量，如果是用bin目录存放启动文件start则需要在套一层os.path.dirname()
sys.path.append(os.path.dirname(__file__))
from core import src


# 开是执行项目函数
if __name__ == "__main__":
    # 先执行用户视图层
    src.run()