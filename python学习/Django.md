# Django

## **命令行操作**

~~~python
# 创建django项目
django-admin startproject 项目名
# 启动django项目
先cd到文件夹下
python manange.py runserver ip:端口 # ip端口可以不用写，默认是本机的回环地址
# 创建app，app就是一个功能
python manage.py startapp app01
# 去settings.py注册app
INSTALLED_APPS列表的结尾加上app的文件名
~~~

## **主要文件介绍**

~~~python
--mysite 项目文件夹
	--mysite 文件夹
		--settings.py 配置文件
         --urls.py 路由与视图函数的对应关系
         --wsgi.py wsgiref模块
    --manage.py django入口文件
    --db.sqlite3 django自带的sql
    --app 文件夹
    	--admin.py django后台管理
        --apps.py 注册使用
        --migrations文件夹 数据库迁移记录
        --models.py 数据库相关
        --tests.py 测试文件
        --views.py 视图函数
    --templates 存放html文件的文件夹 # 需要手动创建，并且去settings.py文件夹下配置的TEMPLATES中的'DIRS': []，为'DIRS': [os.path.join(BASE_DIR,'templates')]
    
~~~

## **函数返回**

~~~python
# views.py
from django.shortcuts import render, HttpResponse, redirect
def func(request): # 参数必须有且必须叫这个
    return render(request,'html文件路径',locals()) # 返回html文件,locals()将当前名称空间的变量发送给html
	return HttpResponse('hello') # 返回字符串数据类型
	return redirect('url') # 重定向，定向到内部的html时可以只写后缀 /index/

~~~

## **request对象解析**

~~~python
request.method # 获取当前请求方式，返回全大写的字符串
request.POST # 获取用户提交的post请求数据（不包括文件），返回字典，值是列表
request.POST.get('key') # 获取值，get只会获取列表最后一个元素
request.POST.getlist('key') # 获取值，是列表
request.GET # 获取用户提交的get请求数据，返回字典，值是列表，其他用法和POST一样
request.path # 获取路由，但是不能获取路由后面的参数
request.get_full_path # 获取路由和参数
~~~

## **静态文件配置**

~~~python
# 在项目文件下创建一个static文件夹，一般情况下在static文件下会做进一步的划分处理，如 css 目录，js 目录，images 目录，plugins 目录，分别放 css文件，js文件，图片，插件。

# 在settings.py内配置
STATIC_URL = '/static/' # 访问静态文件的令牌，别名
STATICFILES_DIRS = [ # 令牌持有者可以访问的文件路径
    os.path.join(BASE_DIR,'static')
]
# 查找顺序是从上往下，查到第一个就不会继续查找

# 注意：此时引用路径中的要用配置文件中的别名 static，而不是目录 statics。
<link rel="stylesheet" href="/static/plugins/bootstrap-3.3.7/dist/css/bootstrap.css"> # 直接固定

# 静态文件的动态解析
{% load static %}
<link rel='stylesheet' href="{% static '文件路径'%}">

{% load static %}
{{name}}<img src="{% static "images/runoob-logo.png" %}" alt="runoob-logo">
~~~

## **post请求权限**

~~~python
{% csrf_token %}
~~~

## **数据库配置**

~~~python
# 在settings.py内配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '库名',
        'USER': 'root',
        'PASSWORD': '1181801087',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CHARSET': 'utf8',
    }
}
# 代码声明
django默认用的是mysqldb模块，但是这个模块的兼容性不好，需要手动改变
'''
在项目名下的init或者任意的应用名下的init文件中书写：
import pymysql
pymysql.install_as_MySQLdb()
'''
~~~

## url、path、re_path

~~~python
# path() 函数
# path() 可以接收四个参数，分别是两个必选参数：route、view 和两个可选参数：kwargs、name。

# 语法格式：
path(route, view, kwargs=None, name=None)
# route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。

# view: 用于执行与正则表达式匹配的 URL 请求。

# kwargs: 视图使用的字典类型的参数。

# name: 用来反向获取 URL。

# Django2.0中可以使用 re_path() 方法来兼容 1.x 版本中的 url() 方法，一些正则表达式的规则也可以通过 re_path() 来实现 。

from django.urls import include, re_path
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]
~~~



# django ORM

~~~python
# ORM对象关系映射
# 不足之处：封装程度太高，有时候sql语句效率偏低，需要自己写

# 应用的models.py文件中写一个类，这个类就是一个表
class User(models.Model):
    id = models.AutoField(primary_key=True)
    # 如果类中没有主键字段，orm会自动加上，并且就叫id
    username = models.CharField(max_length=32)
    # CharField必须要指定max_length参数，verbose_name所有字段都有，作用是对字段的解释
    password = models.IntegerField()
    
# 数据库迁移指令
python manage.py makemigrations # 将操作记录到migrations文件下
python manage.py migrate # 同步到数据库

# 只要修改了models.py中跟数据库相关的代码就要执行数据库迁移指令
~~~

![orm-object](C:\Users\Zhao\Desktop\图\orm-object.png)

**字段的增删改查**

~~~python
# 在models.py文件中的类下进行修改后输入数据库迁移指令

# 增
如果原表中已经有数据
1.可以直接在终端中给出默认值
2.设置参数null：null=True，即该字段可以为空
3.设置参数default：default='默认值'，指定字段默认值

# 删，改
直接修改代码，执行数据库迁移指令
删除执行完毕后，字段对应的数据全部清空（谨慎使用）
~~~

**数据的增删改查**

~~~python
# 去数据库中查数据
from app1 import models
username = request.POST.get('username')
password = request.POST.get('password')
res = models.User.objects.filter(username=username).first()
# 一个特殊的列表，支持索引切片，不支持负数索引，first()就是取出数据，没有就是空
# filter() 可以携带多个参数，参数与参数直接是and关系，可以看作where
# User是类名
if res:
	if password == res.password: # 数据库查到的密码
        pass
