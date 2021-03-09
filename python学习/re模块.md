# re模块

~~~python
ret = re.findall(正则,待匹配的字符串)
# 返回一个列表，列表中是所有满足条件的元素

ret = re.search(正则,带匹配的字符串)
# 返回一个对象，对象中包含的是第一个满足条件的对象
if ret: # 如果不为空
	ret.group() # 取出匹配到的值

# 当某一个正则表达式被多次使用的时候，可以用compile
ret = re.compile(正则)
# finditer返回的是一个迭代器，匹配到的元素以对象的形式存储
res = ret.finditer(字符串)
~~~

## 分组

~~~python
# findall总时只显示括号内匹配到的内容，但匹配时按照的是完整的正则匹配的
# 取所有符合条件的，优先显示分组内的
# 取消分组优先显示 (?:)


# search可以通过给group(n)传参的方式取到别的分组内的内容，n从1开始，从左往右，0是表示显示所有


# 分组命名
(?P=<name>) # name就是该组的名字
res = ret.group('name') # 取值
~~~

