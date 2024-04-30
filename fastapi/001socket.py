import socket


sock = socket.socket()

sock.bind(('127.0.0.1',8383))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)
    print('浏览器发送的请求',data)
    conn.send(b'hello mark')
    conn.close()