~~~

~~~python
# 给数据库增加数据
res = models.User.objects.create(username=username,password=password) # 返回当前被创建的对象本身
res = models.User(username=username,password=password)
res.save() # 保存数据
~~~

~~~python
# 修改数据
models.User.objects.filter(id=user_id).update(username=username,password=password) # 批量更新操作

models.User.objects.filter(id=user_id).delete() # 批量删除

# url问号后面的是参数，不参与路径匹配，但是可以被视图函数捕捉到
<a herf='/edit_user/?user_id={{ user_obj.id }}'>
~~~

## ORM创建表关系

~~~python
# models.py

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    publish = models.ForeignKey(to='Publish',on_delete=True) # 默认与外键表的主键字段关联
    authors = models.ManyToManyField(to='Author')
    # authors是一个虚拟字段 主要是用来告诉orm 数据表和作者是多对多关系
    # orm会自动创建第三张表

class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    # 作者和作者详情是一对一的关系，外键字段建在查询频率高的一方
    author_detail = models.OneToOneField(to='Authordetail',on_delete=True)


class Authordetail(models.Model):
    phone = models.BigIntegerField()
~~~

## django请求生命周期流程图

![django请求生命周期流程图](C:\Users\Zhao\Desktop\图\django请求生命周期流程图.png)![django请求生命周期图](C:\Users\Zhao\Desktop\图\django请求生命周期图.png)

**路由分配**

~~~python
# urls.py
url()的第一个参数是一个正则表达式，只要第一个参数的正则表达式能够匹配到内容，那么就不会再匹配接下来的url

匹配首页url（什么都不匹配）url(r'^$',view.home)

# django的每一个应用都可以有自己的templates文件夹，urls.py,static文件夹
# 利用路由分发之后，总路由不再干路由与视图函数的直接对应关系，而是做一个分发处理
# 识别当前url是

# 总urls.py
from django.urls import include
from app01 import urls as app01_urls
from app02 import urls as app02_urls
urlpatterns = [
	url(r'^app01/',include(app01_urls)), # 只要url前缀是app01开头的全部交给app01下的urls和views处理
    url(r'^app02/',include(app02_urls))
    # 更简洁的写法，不用import导入各应用
    url(r'^app01/',include('app01.urls'))
]
~~~

## 无名分组，有名分组

~~~python
# 无名分组
分组：给某一段正则表达式加一段小括号
url(r'^test/(\d+)',view.test)
无名分组就是将括号内正则表达式匹配到的内容当作位置参数传递给后面的视图函数
def test(request,num):
    print(num)
    return HttpResponse('hello')

# 有名分组
url(r'^test/(?P<year>\d+)',view.test)
有名分组就是将括号内正则表达式匹配到的内容当作关键字参数传递给后面的视图函数
def test(request,year):
    print(year)
    return HttpResponse('hello')

# 两者不能混合使用，单个可以多次使用
~~~

## **反向解析**

~~~python
# 本质：通过一些方法得到一个结构，该结果可以访问到对应的url从而触发视图函数的运行，实际上就是通过url访问而已

# 先给路由与视图函数起一个别名，别名不能冲突
url(r'^func/',views.func,name='func')
# 后端反向解析
from django.shortcuts import reverse
reverse('func')
# 前端反向解析
<a href="{% url 'func' %}">111<\a>


# 无名分组的反向解析
url(r'^index/(\d+)',views.index,name='xxx')
# 后端
def index(request):
    print(reverse('xxx',args=(数字,)))
# 前端
{% url 'xxx' 数字 %}
# 这个数字一般情况下放的是数据的主键值

# 有名分组的反向解析
url(r'^func/(?P<year>\d+)',views.func,name='xxx')
# 后端
def func(request,year):
    print(reverse('xxx'),kwargs={'year':数字})
# 前端
{% url 'xxx' year=数字 %}
# 这个数字一般情况下放的是数据的主键值
~~~

## **名称空间**

~~~python
# 正常情况下的反向解析不能识别url前缀
# 总urls.py
url(r'^app01/',include('app01.urls',namespace='app01'))
url(r'^app02/',include('app02.urls',namespace='app02'))

# 解析的时候
# app01
urlpatterns = [
	url(r'^reg/',views.reg,name='reg')
]
# app02
urlpatterns = [
	url(r'^reg/',views.reg,name='reg')
]

reverse('app01:reg')
reverse('app02:reg')
{% url 'app01:reg' %}
{% url 'app02:reg' %}

# 一般只要保证名字不冲突就没有必要使用名称空间
# app01
urlpatterns = [
	url(r'^reg/',views.reg,name='app01_reg')
]
# app02
urlpatterns = [
	url(r'^reg/',views.reg,name='app02_reg')
]

~~~

## 三板斧

~~~python
'''
HttpResponse；返回字符串类型
render；返回html页面，并且在返回给浏览器之前还可以给html文件传值
redirect：重定向，跳转新页面。参数为字符串，字符串中填写页面路径。一般用于 form 表单提交后，跳转到新页面。
def runoob(request):
    return redirect("/index/")
'''
# 视图函数必须返回一个HttpResponse对象
~~~

## JsonResponse对象

~~~python
from django.http import JsonResponse
def func(request):
    user_dict = {'user':'赵徐璐','password':123}
    # 读源码掌握用法!
    return JsonResponse(user_dict,json_dumps_params={'ensure_ascii':False},safe=False)
# 返回json对象，默认只能序列化字典，序列化其他需要修改safe参数为False
~~~

## 文件上传

~~~python
request.FILES # 获取文件数据
obj = request.FILES.get('file') # 获取文件对象
obj.name # 文件名
obj.chunks() # 对文件进行切片
~~~

