# MySQL

~~~python
# mysql中的sql语句是以分号 ; 结尾，来表示一段命令的结尾
# 查看所有的库名 show databases;
# \c 取消命令
# 退出客户端exit或者quit，退出命令可以不加分号
# 修改当前用户的密码 update mysql.user set password=password(新密码) where user='root' and host='localhost'
# 连接数据库：mysql -h ip -P 端口号 -u用户名 -p
# 配置文件如果要自定义，需要在mysql根目录下新建一个my.ini的文件，在这个新建的文件里面自定义
# mysql5.5版本之后的存储引擎为innodb，5.5版本之前的是myisam
~~~

## 基本的SQL语句

### 针对库（文件夹）的增删改查

~~~sql
# 增
create database 库名;
# 指定字符编码
create database 库名 charset='gbk';

# 查
# 查看全部库
show databases;
# 查看单个库
show create database 库名;

# 改
# 修改字符编码
alter database 库名 charset='utf8';

# 删
drop database 库名;
~~~

## 针对表（文件）的增删改查

~~~python
'''在使用表时，首先要使用库'''
# 查看当前所在的库
select database();
# 切换库
use 库名;

# 增
create table 表名(id int,name char(4));
create table 表名(
    字段名1 类型(宽度) 约束条件,
    字段名2 类型(宽度) 约束条件,
    字段名3 类型(宽度) 约束条件
);
# 同一张表中字段名不能重复，宽度和约束条件是可选的，约束条件可以写多个，最后一行不能有逗号

# 查
# 查看当前库下所有表名
show tables;
# 查单个表
show create table 表名;
describe 表名; (简写：desc 表名;)

# 改
alter table 表名 modify name char(16);

# 删
drop table 表名;
~~~

## 针对数据的增删改查

~~~sql
# 增
insert into 表名 values(数据),(数据2);
insert into 表名(字段名，字段名1) values(数据，数据1)

# 查
# 查看表下的所有数据
select * from 表名;  # 当数据量特别大的时候不建议使用
# 指定字段查
select 字段名 from 表名;

# 改
update 表名 set 字段名=值 where 条件;

# 删
delete from 表名 where 条件;
# 清空表中所有数据
delete from 表名;  # 在删除表中数据的时候，主键的自增不会停止
truncate 表名;  # 删除数据，并且重置主键自增
~~~

## 严格模式

~~~python
# 查看严格模式
show variables like "%mode";
# 修改严格模式
set session  # 只在当前窗口有效
set global  # 全局有效
set global sql_mode='STRICT_TRANS_TABLES';
# 修改完成后需要重新登录
~~~

## 枚举和集合

~~~python
# 枚举,多选一
sex enum('male','female','other')
# 集合,多选多
hobby set('write','read','drug','running')
# 插入数据时多选多格式 'write,read'
~~~

## 约束条件

~~~python
# default默认值
default'值'

# unique唯一
	# 单列唯一
    id int unique # id这个字段不能出现重复值
    # 联合唯一
    ip char(16),
    port int,
    unique(ip,port) # 设置ip和port联合唯一，即单个都可以重复，联合在一起不能重复

# primary key主键
	# 非空且唯一 not null + unique
    id int primary key
    # 它时innodb存储引擎组织数据的依据，即innodb存储引擎在创建表的时候必须要有主键
    # 一张表中有且只有一个主键，如果没有设置主键，会把表中的非空且唯一的字段设置为主键，如果没有这样的字段，那么会自动生成一个隐藏的字段作为主键，这个字段无法使用
    # 联合主键
    ip char(16),
    port int,
    primary key(ip,port)
    
# auto_increment自增,只能加在key上面
id int primary key auto_increment
~~~

## 表与表之间建关系

## 一对多

~~~python
# 外键foregin key

# 一对多，单向
	外键关系建立在多的那一方
	在创建表的时候一定要先建被关联表
    在录入数据的时候也必须先录入被关联表
    # 一个部门可以有多个员工，但是一个员工只能有一个部门
    # 部门表
    create table dep(
    id int primary key auto_increment,
    dep_name char(16),
    dep_desc char(32)
    );
    # 员工表 
    create table emp(
    id int primary key auto_increment,
    name char(16),
    gender enum('male','female'),
    dep_id int,
    foreign key(dep_id) references dep(id) # 本表字段关联被关联表的字段
    );
    # 级联更新/删除（一般情况下设立了外键字段的数据不能随意更改）
    # 需要在建立外键的时候声明
    foreign key(dep_id) references dep(id)
    on update cascade # 同步更新
    on delete cascade # 同步删除  
