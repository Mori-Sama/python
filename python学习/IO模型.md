# IO模型

### 阻塞IO

在服务端开设多进程多线程，本质上没有解决IO问题，该等的地方还是需要等，只不过多个人的等待彼此互补干扰

使用recv的默认参数一直等数据直到拷贝到用户空间，这段时间内进程始终阻塞。A同学用杯子装水，打开水龙头装满水然后离开。这一过程就可以看成是使用了阻塞IO模型，因为如果水龙头没有水，他也要等到有水并装满杯子才能离开去做别的事情。很显然，这种IO模型是同步的。

![阻塞IO](C:\Users\Zhao\Desktop\图\阻塞IO.png)

### 非阻塞IO

改变flags，让recv不管有没有获取到数据都返回，如果没有数据那么一段时间后再调用recv看看，如此循环。B同学也用杯子装水，打开水龙头后发现没有水，它离开了，过一会他又拿着杯子来看看……在中间离开的这些时间里，B同学离开了装水现场(回到用户进程空间)，可以做他自己的事情。这就是非阻塞IO模型。但是它只有是检查无数据的时候是非阻塞的，在数据到达的时候依然要等待复制数据到用户空间(等着水将水杯装满)，因此它还是同步IO。

![非阻塞IO](C:\Users\Zhao\Desktop\图\非阻塞IO.png)

~~~python
'''服务端'''
import socket

server = socket.socket()
server.bind(('127.0.0.1',9000))
server.listen()

# 设置将所有的网络阻塞变为非阻塞
server.setblocking(False)
r_list = []
del_list = []
while 1:
    try:
        conn, addr = server.accept()
        r_list.append(conn)
    except BlockingIOError:
        for conn in r_list:
            try:
                msg = conn.recv(1024)
                if len(msg) == 0:  # 客户端断开连接
                    conn.close()  # 关闭连接
                    del_list.append(conn)
                conn.send(msg.upper())
            except BlockingIOError:
                continue
            except ConnectionResetError:  # 客户端非正常关闭
                conn.close()
                del_list.append(conn)
        # 清除无用连接
        for conn in del_list:
            r_list.remove(conn)
        del_list.clear()

# 该模型会长时间占用cpu资源，并且大部分时间cpu都在空转，实际应用中不考虑非阻塞IO模型
~~~

### IO复用模型

这里在调用recv前先调用select或者poll，这2个系统调用都可以在内核准备好数据(网络数据到达内核)时告知用户进程，这个时候再调用recv一定是有数据的。因此这一过程中它是阻塞于select或poll，而没有阻塞于recv，有人将非阻塞IO定义成在读写操作时没有阻塞于系统调用的IO操作(不包括数据从内核复制到用户空间时的阻塞，因为这相对于网络IO来说确实很短暂)，如果按这样理解，这种IO模型也能称之为非阻塞IO模型，但是按POSIX来看，它也是同步IO，那么也和楼上一样称之为同步非阻塞IO吧。

这种IO模型比较特别，分个段。因为它能同时监听多个文件描述符(fd)。这个时候C同学来装水，发现有一排水龙头，舍管阿姨告诉他这些水龙头都还没有水，等有水了告诉他。于是等啊等(select调用中)，过了一会阿姨告诉他有水了，但不知道是哪个水龙头有水，自己看吧。于是C同学一个个打开，往杯子里装水(recv)。这里再顺便说说鼎鼎大名的epoll(高性能的代名词啊)，epoll也属于IO复用模型，主要区别在于舍管阿姨会告诉C同学哪几个水龙头有水了，不需要一个个打开看(当然还有其它区别)。

![IO复用模型](C:\Users\Zhao\Desktop\图\IO复用模型.png)

~~~python
# 操作系统提供一个监管机制，帮忙监控socket对象和conn对象，并且可以监管多个，只要有人触发了立即返回可执行对象
# 当监管的对象只有一个的时候，其效率比阻塞IO效率还低
'''服务端'''
import socket
import select


server = socket.socket()
server.bind(('127.0.0.1',9000))
server.listen()
server.setblocking(False)
# 检测server对象
read_list = [server]
while 1:
    r_list, w_list, x_list = select.select(read_list,[],[])
    for i in r_list:
        # 针对不同的对象做不同的处理
        if i is server:
            conn, addr = i.accept()
            read_list.append(conn)
        else:
            res = i.recv(1024)
            if len(res) == 0:
                i.close()
                read_list.remove(i)
            print(res)
            i.send(b'hello')

            
'''
监管机制
select机制：windows和linux都有
poll机制：linux有，并且监管数量比select多
当监管的对象特别多的时候，以上两个机制会出现极大的延迟

epoll机制：linux有，它给每一个监管对象都绑定了一个回调机制，一旦有响应，回调机制立即发起提醒
'''
# 针对不同平台的监管机制
# selectors模块，自动选择
~~~

### 异步IO

调用aio_read，让内核等数据准备好，并且复制到用户进程空间后执行事先指定好的函数。E同学让舍管阿姨将杯子装满水后通知他。整个过程E同学都可以做别的事情(没有recv)，这才是真正的异步IO。

![异步IO](C:\Users\Zhao\Desktop\图\异步IO.png)

~~~python
# 异步IO模型是所有模型效率最高的，也是应运最广泛的
# 模块：asyncio模块
# 异步框架：sanic tronado twistedS
~~~