## FBV与CBV

~~~python
# 视图函数既可以是函数（fbv）也可以是类（cbv）
from django.views import View
class MyLogin(View):
    def get(self,request):
        return HttpResponse("get方法")
    def post(self,request):
        return HttpResponse("post方法")
# cbv路由
url(r'^login/',views.MyLogin.as_view())
~~~

## 模板语法传值

~~~python
# view：｛"HTML变量名" : "views变量名"｝
# HTML：｛｛变量名｝｝
from django.shortcuts import render

def runoob(request):
  views_name = "菜鸟教程"
  return render(request,"runoob.html",{"name":views_name})
# render方法的第三个参数，表示将这个变量传递给html文件，然后就可以在html文件内用模板语法调用了


# 模板语法
{{}} : 变量相关
{% %} : 逻辑相关

    
def index(request):
    # 模板语法可以传递的后端python数据类型
    n = 123
    f = 1.12
    s = '赵徐璐'
    l = ['123',123,'徐路']
    d = {'username':'赵','password':123456}
    se = {'弟弟','123'}
    t = (1,2,3)
    def func():
        print('函数执行')
        return '函数执行结束'
    class Myclass(object):
        def get_self(self):
            return 'self'
    obj = Myclass()
    return render(request,'index.html',locals())
# 传递函数名会自动加括号调用，但是模板语法不支持给函数传递参数
# 类以及类对象都可以传递，但也不支持传参数

# django的模板语法取值采用的是‘句点符’形式
d = {'user':[1,2,[3,4]]}
{{ d.user.2.1 }} # 可以点键值，也可以点索引
~~~

## 过滤器

~~~python
# 基本语法
{{数据|过滤器:参数}}

# 过滤器
length ：计算长度
default ：数据为true就展示，否则就展示参数
filesizeformat ：格式化显示文件大小
date ：日期格式化，参数是格式，一般为'Y-m-d H:i:s'
slice ：切片，参数'0:4:2'，开始，终止，步长
truncatechars ：显示多少字符，参数为个数，包含三个点
cut ：移除特定字符，参数为要移除的字符
safe ：取消转义

# 取消转义的后端操作
from django.utils.safestring import mark_safe
res = mark_safe('<h1>转义</h1>')

# 过滤管道可以被套接 ，既是说，一个过滤器管道的输出又可以作为下一个管道的输入：
{{ my_list|first|upper }}

# 关于safe
# 将字符串标记为安全，不需要转义。
# 要保证 views.py 传过来的数据绝对安全，才能用 safe。
# 和后端 views.py 的 mark_safe 效果相同。
# Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。

~~~

## 标签

~~~python
# {% %} : 逻辑相关
# forloop的相关参数
{'parentloop': {}, 'counter0': 0, 'counter': 1, 'revcounter': 10, 'revcounter0': 9, 'first': True, 'last': False}
'''
在 {% for %} 标签里可以通过 {{forloop}} 变量获取循环序号。
forloop.counter: 顺序获取循环序号，从 1 开始计算
forloop.counter0: 顺序获取循环序号，从 0 开始计算
forloop.revcounter: 倒叙获取循环序号，结尾序号为 1
forloop.revcounter0: 倒叙获取循环序号，结尾序号为 0
forloop.first（一般配合if标签使用）: 第一条数据返回 True，其他数据返回 False
forloop.last（一般配合if标签使用）: 最后一条数据返回 True，其他数据返回 False
'''

# if
# 根据条件判断是否输出。if/else 支持嵌套。
# {% if %} 标签接受 and，or 或者 not 关键字来对多个变量做判断 ，或者对变量取反（not）
{% if 条件 %}
{% elif %}
{% else %}
{% endif %}

# for
{% for i in lis %}
{% endfor %}
{% empty %} # for循环的对象是空的就执行

# {% for %} 允许我们在一个序列上迭代。
# 与 Python 的 for 语句的情形类似，循环语法是 for X in Y ，Y 是要迭代的序列而 X 是在每一个特定的循环中使用的变量名称。
# 每一次循环中，模板系统会渲染在 {% for %} 和 {% endfor %} 之间的所有内容。
# 例如，给定一个运动员列表 athlete_list 变量，我们可以使用下面的代码来显示这个列表：
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
# 给标签增加一个 reversed 使得该列表被反向迭代：
{% for athlete in athlete_list reversed %}
...
{% endfor %}

# with起别名
{% with d.hobby.1.0 as 别名 %}
~~~

## 自定义过滤器、标签、inclusion_tag

~~~python
1.在应用下创建一个名字为templatetags的文件夹
2.在该文件夹内创建一个py文件
3.然后在该py文件的开头写以下两句话
from django import template
register = template.Library()#register的名字是固定的,不可改变

# 在settings文件内配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "/templates",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "libraries":{                          # 添加这边三行配置
                'my_tags':'templatetags.my_tags'   # 添加这边三行配置        
            }                                      # 添加这边三行配置
        },
    },
]

# 自定义过滤器，最多两个参数，name表示别名
@register.filter(name='zhao')
def my_sum(v1,v2):
    return v1+v2

# 自定义标签
@register.simple_tag(name='xulu')
def inde(a,b,c,d):
    return f'{a}{b}{c}{d}'

# 自定义inclusion_tag
@register.inclusion_tag('zhao.html')
def left(n):
    dta = [f'第{i}项' for i in range(n)]
    return locals() # 把dta传递给zhao.html，这个html实际上就为了帮助渲染的
'''
原理：
先定义一个方法
在页面上调用该方法，并且可以传值
该方法会生成一些数据然后传递给一个html页面渲染
之后将渲染好的结果放到调用位置
'''


