"""
基于select方法的IO多路复用网络并发
重点代码！！！
"""

from socket import *
from select import select

# 创建好监听套接字
sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(5)

# 与非阻塞IO防止传输过程中阻塞
sockfd.setblocking(False)

# 准备IO进行监控
rlist = [sockfd]
wlist = []
xlist = []

# 循环监控IO发送
while True:
    rs, ws, xs = select(rlist, wlist, xlist)
    # 伴随监控的IO的增多,就绪的IO情况也会复杂
    # 分类讨论 分两类 sockfd-->connfd
    for i in rs:
        if i is sockfd:
            connfd, addr = i.accept()
            print('Connect from:', addr)
            connfd.setblocking(False)
            rlist.append(connfd)  # 添加监控
        else:
            # 某个客户端发消息了
            data = i.recv(1024).decode()
            if not data:
                # 客户端退出
                rlist.remove(i)  # 删除监控
                i.close()
                continue
            print('收到了：', data)
            # i.send(b'OK')
            wlist.append(i)

    for w in wlist:
        w.send(b'OK')
        wlist.remove(w)  # 如果不移除就会一直循环发送
