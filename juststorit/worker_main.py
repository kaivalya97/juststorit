from flask import Flask, request, jsonify
import requests.exceptions
from encrypt_split import encrypt_split
from decrypt_merge import decrypt_merge
from sn_up import sn_up
import crud
import os
import random
from worker_client import send_file,recv_file
import json
import sock_comm
# worker - send - user - 8003
# worker - recv - user - 8002
# worker - send - storjnode - 8001
# worker - recv - storjnode - 8000
PORT_send_user = 8003
PORT_recv_user = 8002
PORT_send_sn = 8001
PORT_recv_sn = 8000

def poll_queue():
	queueIP = "10.20.24.90"
	queue = "http://" + queueIP + ":8005/queuepop"
	headers = {'Content-Type': 'application/json'}
	return requests.get(queue, headers=headers)


def get_shards(filename, uid):
	shards = crud.get_shard_sn_list(filename, uid)
	noofshards = len(shards)
	for i in range(0, noofshards):
		sn_ip = shards[i]['storage_id']  ###Get storage node IP for each shard
		shard_name = shards[i]['shard_id']  ###Get shard name
		shard_name = shard_name
		recv_file(sn_ip, shard_name, PORT_recv_sn)
	filename = filename['filename']
	print filename
	decrypt_merge(filename,noofshards)
	for i in range(0, noofshards):
		os.remove(shards[i]['shard_id'])

while (1):
	req = poll_queue()
	while (req.text == '101'):
		req = poll_queue()
	print req.text
	req = req.json()
	my_request = req['Operation']
	ip = req['User_IP']
	uid = req['UserID']

	if my_request == "U":
		name = req['File_Name']
		file_path = req['File_Path']
		recv_file(ip, file_path, PORT_recv_user)
		response = crud.insertFiledetails(uid, name)
		file_id = response
		encrypt_split(name)
		sn = sn_up()
		noofsn = len(sn)
		for shard in os.listdir("shards"):
			print shard
			file_shard = 'shards/'+shard
			sn_ip = sn[random.randint(0, noofsn-1)]
			send_file(sn_ip, file_shard, PORT_send_sn)
			crud.insertSharddetails('shard', file_id, shard, sn_ip)
			os.remove('shards/'+shard)
		os.remove(name)
	elif my_request == "D":
		file_list = crud.list_files(uid)
		sock_comm.send(ip,json.dumps(file_list))
		#send list to user. {fid:filename}
		
	elif my_request == "DL":
		name = req['File_Name']
		get_shards(name, uid)
		send_file(ip, name['filename'], PORT_send_user)
		os.remove(name['filename'])

	elif my_request == "l":
		crud.list_files(uid)