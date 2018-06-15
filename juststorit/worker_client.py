import socket
import os

BUFFER_SIZE = 1024

# for - client upload (client will upload)
def send_file(ip, filename, port):
	if os.path.isfile(filename):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
		try:
			#sock.sendall(message)
			# remove any parent local folder paths of the file for server folder
			file = filename.split('/')[-1]
			sock.send(file)
			response = sock.recv(BUFFER_SIZE)
			with open(filename, 'rb') as f:
				print 'file opened',filename
				l = f.read(BUFFER_SIZE)
				while l:
					#print "Sending: %s" %(l)
					sock.send(l)
					#print('Sent ',repr(l))
					l = f.read(BUFFER_SIZE)
				f.close()
			#print "Received: {}".format(response)
			print "Received: ",response
		finally:
			print "file close()",filename
			sock.close()
	else:
		print "Error: File",filename,"not found"

# for - client download (client will download)
def recv_file(ip, filename, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	try:
		#sock.sendall(message)
		sock.send(filename)
		response = sock.recv(BUFFER_SIZE)
		#print "Received: {}".format(response)
		print "Response: ",response
		if response == "ok":
			sock.send("ack")
			# remove any parent server paths of file for local folder
			filename = filename.split('/')[-1]
			file = filename
			count = 1

			# handle copies in local folder of terminal path
			while os.path.isfile(file):
				file = filename[:-len(filename.split('.')[-1])-1] + " (" + str(count) + ")." + filename.split('.')[-1]
				count += 1
			with open(file, 'wb') as f:
				print 'file opened',file
				while True:
					#print('receiving data...')
					data = sock.recv(BUFFER_SIZE)
					if not data:
						print 'file close()',file
						break
					# write data to a file
					f.write(data)
	finally:
		f.close()
		sock.close()


"""
if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port

	ip1, port1 = '0.0.0.0', 8000
	ip2, port2 = '0.0.0.0', 8001
	
	ip = ip1	
	# ip1 and ip2 are same

	send_file(ip1, "abc.txt")
	recv_file(ip2, "worker_client.py")
	send_file(ip1, "maitrey_server.py")
"""