# 前端使用时先用load导入，要在 html 文件 body 的最上方中导入该 py 文件
{% load py文件名 %}
# 自定义过滤器inclusion_tag
<p>{{ n|zhao:10 }}</p>
# 自定义标签
<p>{% xulu 'zhao' 1 2 3 %}</p>
# 自定义inclusion_tag
{% left 10 %}
~~~

## 模板的继承、导入

~~~python
# 继承模板页面
{% extends '模板.html' %}
# 标记修改区域，模板页面标记范围，子模版再用标记修改
{% block 名字 %}
'可修改的内容'
{% endblock %}

# 模板页面上一般至少有三个可以修改的区域
1.css区域
2.js区域
3.html区域

# 模板的导入
{% include '导入模板.html' %}
~~~

# ORM的表操作

~~~python
# 两个字段
DateField() 年月日
DateTimeField() 年月日时分秒
# 两个关键参数
auto_now 每次操作数据的时候，该字段会自动更新
auto_now_add 创建数据的时候，自动将创建时间记录，之后只要不修改这个时间，他就一直不变
~~~

## 测试脚本环境

~~~python
# 当你想测试django中某一py文件时
# 把下面的代码写入tests文件内，就可以使用了，这些代码在manage中
import os
import sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Test1.settings')

if __name__ == '__main__':
    main()
    import django # 手写
    django.setup() # 手写
    # 要测试什么就导入什么
    from app import models   
~~~

## 必知必会13条

~~~python
res = models.User.objects.filter(pk=2).first() # pk字段表示当前表的主键

1.all() 查询所有数据
2.filter() 带有过滤条件的查询
3.get() 直接拿数据对象，如果不存在则报错
4.first() 获取queryset里面的第一个对象
5.last() 获取最后一个
6.values() 按照字段名取值，返回queryset对象，类似列表套字典
7.values_list() 返回queryset对象，类似列表套元组
8.distinct() 去重，但是一定要注意是否包含主键字段
9.order_by() 排序，按照某字段排序，默认升序，降序就在字段名前加上负号
10.reverse() 反转，前提是对象必须经过排序
11.count() 计数，统计当前数据个数
12.exclude() 除某一条件之外的数据
13.exists() 判断数据是否存在，返回bool值
~~~

## 双下划线查询

~~~python
# 年龄大于35岁的数据
res = models.User.objects.filter(age__gt=25)
# 小于 __lt
# 大于等于 __gte 
# 小于等于 __lte
# 在某几个数里面 __in=['元素','元素1']
# 在某个范围之间 __range=[start,end] 包含首尾
# 模糊查询 __contains='n' 忽略大小写__icontains='n'
# 时间查询 __month,__year,__day
~~~

## 多表操作

~~~python
# 外键的增删改查

# 一对多
# 直接写实际字段id
models.Book.objects.create(title='呐喊',publish_id=1)
# 虚拟字段对象
publish_obj = models.Publish.objects.filter(pk=2).first()
models.Book.objects.create(title='呐喊',publish=publish_obj)

# 多对多
# 实际上就是操作第三张表
book_obj = models.Book.objects.filter(pk=1).first()
# 增加
book_obj.authors.add(1,2) # 可以放多个参数，也可放对象
# 删除
book_obj.authors.remove(2) # 可以放多个参数，也可以放对象
# 修改
book_obj.authors.set([1,2]) # 参数必须是一个可迭代对象，可迭代对象内可以放多个元素，本质上时先删后增
# 清空
book_obj.authors.clear() # 清空关于id为1的书籍与作者的所有关系

~~~

## 正反向概念

~~~python
# 从有外键字段的表去查关联表叫正向，反之则叫反向
~~~

## 多表查询

~~~python
正向查询按字段，反向查询按小写表名__
# 子查询（基于对象的跨表查询）
# 查询书籍id为1的出版社
book_obj = models.Book.objects.filter(pk=1).first()
res = book_obj.publish
res.name
res.addr

# 查询书籍id为1的作者
res = book_obj.authors.all()
# 当查询结果有多个时需要加上all()

# 查询出版社是东方出版社的书,反向
publish_obj = models.Publish.objects.filter(name='东方出版社')
res = publish_obj.book_set.all()
# 当查询结果有多个时，表名小写需要加上 _set.all() 只有一个的时候不需要加


# 基于双下划线的跨表查询
# 查询鲁迅的手机号和姓名
res = models.Author.objects.filter(name='鲁迅').values('author_detail__phone')
# 反向
res = models.AuthorDetail.objects.filter(author__name='鲁迅').values('phone','author__name')

# 查询书籍id为1的出版社名称，和书的名字
res = models.Book.objects.filter(pk=1).values('title','publish__name')


# 在filter和values中，在我们在models创建类的时候设置的外键字段，可以当作是联系两张表的桥梁，当这些字段出现在其中是，就可以看作是在本表上打开了通向关联表的通路，然后通过__双下划线去操作关联表

~~~

## 聚合查询

~~~python
# 通常情况下配合分组一起使用 aggregate
from django.db.models import Max,Min,Sum,Count,Avg
# 所有书的平均价格
res = models.Book.objects.aggregate(Avg('price'))
~~~

## 分组查询

~~~python
# annotate
# 统计每一本书的作者个数
res = models.Book.objects.annotate(author_num=Count('authors')).values('title','author_num')

# 统计每个出版社最便宜的书的价格
res = models.Publish.objects.annotate(min_price=Min('book__price')).values('name','min_price')

# 统计不止一个作者的图书
res = models.Book.objects.annotate(author_num=Count('authors')).filter(author_num__gt=1).values('title','author_num')

# 按照某一字段分组
models.Book.objects.values('price').annotate()
# values出现在annotate之前的话就按照values指定的字段分组
~~~

## F与Q查询

~~~python
# F查询
# F的作用是获取本表中的字段数据
from django.db.models import F
# 查询销售大于库存的书
res = models.Book.objects.filter(sell__gt=F('stock'))

