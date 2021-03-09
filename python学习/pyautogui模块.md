# pyautogui模块



### 鼠标控制功能

~~~python
import pyautogui
# 返回屏幕分辨率，元组
pyautogui.size()
# 返回鼠标此时的坐标，元组
pyautogui.position()
# 检测某个坐标是否在屏幕上，返回bool值
pyautogui.onScreen(0, 0)
# 鼠标移动，2s后移动到指定坐标，如果坐标参数为None则表示当前位置，（如果持续时间小于pyautogui.MINIMUM_DURATION该运动将是即时的。默认pyautogui.MINIMUM_DURATION值为0.1。）
pyautogui.moveTo(100, 200, 2)
# 鼠标相对当前位置移动
pyautogui.move(0,50)
# 鼠标拖拽，也有dragTo和drag参数，类似move，button参数表示按住鼠标左/右键不放
pyautogui.dragTo(100, 200, button='left/right')
'''
在鼠标拖拽和鼠标移动函数中还可以传入第四个参数
pyautogui.easeInQuad：使鼠标开始缓慢移动，然后加快，总时间不变
pyautogui.easeOutQuad：开始快速移动，然后减慢
pyautogui.easeInOutQuad：开始和结束快，中间移动慢
pyautogui.easeInBounce：来回弹射
pyautogui.easeInElastic：弹弓模式
...
'''
# 鼠标点击
pyautogui.click()
# 鼠标移动后点击
pyautogui.click(x=100, y=100, button='right')
# 鼠标连续多次点击:clicks点击次数，interval间隔时间
pyautogui.click(clicks=2, interval=0.25, button='right')
# 双击快捷方式：参数有x，y，interval，button
pyautogui.doubleClick()
# 按下鼠标释放鼠标：参数x，y，button
pyautogui.mouseUp(x=100, y=100)  # 移动到(100,200)然后释放鼠标
pyautogui.mouseDown()
# 鼠标滚动：参数为正向上滚动，为负向下滚动
pyautogui.scroll()

~~~





