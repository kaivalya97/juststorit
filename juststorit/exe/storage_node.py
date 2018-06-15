import socket
import threading
import SocketServer
import os
import time


BUFFER_SIZE = 1024
PORT1 = 8000
PORT2 = 8001


host = '10.20.24.43'
master_port = 65525
size = 1024
conn = False

# For upload (Storage Node will upload)
class ThreadedTCPRequestHandler1(SocketServer.BaseRequestHandler):

	def handle(self):
		filename = self.request.recv(BUFFER_SIZE)
		#print filename
		if os.path.isfile(filename):
			self.request.send("ok")
			response = self.request.recv(BUFFER_SIZE)
			with open(filename, 'rb') as f:
				print 'file opened',filename
				l = f.read(BUFFER_SIZE)
				while l:
					#print "Sending: %s" %(l)
					self.request.send(l)
					#print('Sent ',repr(l))
					l = f.read(BUFFER_SIZE)
				print "file close()",filename
				f.close()
		else:
			self.request.send("error: file not found")
			response = self.request.recv(BUFFER_SIZE)
		"""
		cur_thread = threading.current_thread()
		response = "{}: {}".format(cur_thread.name, data)
		self.request.sendall(response)
		"""

# For download (Storage Node will download)
class ThreadedTCPRequestHandler2(SocketServer.BaseRequestHandler):

	def handle(self):
		filename = self.request.recv(BUFFER_SIZE)
		print filename
		self.request.send("ok")

		cur_thread = threading.current_thread()
		response = "{}: {}".format(cur_thread.name, filename)

		file = filename
		count = 1
		while os.path.isfile(file):
			file = filename[:-len(filename.split('.')[-1])-1] + " (" + str(count) + ")." + filename.split('.')[-1]
			count += 1
		with open(file, 'wb') as f:
			print 'file opened',file
			while True:
				#print('receiving data...')
				data = self.request.recv(BUFFER_SIZE)
				if not data:
					f.close()
					self.request.close()
					print 'file close()',file
					break
				# write data to a file
				f.write(data)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	SocketServer.TCPServer.allow_reuse_address = True

# for - client upload (client will upload)
def send_file(ip, filename):
	global PORT2
	port = PORT2
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
def recv_file(ip, filename):
	global PORT1
	port = PORT1
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

def run_threaded_server():
	global PORT1, PORT2
	# Port 0 means to select an arbitrary unused port
	HOST = "0.0.0.0" # storage node

	server1 = ThreadedTCPServer((HOST, PORT1), ThreadedTCPRequestHandler1)
	server2 = ThreadedTCPServer((HOST, PORT2), ThreadedTCPRequestHandler2)

	# important so that after program exits, it can be used
	server1.allow_reuse_address = True
	server2.allow_reuse_address = True

	ip1, port1 = server1.server_address
	ip2, port2 = server2.server_address
	
	# ip1 and ip2 are same

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread1 = threading.Thread(target=server1.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread1.daemon = True
	server_thread1.start()
	print "Server loop running in thread:", server_thread1.name

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread2 = threading.Thread(target=server2.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread2.daemon = True
	server_thread2.start()
	print "Server loop running in thread:", server_thread2.name

	#send_file(ip1, "abc.txt")
	#recv_file(ip2, "worker_client.py")
	#send_file(ip1, "maitrey_server.py")
	try:
		while True:
			pass
	finally:
		server1.shutdown()
		server1.server_close()
		server2.shutdown()
		server2.server_close()

def heartbeat():
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

if __name__ == "__main__":
	t1 = threading.Thread(target=heartbeat)
	t1.setDaemon(True)
	t1.start()
	run_threaded_server()
	print 'Done'
	