# 在操作字符类型的数据的时候，F不能够直接做字符串的拼接
from django.db.models.functions import Concat
from django.db.models import Value
models.Book.objects.update(title=Concat(F('title'),Value('1')))
~~~

~~~python
# Q查询
from django.db.models import Q
# 查询卖出数大于100或者价格小于600的书籍
res = models.Book.objects.filter(Q(sell__gt=100)|Q(price__lt=600))
# 用Q包裹的数据可以实现关系
, 表示and
| 表示or
~ 表示not

# Q的高阶用法
q = Q()
q.connector = 'or' # 修改链接关系，默认and
q.children.append(('sell__gt',100)) # 添加查询条件
q.children.append(('price__lt',600))
res = models.Book.objects.filter(q)
~~~

## django中开启事务

~~~python
from django.db import transaction
with transacthion.atomic():
    # 在with代码块内书写的所有orm操作都是属于同一个事务
~~~

## ORM中常用字段和参数

~~~python
AutoField：定义主键字段

CharField：varchar()
    verbose_name 字段注释
    max_length 长度
    
IntegerField：int
BigIntegerField：int

EmailField：varchar(254)

DateField：
DateTimeField：

BooleanField：布尔值类型，数据库存0/1

TextField：文本类型，用来存大段内容。没有字数限制

FileField：文件字段
	upload_to='path' 上传文件的保存路径，会自动将文件存在文件路径下，数据库内存文件路径

# django支持自定义字段

# 外键字段参数
unique=True # 形成一对一关系

db_index=True # 设置该字段为索引

to_field # 设置要关联表的字段，默认为主键

on_delete # 2.x版本即以上需要设置，表示级联更新删除
~~~

## 数据库查询优化

~~~python
only与defer
select_related与prefetch_related

'''
orm语句的特点：惰性查询
如果只是书写了orm语句，但是后面没有使用到该语句所查询出的数据
那么orm会自动识别，直接不执行
'''

# only
res = models.Book.objects.only('title')
for i in res:
    print(i.title) # 取only括号内的字段不走数据库
    print(i.price) # 取only括号外的字段会重新去数据库查询
# defer与only相反

# select_related 联表
res = models.Book.objects.select_related('publish')
# select_related内部直接将book和publish链接起来，然后一次性将大表里面的所有数据全部封装给查询出的对象
# select_related只能放外键字段，并且不能适用多对多的关系

# prefetch_related 子查询
res = models.Book.objects.prefetch_related('publish')
# 其他和select_related相同
~~~

## choices参数（数据库字段设计常见）

~~~python
# 针对某些可以列举完全的字段
gender_choices=((1,'male'),(2,'female'),(3,'others'))
gender = models.IntegerField(choices=gender_choices)

# 存数据的时候按照元组的对应关系存储数字
# 取的时候，只要是有choices参与的字段，固定写法get_字段名_display()
# 存的时候可以超出choices指定的数字范围，但是取的时候，因为没有对应关系，所以存什么取什么

# 保证字段类型，跟元组列举出来的第一个元素类型一致即可
~~~

## MTV与MVC模型

~~~python
# M：models（模型）
# T：templates（模板）
# V：views（视图）
# C：controller（控制器）
~~~

![MVCT](C:\Users\Zhao\Desktop\图\MVCT.png)

## 多对多三种创建方式

~~~python
# 全自动
models.ManyToManyField()
# 不足之处：第三张关系表的扩展性极差，无法添加额外字段

# 手动
自己创建第三张表，设置models.ForeignKey()
# 不足之处：无法使用orm方法

# 半自动
手动创建一第三张表，设置models.ForeignKey()
再去某张表中设置models.ManyToManyField(to='关联表',
                               		 through='第三张表的表名',
                              		 through_fields=('第三张表的字段','~'))
# through_fields参数的顺序是，当前这个字段建在哪个表，就把哪个表名字段放在前面
# 不足之处：可以使用orm查询，但是无法使用add，set，remove，clear这四个函数

# 一般来说，我们通常使用半自动这种方式
~~~

# Ajax

~~~html
异步提交，局部刷新
作用是在不重新加载整个页面的情况下，可以与服务器交换数据并且更新部分网页内容
<script>
    $('#btn').click(function () { // 绑定点击事件
        // 朝后端发送ajax请求
        $.ajax({
            // 指定向哪个后端发送ajax请求
            url:'', // 不写就是朝当前地址提交
            // 请求方式
            type:'post', // 不写默认get
            // 数据
            data:{}, // 以键值的形式存储
            dataType:'JSON', // 当后端是用HttpR返回的json数据格式时，会自动帮你反序列化
            // 回调函数：当后端给你返回结果的时候自动触发,args接收后端返回的结果
            success:function(args){
            	// 通过渲染到指定部分
        }
        })
    })
<\script>
针对后端，如果是用HttpResponse返回的数据，回调函数不会自动帮你反序列化
    如果用的是JsonResponse返回的数据，回调函数会自动帮你反序列化
~~~

## ajax发送json格式数据

~~~python
# 参数指定编码格式
contentType:'application/json', # 默认是urlencoded
data:JSON.stringify()
# 针对json格式数据，在后端需要手动处理
if request.is_ajax(): # 判断请求是否是ajax请求
    json_bytes = request.body # 二进制数据
    json_dict = json.loads(json_bytes) # 自动解码在反序列化
~~~

## ajax发送文件

~~~js
# ajax发送文件需要借助于js内置对象FromData
let fromDateObj = new FormDate();
fromDateObj.append('文件名',文件)

# ajax参数
contentType:false // 不需要使用任何编码，django后端能够自动识别formdata对象
processData:false // 告诉浏览器不要对数据进行任何处理

if request.is_ajax():
	if request.method == 'POST':
    	request.POST
		request.FILES
