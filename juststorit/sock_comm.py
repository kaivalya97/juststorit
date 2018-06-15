import socket

comm_port = 65520
size = 1024

def send(host,text):
	comm_port = 65520
	size = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,comm_port))
	s.sendall(text)
	s.close()

def recv():
	host = ''
	comm_port = 65520
	backlog = 5
	size = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, comm_port))
	s.listen(backlog)
	while True:
		client, address = s.accept()
		data = client.recv(size)
		s.close()
		return data

	
