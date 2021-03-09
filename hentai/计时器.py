from datetime import datetime
import time
import os
import pyautogui
import pyperclip
import win32gui
import win32con

system = datetime.now()


# 计算启动时间
def d_time(second, minute, hour, day=system.day, month=system.month, year=system.year):
    d_value = datetime(year, month, day, hour, minute, second) - datetime.now()
    return d_value.seconds


# 在规定时间打开设定文件
def copen(stime_value, path):
    time.sleep(stime_value)
    try:
        os.startfile(path)
        return 1
    except Exception:
        print("输入路径有误")
        return 0


def run_time(new_time_len, path, new_time):
    if new_time_len == 3:
        second, minute, hour = new_time
        s_time_value = d_time(int(second), int(minute), int(hour))
    elif new_time_len == 4:
        second, minute, hour, day = new_time
        s_time_value = d_time(int(second), int(minute), int(hour), int(day))
    elif new_time_len == 5:
        second, minute, hour, day, month = new_time
        s_time_value = d_time(int(second), int(minute), int(hour), int(day), int(month))
    elif new_time_len == 6:
        second, minute, hour, day, month, year = new_time
        s_time_value = d_time(int(second), int(minute), int(hour), int(day), int(month), int(year))
    else:
        print("输入有误，请重新输入")
        return 0
    return copen(s_time_value, path)


def get_time():
    while 1:
        print('请输入启动项目的绝对路径')
        path = input()
        # 顺序 秒 分 时 日 月 年，后三个默认今天的年月日
        # 格式：00 00 10
        print('请输入设定的时间：')
        new_time = input().split(' ')
        new_time_len = len(new_time)
        num = run_time(new_time_len, path, new_time)
        if num == 1:
            break
        else:
            continue


# 获取窗口并显示在屏幕最上层
def show_window(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    # 获取窗口左上坐标并以元组的形式返回
    left, top, *_ = win32gui.GetWindowRect(hwnd)
    return left, top


# 对窗口进行操作
def operation(args, group_name):
    left, top = args
    x = left + 150
    y = top + 160
    pyautogui.click(x, y)
    # 将内容发送到剪贴板
    pyperclip.copy(group_name)
    pyautogui.hotkey('ctrl', 'v')
    y1 = y + 100
    time.sleep(2)
    pyautogui.click(x=x, y=y1, clicks=2, interval=0.25)


# 发送内容
def send_msg(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')


def run():
    print('请输入对象名称')
    group_name = input()
    print('请输入发送消息')
    msg = input()
    get_time()
    operation(show_window('QQ'), group_name)
    send_msg(msg)


if __name__ == '__main__':
    run()