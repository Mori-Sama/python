# pymysql模块

~~~python
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '1181801087',
    database = 'zhaoxulu',
    charset = 'utf8' # 编码，不要加杠
) # 链接数据库

cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) # 产生一个游标对象(用来执行命令的)
# cursor=pymysql.cursors.DictCursor设置查询结果以字典的形式返回
sql = 'show tables;' # sql 语句
res = cursor.execute(sql) # 返回的是你当前sql语句影响的行数

# 获取数据类似文件光标移动，读取都是相对当前光标位置移动
cursor.fetchall() # 返回所有数据
cursor.fetchone() # 返回一条数据
# cursor.fetchmany(n)  返回n条数据
cursor.scroll(1,'relative') # 相对游标所在位置继续往后移动一位
cursor.scroll(1,'absolute') # 相对游标起始位置继续往后移动一位

# 防止sql注入问题
# 不要手动拼接数据，先用%s占位，之后将需要拼接的数据直接交给execute方法即可
username = input()
password = input()
sql = "select * from user where name=%s and password=%s;"
cursor.execute(sql,(username,password))

# 操作完成后断开连接，关闭游标
cursor.close()
conn.close()
~~~

~~~python
# 增删改数据的时候，需要二次确认
sql = 'insert into user(name,password) value(%s,%s)'
rows = cursor.execute(sql,('zhao',123))
# 操作多条数据
rows = cursor.executemany(sql,[('zhao',123),('xu',123),('lu',123)])
conn.commit() # 确认输入
~~~

## 开启事务

~~~python

~~~

