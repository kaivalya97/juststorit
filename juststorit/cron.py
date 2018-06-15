import crud
import time

nodes = crud.retrieveTable('heartbeat')
start = int(time.time())

for node in nodes:
	if start-int(node['time']) > 10:
		print node['node']+' OFFLINE: '+str((start - int(node['time'])))
		crud.updateRow('nodestatus','status','0','node',node['node'])
	else:
		print node['node']+' ONLINE: '+str((start - int(node['time'])))
		crud.updateRow('nodestatus','status','1','node',node['node'])
