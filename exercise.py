from socket import *
import time

tcp = socket()
tcp.bind(('0.0.0.0', 8888))
tcp.listen(5)

# tcp.setblocking(False)
tcp.settimeout(3)

while True:
    try:
        print('waiting for connect')
        connfd, addr = tcp.accept()
        print("connect from:", addr)
    except BlockingIOError as e:
        time.sleep(2)
        with open('test.log', 'a') as f:
            msg = '%s:%s\n' % (time.ctime(), e)
            f.write(msg)                                                    
    except timeout as e:
        with open('test.log', 'a') as f:
            msg = '%s:%s\n' % (time.ctime(), e)
            f.write(msg)
    else:
        data = connfd.recv(1024).decode()
        print(data)
