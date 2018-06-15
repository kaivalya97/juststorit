import os
import json
import requests
import socket
import sock_comm
from user_file_transfer import run_threaded_server
import threading
import sys
import getip
import getpass

username = raw_input("Username: ")
password = getpass.getpass("Password: ")
masterIP = "10.20.24.43"
master_url = "http://" + masterIP + ":5005/userauth"
print master_url
headers = {'Content-Type': 'application/json'}
r = requests.post(
    master_url,
    data=json.dumps({
        "Username": username,
        "Password": password
    }),
    headers=headers)
json_data = r.text.split(':')
queue_url = "http://" + json_data[1] + ":8005/queue"
userID = json_data[2]
if (json_data[0] == "1"):
    t1 = threading.Thread(target=run_threaded_server)
    t1.setDaemon(True)
    t1.start()
    while True:
        ip = getip.getIP()
        my_request = raw_input("Enter U for Upload and D for Download: ")
        if my_request == "U":
            name = raw_input("Enter filename to upload: ")
            req = (json.dumps(
                {"Operation": my_request, "File_Name": name, "File_Path": name, "User_IP": ip, "UserID": userID}))
            print req
            r1 = requests.post(
                queue_url, data=json.dumps(req), headers=headers)
        elif my_request == "D":
            req = (json.dumps(
                {"Operation": my_request, "User_IP": ip, "UserID": userID}))
            r1 = requests.post(
                queue_url, data=json.dumps(req), headers=headers)
            received_text = sock_comm.recv()
            files_online = json.loads(received_text)
            
            i = 1
            for f in files_online:
                print str(i) + ": " + f['filename']
                i = i + 1
            d_f = raw_input("Enter the file number you want to download: ")
            name = files_online[int(d_f)-1]
            req = (json.dumps({
                "Operation": "DL",
                "File_Name": name,
                "User_IP": ip,
                "UserID": userID
            }))
        r2 = requests.post(queue_url, data=json.dumps(req), headers=headers)
else:
    print "Authentication Failed"