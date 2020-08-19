"""
select 方法示例
"""
from select import select
from socket import *

f = open('test.log')
sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(5)

udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(('0.0.0.0', 9999))
print('开始监控IO')
rs, ws, xs = select([udp], [], [])
print('rlist:', rs)
print('wlist:', ws)
print('xlist:', xs)
