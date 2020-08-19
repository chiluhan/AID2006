from socket import *

tcp = socket()
tcp.bind(('0.0.0.0', 8888))
tcp.listen(5)

c, addr = tcp.accept()
data = c.recv(1024)
print(data.decode())

html = "HTTP/1.1 200 OK\r\n"
html += "Content-Type:text/html\r\n"
html += "\r\n"
with open('test.log') as f:
    html += f.read()
c.send(html.encode())
c.close()
tcp.close()