~~~

## 多对多

~~~python
# 针对多对多字段表关系，不能在两张原有的表中创建外键，需要单独开设一张专门用来存储两张表数据之间关系的表
# 图书表
create table book(
	id int primary key auto_increment,
    title varchar(32),
    price float
);
# 作者表
create table author(
	id int primary key auto_increment,
    name varchar(32),
    age int
);
# 关联表
create table book_authot(
	id int primary key auto_increment,
    author_id int,
    book_id int,
    foreign key(author_id) references author(id)
    on updata cascade
    on delete cascade,
    foreign key(book_id) references book(id)
    on updata cascade
    on delete cascade,
);
~~~

## 一对一

~~~python
# 如果一个表的字段特别多，每次查询又不是所有的字段都能用得到，就可以把表拆开，建立一对一的关系表
# 一般来说外键建在查询较多表中

# 用户详情表
create table authordetail(
	id int primary key auto_increment,
    phone int,
    addr varchar(64),
    gender enum('male','female')
);

# 用户表
create table author(
	id int primary key auto_increment,
    name varchar(64),
    age int,
    authordetail_id int unique,
    foreign key(authordetail_id) references authordetail(id)
    on updata cascade
    on delete cascade
);
~~~

## 修改表

~~~python
# 修改表名
alter table 表名 rename 新表名;
# 增加字段
alter table 表名 add 字段名 字段类型(宽度) 约束条件;
alter table 表名 add 字段名 字段类型(宽度) 约束条件 first; # 放在表首
alter table 表名 add 字段名 字段类型(宽度) 约束条件 after 字段名; # 跟在某字段后
# 删除字段
alter table 表名 drop 字段名;
# 修改字段
alter table 表名 modify 字段名 字段类型(宽度) 约束条件;
alter table 表名 change 旧字段名 新字段名 字段类型(宽度) 约束条件;
~~~

## 复制表

~~~python
# sql语句的查询结果其实也是一张虚拟表
create table 表名 select * from 旧表 where 条件; # 只能复制表结构和数据，主键外键索引等无法复制
~~~

## where约束条件

~~~python
# 作用：对整体数据的一个筛选操作

# 查找id在[3,6]的数据
select id,name,age from emp where id>=3 and id<=6;
select id,name,age from emp where id between 3 and 6;

# 查询id不在[3,6]的数据
select id,name,age from emp where id not between 3 and 6;

# 查找salary是200或100或150的数据
select * from emp where salary=200 or salary=100 or salary=150;
select * from emp where salary in (200,100,150);
select * from emp where salary not in (200,100,150); # 不在这个范围内的

# 查询员工姓名包含字面o的数据
'''
模糊查询like
% 表示匹配任意多个字符
_ 表示匹配单个字符
'''
select * from emp where name like '%o%';
# 查询员工姓名是由四个字符组成的
select * from emp where name like '____';
select * from where char_length(name) = 4;

# 查询age为空的数据
select * from emp where age is NULL; # 针对null不用等号，用is
select * from emp where age is not NULL;
~~~

## group by分组聚合

~~~python
'''分组之后，最小可操作单位应该是组，而不再是组内的元素'''

# 获取每个部门的最高薪资
select post as '部门',max(salary) as '最高薪资' from emp group by post; # as可以给字段名或者表名起别名

'''
聚合函数
sum
max
min
avg
count
'''

# 查询分组之后部门名称和每个部门下所有员工的姓名
'''group_concat 获取分组之后的其他字段值可获取多个，支持字符串拼接'''
'''concat 字符串拼接'''
select post,group_concat(name,'：',salary) from emp group by post;

# 一些注意事项
'''
关键子where和group by同时出现的时候group by必须在where的后面
聚合函数只能在分组之后使用
where筛选条件不能使用聚合函数
'''
# 查询每个部门年龄大于30岁的员工的平均薪资
select post,avg(salary) from emp where age > 30 group by post;
~~~

## having分组后筛选

