"""
web server 程序
完成一个类，提供给使用者，让使用者
可以快速搭建web服务，，展示自己的网页
"""
from socket import *
import re
from select import select


# 1.搭建服务 2. 实现http功能
class WebServer:
    def __init__(self, host='0.0.0.0', port=88, html=None):
        self.host = host
        self.port = port
        self.html = html  # 网页的根目录
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 搭建服务的准备操作
        self.creat_socket()
        self.bind()

    def creat_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    # 启动服务器开始监听客户端连接
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        # 循环监控IO
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for i in rs:
                if i is self.sock:
                    connfd, addr = i.accept()
                    print('Connect from:', addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # 收到http请求
                    try:
                        self.handle(i)
                    except:
                        i.close()
                        self.rlist.remove(i)

    def handle(self, connfd):
        # 接收浏览器请求
        request = connfd.recv(1024 * 10).decode()
        # 解析请求 -->获取请求内容
        pattern = "[A-Z]+\s(?P<info>/\S*)"
        result = re.match(pattern, request)
        if result:
            # 匹配到内容 --> 请求内容
            info = result.group('info')
            print("请求内容：", info)
            self.send_html(connfd, info)  # 发送数据
        else:
            # 没有匹配到，任务客户端断开
            connfd.close()
            self.rlist.remove(connfd)
            return

    # 根据请求发送响应数据
    def send_html(self, connfd, info):
        # info --> 请求 主页 否则具体请求内容
        if info == '/':
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        try:
            # 考虑到传送的文件可能是图片
            f = open(filename, 'rb')
        except:
            # 文件不存在
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...<\h1>"
            response = response.encode()
        else:
            data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data

        finally:
            # 发送响应到客户端
            connfd.send(response)


if __name__ == '__main__':
    # 实例化对象
    httpd = WebServer(host='0.0.0.0', port=8000, html='./static')
    # 对象启动服务
    httpd.start()
