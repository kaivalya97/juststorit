import socket
import time
import smtplib

host = '10.20.24.43'
master_port = 65525
size = 1024
conn = False
while not conn:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,master_port))
		s.send("init")
		conn = True
		time.sleep (3)
	except:
		print ('Error Server offline')
		conn = False
while (conn):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,master_port))
		s.send("1")
		time.sleep (3)
	except:
		print ('Error Server offline')
		time.sleep (3)