~~~python
'''
having的语法和where是相同的
但是having是在分组之后进行的过滤操作
having可以直接使用聚合函数
'''

# 查询每个部门年龄大于30岁的员工的平均薪资大于10000的部门
select post,avg(salary) as avs from emp where age > 30 group by post having avs > 10000 ;
~~~

## distinct去重

~~~python
# 必须是完全一样的数据才可以去重
# 一定要注意有主键存在的情况下是不可能去重的
select distinct age from emp;
~~~

## order by排序

~~~python
# 把数据按照薪资排序
select * from emp order by salary;
'''
order by 默认升序
关键字：asc升序 desc降序
'''

# 先按照age的降序排，age相同按照salary的升序排
select * from emp order by age desc,salary asc;
~~~

## limit限制展示条数

~~~python
'''针对数据过多的情况，一般进行分页处理'''
# 从emp表中展示前3条数据
select * from emp limit 3;

# 第一个数字的起始位置，第二个是条数
select * from emp limit 0,5;
~~~

## 正则

~~~python
select * from emp where name regexp '^j.*(n|y)$'
~~~

## 多表查询

~~~python
'''
inner join 内连接 
left join 左连接
right join 右连接
union 全连接
'''

# 内连接，只拼接两张表共有的数据部分
select * from emp inner join dep on emp.dep_id = dep.id;
# 左连接，以左表为标准，没有对应的项就用NULL填充
select * from emp left join dep on emp.dep_id = dep.id;
# 右连接
# 全连接，即把左连接和右连接的表拼接在一起
select * from emp left join dep on emp.dep_id = dep.id
union
select * from emp right join dep on emp.dep_id = dep.id;
~~~

## 子查询

~~~python
'''将一个查询的结果当作另一个查询的条件'''
select * from emp where dep_id in (select id from dep where name='技术' or name='人力资源');

# 只要是多表查询，就有两种思路 - 联表和子查询

# 关键字exist
# 返回bool值，返回true时外层查询语句执行。
select * from emp where exists (select id from dep where id > 3);
# 即如果子语句有值，才会执行外层的语句
~~~



# MySQL的数据类型

## 数值类型

