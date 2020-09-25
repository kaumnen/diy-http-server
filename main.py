import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1244))
s.listen(1)

while True:
    clientsocket, address = s.accept()
    print(f'Connection from {address} has been established!')
    clientsocket.send(bytes('Welcome to the server!', 'utf-8'))
