import socket
from flask import Flask, request, jsonify
import crud
import time
import threading

app = Flask(__name__)


def heartbeat():
	host = ''
	port = 65525
	backlog = 5
	size = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(backlog)
	while True:
		client, address = s.accept()
		data = client.recv(size)
		start = int(time.time())
		if data == 'init':
			print 'Storage Node: ' + address[0] + ' INITIATED CONNECTION.'
			crud.insertTable(address[0], 'nodestatus', '1')
			crud.insertTable(address[0], 'heartbeat', start)
		else:
			crud.updateRow('heartbeat', 'time', start, 'node', address[0])
		client.close()


@app.route('/userauth', methods=["POST"])
def userauth():
	if request.method == 'POST':
		jsonRes = request.get_json()
		username = jsonRes['Username']
		password = jsonRes['Password']
		dbpass = crud.auth(username)[0]
		if dbpass['password']==password:
			return "1:" + queueIP+":"+str(dbpass['id'])
	return str(0)


if __name__ == "__main__":
	queueIP = "10.20.24.90"
	t1 = threading.Thread(target=heartbeat)
	t1.setDaemon(True)
	t1.start()
	app.run(host='0.0.0.0', port=5005, debug=True, threaded=True)