// django后端能够直接识别到formdata对象。
~~~

## django自带的序列化组件

~~~python
from django.core import serializers
lis = [{},{},{},{}]
res = serializers.serialize('json',lis)
~~~

## 批量插入

~~~python
book_list = []
for i in range(1000):
    book_obj = models.Book(title=f'第{i}本')
    book_list.append(book_obj)
    
models.Book.objects.bulk_create(book_list) # 批量插入，提高效率
~~~

## 自定义分页器的使用

~~~python
# 当我们需要使用到非django内置的第三方功能或者组件代码的时候，我们一般情况下会创建一个utils文件夹（项目文件夹下），在该文件夹内对模块进行功能性划分
class Pagination(object):
    def __init__(self, current_page, all_count, base_url, query_params, per_page=30, pager_page_count=11):
        """
        分页初始化
        :param current_page: 当前页码
        :param per_page: 每页显示数据条数
        :param all_count: 数据库中总条数
        :param base_url: 基础URL
        :param query_params: QueryDict对象，内部含所有当前URL的原条件
        :param pager_page_count: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        query_params = query_params.copy()
        query_params._mutable = True
        self.query_params = query_params
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        数据获取值起始索引
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        生成HTML页码
        :return:
        """
        if self.all_count == 0:
            return ""

        # 如果数据总页码pager_count<11 pager_page_count
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据页码已经超过11
            # 判断： 如果当前页 <= 5 half_pager_page_count
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # 如果： 当前页+5 > 总页码
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []

        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev = '<li><a href="%s?%s">上一页</a></li>' % (self.base_url, self.query_params.urlencode())
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">下一页</a></li>' % (self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)

        if self.all_count:
            tpl = "<li class='disabled'><a>共%s条数据，页码%s/%s页</a></li>" % (
            self.all_count, self.current_page, self.pager_count,)
            page_list.append(tpl)
        page_str = "".join(page_list)
        return page_str
~~~

~~~python
# 后端
# 1. 在视图函数中
# 假设有个问题表Issues
# 获取指定项目的问题
    queryset = models.Issues.objects.filter(project_id=project_id)
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=queryset.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    issues_object_list = queryset[page_object.start:page_object.end]

    context = {
        'issues_object_list': issues_object_list,
        'page_html': page_object.page_html()
    }
    return render(request, 'issues.html', context)
~~~

~~~python
# 前端
# 注意：自定义分页器的样式是基于bootstrap的，请提前导入bootstrap。
<!--对问题遍历-->
{% for item in issues_object_list %}
	{{item.xxx}}
{% endfor %}

<!--前端使用分页器-->
<nav aria-label="...">
   <ul class="pagination" style="margin-top: 0;">
       {{ page_html|safe }}
   </ul>
</nav>
~~~

# forms组件

~~~python
# 基本使用
from django import forms

class MyForm(forms.Form):
    # username字段最小3位最大8位
    username = forms.CharField(min_length=3,max_length=8,label='用户名',
                              error_messages={
                                  'min_length':'用户名最少3位',
                                  'required':'用户名不能位空',
                              })
    # error_messages是一个字典，键时限制条件，值是错误信息
    # email字段必须是邮箱格式
    email = forms.EmailField()

# 当我们的forms组件太多的时候我们一般会创建一个文件夹专门存放forms组件
~~~

## 校验数据

~~~python
from app import views
# 将带校验的数据组织成字典的形式传入
form_obj = views.MyForm({'username':'zhao','email':'125'})
# 判断数据是否合法
form_obj.is_valid() # 该方法只有在所有数据都符合要求时才会返回true
# 返回合法数据
form_obj.cleaned_data # 格式是字典
# 返回非法数据,即非法原因
form_obj.errors # 格式是字典套列表

# 内部原理
'''
先去类中获取字段名
再在传入的字典中取出对应的键的值
再把值拿去比对

所以当我们传入超出类中字段的字段个数时，form仍然只会校验类中有的字段，多传的会被忽略掉

但是不能少传数据，form默认所有字段都需要传值
'''
~~~

## 渲染标签

~~~python
# forms组件只能自动帮你渲染获取用户输入的标签
def index(request):
    # 1.先产生一个空对象
    form_obj = MyForm()
    # 2.直接将该空对象传递给html页面
    return render(request,'index.html',locals())
# 前端
{% for form in form_obj %} # 这个对象可以循环，循环的就是这个类里面的字段
	<p>	{{ form.label }} : {{ form }} </p>
{% endfor %}
# 也可以通过点的方式获取字段，{{ form_obj.username.label }}

# label属性默认时展示类中定义的字段首字母大写
~~~

## 渲染错误信息

~~~python
def index(request):
    form_obj = MyForm() # 这个名字和下面那个要一样
    if request.method == 'POST':
        # 获取用户数据并校验
        form_obj = MyForm(request.POST) # 这两个名字要一样
        # 判断数据是否合法
        if form_obj.is_valid():
            # 操作数据库
            pass      
    return render(request,'index.html',locals())

# 前端
{% for form in form_obj %}
	<p>	{{ form.label }} : {{ form }} </p>
    <span> {{ form.errors.0 }} </span>
{% endfor %}

# get请求和post请求传给html页面的对象一定要一致
~~~

## forms组件钩子函数hook

~~~python
# 在特定节点自动触发完成响应操作

# 局部钩子：当你需要给某个字段增加校验规则的时候可以使用

校验用户名中不能有123

在创建字段的类中，写钩子函数,函数名是 clean_字段名
def clean_username(self):
    # 获取用户名
    username = self.cleaned_data.get('username')
    if '123' in username:
        # 提示前端展示错误信息
        self.add_error('username','用户名不能含有123') # 第一个参数是字段名，第二个参数是错误信息
    # 将数据放回去
    return username


