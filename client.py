import socket

s = socket.socket()
host = socket.gethostname()
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
while True:
	s.send(b'Hello, World!')
	data = s.recv(1024)
	print('received',data)
s.close()