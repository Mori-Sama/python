# python的一些数据结构



## 列表

~~~python

~~~





## 字典

~~~python
# 字典是另一种可变容器模型，且可存储任意类型对象。
# 字典的每个键值 key=>value 对用冒号 : 分割，每个对之间用逗号(,)分割，整个字典包括在花括号 {} 中 ,格式如下所示：

d = {key1 : value1, key2 : value2, key3 : value3 }

# 字典的键必须是不可变数据类型，并且唯一
# 在python3.5版本之前是无序的，在3.7之后都是有序的
# 字典的查询速度非常快，存储关联性强，是用空间换取时间
~~~

~~~python
# 字典创建的几种方式

# 1.创建空字典
>>> dic = {}
>>> type(dic)
<type 'dict'>

# 2.直接赋值创建
>>> dic = {'spam':1, 'egg':2, 'bar':3}
>>> dic
{'bar': 3, 'egg': 2, 'spam': 1}

# 3.通过关键字dict和关键字参数创建
>>> dic = dict(spam = 1, egg = 2, bar =3)
>>> dic
{'bar': 3, 'egg': 2, 'spam': 1}

# 4.通过二元组列表创建
>>> list = [('spam', 1), ('egg', 2), ('bar', 3)]
>>> dic = dict(list)
>>> dic
{'bar': 3, 'egg': 2, 'spam': 1}

# 5.dict和zip结合创建
>>> dic = dict(zip('abc', [1, 2, 3]))
>>> dic
{'a': 1, 'c': 3, 'b': 2}

# 6.通过字典推导式创建
>>> dic = {i:2*i for i in range(3)}
>>> dic
{0: 0, 1: 2, 2: 4}

# 7.通过dict.fromkeys()创建
通常用来初始化字典, 设置value的默认值
>>> dic = dict.fromkeys(range(3), 'x')
>>> dic
{0: 'x', 1: 'x', 2: 'x'}

# 8.其他
>>> list = ['x', 1, 'y', 2, 'z', 3]
>>> dic = dict(zip(list[::2], list[1::2]))
>>> dic
{'y': 2, 'x': 1, 'z': 3}
~~~

~~~python
# 字典的操作

dic = {'name':'zhaoxulu','age':18}

dic['sex'] = '男' # 无则创建
dic['age'] = 21 # 有则修改

con = dic.setdefault('age', 45) # 无则创建，有则不变并且返回这个键的值

con = dic.pop('age', '没有此键') # 删除这个键，并且返回这个键的值，如果没有这个键则会返回第二个参数对应的内容（非必须）

dic.clear() # 清空字典的所有内容

con = dic.get('age', '无') # 有则返回值，无则返回第二个参数对应的值（无则返回None）

con = list(dic.keys()) # 返回所有的key值，其数据类型是一个特殊的数据类型，可以转化其类型在进行操作

con = list(dic.values()) # 返回所有的value值

con = list(dic.items()) # 返回所有的key和value，对应的用元组包含

dic.update(hobby='运动',hight=175) # 增加新键值对，如果存在则修改
dic.update([(1,'a'),(2,'b')])
dic.update(dict)

dic.fromkeys('abc',100) # 第一个参数是一个可迭代对象，第二个参数是共用的值
dic.fromkeys([1,2,3],[]) # 值是共用的，对于可变类型，一个变，全部变
dic[1].append(666) # 所有的值都会追加一个666

~~~





## 集合

~~~python
# 集合（set）是一个无序的不重复元素序列。

# 可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。

# 集合内的元素是不可变的，但是集合本身是可变的，集合是无序的

# 集合的主要作用是去重

~~~



## 元组

~~~python
# 元组中只包含一个元素时，需要在元素后面添加逗号，否则括号会被当作运算符使用：
>>> tup1 = (50)
>>> type(tup1)     # 不加逗号，类型为整型
<class 'int'>

>>> tup1 = (50,)
>>> type(tup1)     # 加上逗号，类型为元组
<class 'tuple'>
~~~