# 全局钩子：当你需要给多个字段增加校验规则的时候可以使用

校验输入密码和确认密码一致

def clean(self):
    password = self.cleaned_data.get('password')
    re_password = self.cleaned_data.get('re_password')
    if not password == re_password:
        self.add_error('re_password','两次密码不一致')
    # 将数据返回
    return self.cleaned_data
~~~

## forms组件其他参数及补充知识点

~~~python
# label ：字段名

# error_messages ：自定义错误信息

# initial ：默认值

# required ：控制字段是否必填

# widget ：控制input标签的type及样式
widget=forms.widgets.PasswordInput(attr={'calss':'form_control c1 c2'})
# 多个属性值直接用空格隔开

# validators ：正则校验器
validators=[
    RegexValidator(r'^[0-9]+$','请输入数字'),
    RegexValidator(r'^159[0-9]+$','必须以159开头')
]
~~~

# cookie与session

~~~python
# cookie
保存在浏览器上面的信息都可以称之为cookie
一般而言是键值对

# session
数据是保存在服务端的
一般而言也是键值对

# sesion基于cookie工作
~~~

## django的cookie操作

~~~python
# 设置cookie
# 在视图函数返回对象时，先创建一个对象
obj = HttpResponse()
obj.set_cookie(key,value)
# 获取
request.COOKIES.get(key)

# 在设置cookie的时候可以添加一个超时时间（有效时间）
obj.set_cookie(key,value,max_age=3) # 设置超时时间为3秒，expires也是设置超时时间，但是这个参数时针对ie浏览器的


# 校验是否登录的装饰器
def login_auth(func):
    def inner(request,*args,**kwargs):
        target_url = request.get_full_path()
        if request.COOKIES.get('username') == 'zhao':
           	return func(request,*args,**kwargs)
        else:
            # 将发起请求的url传递给login
            return redirect(f'/login/?next={taget_url}')
    return inner


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'zhao' and password == 'xulu':
            # 获取访问的url
            target_url = request.GET.get('next')
            if target_url:
                # 如果存在就在登陆后，跳转到那个url
                obj = redirect(target_url)
            else:
                # 如果不存在就跳转到首页
                obj = redirect('/home/')
            # 让浏览器记录cookie
            obj.set_cookie('username','zhao')
            return obj
    return render(request,'login.html')


@login_auth
def home(request):
    # 获取cookie信息
    # if request.COOKIES.get('username') == 'zhao':
        # return HttpResponse('yes')
    return redirect('/login/')

# 注销cookie
@login_auth
def logout(request):
    obj = redirect('/login/')
    obj.delete_cookie('username') # 删除cookie
    return obj
~~~

## django的session操作

~~~python
# session的数据是保存在服务端的，给客户端的是一个随机字符串
# 设置session
request.session['key'] = value
# 获取
request.session.get('key')
# 在默认情况下操作session的时候需要django默认的一张django_session表
# django默认session的过期时间是14天


def set_session(request):
    request.session['password'] = 'xulu'
    return HttpResponse('hello')

def get_session(request):
    request.session.get('password')
    return HttpResponse('world')

# 设置session内部发生的事情
1.django内部自动生成一个随机字符串
2.django内部自动将堆积字符串和对应的数据存储到django_session中
3.将产生的随机字符串返回给客户端浏览器保存

# 获取session内部发生的事情
1.自动从浏览器请求中获取sessionid对应的随机字符串
2.拿着随机字符串取django_session表中查找对应的数据
3.如果比对成功，则将对应的数据取出并以字典的形式封装到request.session
	如果比对不成功，则request.session.get返回none

# django_session表中的数据条数是取决于浏览器的，同一个计算机上同一个浏览器只会有一条数据生效（session过期的时候可能会出现多条数据，但是该现象不会持续很久，内部会自动识别）

# session设置过期时间
request.session.set_expiry()
# 括号内可以放四种类型的参数
1. 整数 秒
2. datatime/timedelta格式 到指定日期失效
3. 0 一旦浏览器窗口关闭，立刻失效
4. 不写 默认14天，全局失效时间

# 清除
request.session.delete() # 只删除服务端
request.session.flush() # 浏览器和数据库所有的数据，一般使用

# session是保存在服务端的，但是session的保存位置可以有多种
~~~

## CBV添加装饰器

~~~python
from django.views import View
from django.utils.decorators import method_decorator
# CBV中不建议直接加装饰器

# 方法二
# @method_decorator(login_auth,name='get') 前一个参数是装饰器，第二个参数是给谁加
# @method_decorator(login_auth,name='post')
class MyLogin(View):
    # 方法三
    # 给dispatch函数加，这表示这个类里面的所有方法都被这个装饰器装饰
    @method_decorator(login_auth)
    def dispatch(self,request,*args,**kwargs):
        super().dispatch(request,*args,**kwargs)
    # 方法一
    # @method_decorator(login_auth) # 括号内是装饰器的名字，直接装饰在类的方法上面
    def get(self,request):
        return HttpResponse('')
    
    def post(self,request):
        return HttpResponse('')
~~~

# Django中间件

## 中间件介绍

~~~python
# django自带七个中间件，同时支持程序源自定义中间件，并且暴露给程序员五个可以自定义的方法

# 请求来的时候，中间件的执行顺序是从上到下
# 响应走的时候，中间件的执行顺序是从下到上

# 可自定义的五个方法

process_request(self,request)
# 请求来的时候需要经过每一个中间件里面的这个方法，如果中间件没有定义这个方法，那么直接跳过这个中间件。
# 如果该方法返回了HttpResponse对象，那么请求将不再继续往后执行，而是直接原路返回。
# process_request就是用来做全局相关的所有限制功能

process_response(self,request,response)
# 响应走的时候，需要经过每一个中间件里面的process_response方法，该方法必须有两个额外的参数request,response
# 该方法必须返回一个HttpResponse对象，即传递响应对象
# 如果中间件没有这个方法，那么直接跳过这个中间件


