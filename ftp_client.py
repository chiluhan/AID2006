"""
ftp 客户端
"""
from socket import *
import time,sys

# 服务器地址
ADDR = ('127.0.0.1', 8888)
FTP = '/home/tarena/桌面/FTP/'


# 具体的请求方法
class FTPClient:
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):
        self.sock.send(b'LIST')
        result = self.sock.recv(128)
        if result == b'OK':
            files = self.sock.recv(1024 * 1024)
            print(files.decode())

        else:
            print('文件库为空')

    def do_put(self, filename):
        try:
            f = open(filename, 'rb')
        except:
            print('要上传的文件不存在')
            return
        filename = filename.split('/')[-1]
        data = 'PUT ' + filename
        self.sock.send(data.encode())
        result = self.sock.recv(128)
        if result == b'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sock.send(b'##')
                    break
                self.sock.send(data)
            f.close()
        else:
            print('该文件已存在')

    def do_get(self, filename):
        data = 'GET ' + filename
        self.sock.send(data.encode())
        result = self.sock.recv(128)
        if result == b'OK':
            f = open(FTP + filename, 'wb')
            while True:
                data = self.sock.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print('该文件不存在')

    def do_exit(self):
        self.sock.send(b'EXIT')
        self.sock.close()
        sys.exit('谢谢使用')


# 网络连接启动程序
def main():
    sock = socket()
    sock.connect(ADDR)  # 建立网络连接

    # 通过对象调用类中具体方法完成请求
    ftp = FTPClient(sock)

    # 循环输入命令
    while True:
        print("""
        ========== 命令选项 ===========
                    list
                  get file
                  put file
                    exit
        ==============================
        """)
        cmd = input("命令:")
        if cmd == 'list':
            ftp.do_list()
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd == 'exit':
            ftp.do_exit()
        else:
            print('请输入正确指令')


if __name__ == '__main__':
    main()
