import crud
import json

def sn_up():
	nodes=crud.selectFromTable('node','nodestatus','status','1')
	ip_list=[]
	for i in nodes:
		ip_list.append(i['node'])
	return ip_list
