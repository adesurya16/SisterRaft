import socket

s = socket.socket()
host = socket.gethostname()
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
c,addr = s.accept()
print('Got Connection')
print(addr)
while True:
	data = c.recv(1024)
	if not data:
		break
	print(data)
	c.send(data)
c.close()