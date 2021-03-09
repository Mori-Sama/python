# hash

**特点：**
1.只要传入的内容一样，得到的hash值必然一样
2.不能由hash值反解加密内容，不可逆
3.只要使用的hash算法不变，无论加密的内容有多大，得到的hash值的长度是固定的

**用途：**
1.加密传输
2.数据校验

~~~python
# 以md5算法为例子
import hashlib
m = hashlib.md5() # 实例化一个加密对象
m.update('hello'.encode('utf-8')) # update表示输入加密数据，只能加入二进制数据
m.update('world'.encode('utf-8'))
res = m.hexdigest() # hexdigest表示得到在这步之前的所有update输入数据的加密数据
print(res)

m1 = hashlib.md5()
m1.update('hel'.encode('utf-8'))
m1.update('lo'.encode('utf-8'))
m1.update('wor'.encode('utf-8'))
m1.update('ld'.encode('utf-8'))
res1 = m1.hexdigest()
print(res1)
# res和res1的加密数据完全一样

# 加盐
m2.hashlib.md5('盐'.encode('utf-8')) # 加盐
~~~