| 类型         | 大小                                     | 范围（有符号）                                               | 范围（无符号）                                               | 用途            |
| :----------- | :--------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :-------------- |
| TINYINT      | 1 byte                                   | (-128，127)                                                  | (0，255)                                                     | 小整数值        |
| SMALLINT     | 2 bytes                                  | (-32 768，32 767)                                            | (0，65 535)                                                  | 大整数值        |
| MEDIUMINT    | 3 bytes                                  | (-8 388 608，8 388 607)                                      | (0，16 777 215)                                              | 大整数值        |
| INT或INTEGER | 4 bytes                                  | (-2 147 483 648，2 147 483 647)                              | (0，4 294 967 295)                                           | 大整数值        |
| BIGINT       | 8 bytes                                  | (-9,223,372,036,854,775,808，9 223 372 036 854 775 807)      | (0，18 446 744 073 709 551 615)                              | 极大整数值      |
| FLOAT        | 4 bytes                                  | (-3.402 823 466 E+38，-1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38) | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                  | 单精度 浮点数值 |
| DOUBLE       | 8 bytes                                  | (-1.797 693 134 862 315 7 E+308，-2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 双精度 浮点数值 |
| DECIMAL      | 对DECIMAL(M,D) ，如果M>D，为M+2否则为D+2 | 依赖于M和D的值                                               | 依赖于M和D的值                                               | 小数值          |

**浮点型**：salary float(255,30)  表示总共255位，其中小数位数占30位

## 日期类型

| 类型      | 大小 ( bytes) | 范围                                                         | 格式                | 用途                     |
| :-------- | :------------ | :----------------------------------------------------------- | :------------------ | :----------------------- |
| DATE      | 3             | 1000-01-01/9999-12-31                                        | YYYY-MM-DD          | 日期值                   |
| TIME      | 3             | '-838:59:59'/'838:59:59'                                     | HH:MM:SS            | 时间值或持续时间         |
| YEAR      | 1             | 1901/2155                                                    | YYYY                | 年份值                   |
| DATETIME  | 8             | 1000-01-01 00:00:00/9999-12-31 23:59:59                      | YYYY-MM-DD HH:MM:SS | 混合日期和时间值         |
| TIMESTAMP | 4             | 1970-01-01 00:00:00/2038结束时间是第 **2147483647** 秒，北京时间 **2038-1-19 11:14:07**，格林尼治时间 2038年1月19日 凌晨 03:14:07 | YYYYMMDD HHMMSS     | 混合日期和时间值，时间戳 |

## 字符串类型

| 类型       | 大小                  | 用途                            |
| :--------- | :-------------------- | :------------------------------ |
| CHAR       | 0-255 bytes           | 定长字符串，不够空格补全        |
| VARCHAR    | 0-65535 bytes         | 变长字符串                      |
| TINYBLOB   | 0-255 bytes           | 不超过 255 个字符的二进制字符串 |
| TINYTEXT   | 0-255 bytes           | 短文本字符串                    |
| BLOB       | 0-65 535 bytes        | 二进制形式的长文本数据          |
| TEXT       | 0-65 535 bytes        | 长文本数据                      |
| MEDIUMBLOB | 0-16 777 215 bytes    | 二进制形式的中等长度文本数据    |
| MEDIUMTEXT | 0-16 777 215 bytes    | 中等长度文本数据                |
| LONGBLOB   | 0-4 294 967 295 bytes | 二进制形式的极大文本数据        |
| LONGTEXT   | 0-4 294 967 295 bytes | 极大文本数据                    |

**注意**：char(n) 和 varchar(n) 中括号中 n 代表字符的个数，并不代表字节个数，比如 CHAR(30) 就可以存储 30 个字符。

CHAR 和 VARCHAR 类型类似，但它们保存和检索的方式不同。它们的最大长度和是否尾部空格被保留等方面也不同。在存储或检索过程中不进行大小写转换。
char：浪费空间，但速度快
varchar：节省空间，但速度慢，存的时候会存入一个报头，记录数据的长度

BINARY 和 VARBINARY 类似于 CHAR 和 VARCHAR，不同的是它们包含二进制字符串而不要非二进制字符串。也就是说，它们包含字节字符串而不是字符字符串。这说明它们没有字符集，并且排序和比较基于列值字节的数值值。

BLOB 是一个二进制大对象，可以容纳可变数量的数据。有 4 种 BLOB 类型：TINYBLOB、BLOB、MEDIUMBLOB 和 LONGBLOB。它们区别在于可容纳存储范围不同。

有 4 种 TEXT 类型：TINYTEXT、TEXT、MEDIUMTEXT 和 LONGTEXT。对应的这 4 种 BLOB 类型，可存储的最大长度不同，可根据实际情况选择。

# 杂项知识点

## 视图

~~~python
# 视图
'''
视图就是通过查询得到一张虚拟表，然后保存下来，下次可以直接使用
如果要频繁的操作一张虚拟表（拼表组成的），就可以将其制作成视图
'''
# 固定语法
create view 表名 as 虚拟表的查询sql

'''
创建视图在硬盘上只会有表结构，没有表数据（数据还是来自之前的表）
视图一般只用来查询，里面的数据不要继续修改，可能会影响真正的表
'''
~~~

## 触发器

~~~python
# 触发器
'''
在满足对表数据进行增删改的情况下自动触发的功能
使用触发器可以帮助我们实现监控、日志......
'''
# 基本语法结构
delimiter $$
create trigger 触发器名字 before/after insert/update/delete on 表名
for each row
begin
	sql语句;
end $$
delimiter ;

# 删除触发器
drop trigger 触发器名
~~~

## 事务

~~~python
# 事务
'''
开启一个事物可以包含多条sql语句，这些sql语句要么同时成功，要么都不成功
事务保证了数据的安全性
'''

'''
四大特性ACID
A：原子性
	一个事务是一个不可分割的单位
C：一致性
	事务必须是让数据库从一个一致性状态变到另一个一致性状态
I：隔离性
	一个事务的执行不能被其他事务干扰
D：持久性
	一个事务一旦提交执行成功，那么它对数据库中数据的修改应该是永久的
'''

# 事务相关的关键字
'''
1.开启事务
start transaction;
2.回滚(回到事务执行之前的状态)
rollback;
3.确认(确认之后就无法回滚了)
commit;
'''
~~~