process_view(self,request,view_name,*args,**kwargs)
# 在路由匹配成功之后，执行视图函数之前，会自动执行process_view方法


process_template_response(self,request,response)
# 返回的HttpResponse对象有render属性的时候才会触发


process_exception(self,request,exception)
# 当视图函数中出现异常的情况下触发

~~~

## 自定义中间件

~~~python
# 在项目名或者应用名下创建一个任意名称的文件夹
# 在该文件夹内创建一个任意名称的py文件
# 在该py文件内书写类（需要继承MiddlewareMixin），然后在这个类里面就可以自定义五个方法了
# 将类的路径以字符串的形式注册到配置文件中MIDDLEWARE，例如：应用名.文件夹名.py文件名.类名

from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):
    def process_request(self,request):
        pass
~~~

## csrf跨站请求伪造校验

~~~python
csrf_token 用于form表单中，作用是跨站请求伪造保护。
如果不用｛% csrf_token %｝标签，在用 form 表单时，要再次跳转页面会报403权限错误。
用了｛% csrf_token %｝标签，在 form 表单提交数据时，才会成功。

解析：
首先，向服务器发送请求，获取登录页面，此时中间件 csrf 会自动生成一个隐藏input标签，该标签里的 value 属性的值是一个随机的字符串，用户获取到登录页面的同时也获取到了这个隐藏的input标签。
然后，等用户需要用到form表单提交数据的时候，会携带这个 input 标签一起提交给中间件 csrf，原因是 form 表单提交数据时，会包括所有的 input 标签，中间件 csrf 接收到数据时，会判断，这个随机字符串是不是第一次它发给用户的那个，如果是，则数据提交成功，如果不是，则返回403权限错误。

# 网站在用户返回一个具有提交数据功能页面的时候会给这个页面加一个唯一标识
# 当这个页面朝后端发送post请求的时候，我们的后端会校验唯一标识，如果不对，直接拒绝

# 在前端的form表单内写上
{% csrf_token %}

# ajax请求
1.利用标签查找获取页面上的随机字符串
data:{'csrfmiddlewaretoken':$('[name=csrfmiddlewaretoken]').val()}
2.利用模板语法
data:{'csrfmiddlewaretoken':'{{ csrf_token }}'}
3.通用
导入js代码
~~~

## csrf相关装饰器

~~~python
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# 网站整体不校验csrf，只有几个视图函数需要校验
# 网站整体校验，只有几个不校验
@csrf_protect 需要校验
@csrf_exempt 不需要校验

# CBV
# csrf_protect三种方法都适用

# csrf_exempt只有第三种方法生效
~~~

## importlib模块，及一个重要思想

~~~python
# 用来做字符串的形式导入
importlib.import_module(res)
# 最小单位是模块名，不能继续到变量名

# __init__
import settings
import importlib

def send_all(content):
    for path_str in settings.LIST:
        module_path, class_name = path_str.rsplit('.', maxsplit=1)
        # 利用字符串导入模块
        module = importlib.import_module(module_path)
        # 利用反射获取类名
        cls = getattr(module, class_name)
        # 生成类对象
        obj = cls()
        # 利用鸭子类型直接调用send方法
        obj.send(content)
~~~

## Auth模块

~~~python
# auth_user表
# 创建管理员用户
python manage.py createsupperuser

# 依赖auth_user表完成一个登录功能
from django.contrib import auth
# 装饰器
from django.contrib.auth.decorators import login_required

def login(requset):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 如果正确返回的是一个用户对象，如果不正确返回None
        user_obj = auth.authenticate(request, username=username, password=password)
        # 判断
        if user_obj:
            # 保存用户登录状态，类似request.session[key] = user_obj
            # 只要执行了该方法，你在任何地方都可以通过request.user获取当前登录用户对象，如果没有登录则返回Anonymoususer
            auth.login(request,user_obj)
            return redirect('/home/')
    return render(request,'login.html')


@login_required(login_url='/login/') # 用户如果没有登录就跳转到login_url指定的网址
def home(request):
    request.user.is_authenticated() # 判断用户是否登录
    return

# 全局配置跳转url，settings文件中，此时login_required可以不写参数
LOGIN_URL = '/login/'

# 如果局部全局都有login_url，优先局部的

# 修改密码
@login_required
def set_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        # 校验老密码对不对
        is_right = request.user.check_password(old_password) # 自动加密对比
        if is_right:
            request.user.set_password(new_password) # 修改对象属性
            request.user.save() # 同步数据到数据库
        return redirect('/login/')
    return render(request,'set_password',locals())

# 注销功能
@login_required
def logout(request):
    auth.logout(request) # 类似于request.session.flush()
    return redirect('/login/')

# 注册功能
from django.contrib.auth.models import User # 这个就是auth_user表
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 创建普通用户
        User.object.create_user(username=username, password=password)
        
~~~

## auth_user表的扩展

~~~python
# 第一种：一对一关系表（不推荐）
from django.contrib.auth.models import User, AbstractUser
# 第二种：面向对象的继承
class UserInfo(AbstractUser):
    '''
    如果继承了AbstractUser
    那么在执行数据库迁移指令的时候auth_user表就不会再创建出来了
    而UserInfo表中会出现auto_user所有字段外加扩展字段
    前提：继承之前没有数据库迁移，继承的类里面不要覆盖AbstractUser的字段名
    需要再配置文件里面设置：AUTH_USER_MODEL = '应用名.表名'
    '''
    phone = models.BigIntegerField()
# 如果替换了表，auth的方法依然不变，并且参考的是替换的那张表
~~~

## 项目开发流程

~~~python
需求分析 项目设计 分组开发 测试 交付上线
~~~









