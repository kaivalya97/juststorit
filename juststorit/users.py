import numpy as np
import os
import json
import requests
import socket
import sock_comm
from user_file_transfer import run_threaded_server
import threading
import sys
import getip
if sys.version_info >= (3, 0):
	from tkinter import *
	from tkinter import ttk
	from tkinter.filedialog import askopenfilename
else:
	from Tkinter import *
	import ttk
	from tkFileDialog import *

my_request = {}
name = {}
size = {}
ip = {}
file_path = {}


def Login():
	global nameEL
	global pwordEL
	global rootA

	rootA = Tk()
	rootA.title('Login')

	intruction = Label(rootA, text='Login Page\n')
	intruction.grid(sticky=E)

	nameL = Label(rootA, text='Username: ')
	pwordL = Label(rootA, text='Password: ')
	nameL.grid(row=1, sticky=W)
	pwordL.grid(row=2, sticky=W)

	nameEL = Entry(rootA)
	pwordEL = Entry(rootA, show='*')
	nameEL.grid(row=1, column=1)
	pwordEL.grid(row=2, column=1)

	rmuser = Button(
		rootA, text='Sign In', fg='blue', command=FSSignin
	)  # This makes the deluser button. blah go to the deluser def.
	rmuser.grid(row=3, column=1, sticky=W)

	rootA.mainloop()


def Upload_Download():

	global rootB

	rootB = Tk()
	rootB.title('Upload OR Download')

	intruction = Label(rootB, text='Do you want to Upload or Download ?\n')
	intruction.grid(sticky=E)

	rmuser = Button(
		rootB, text='Upload', fg='blue', command=Upload
	)
	rmuser.grid(row=1, column=1, sticky=W)

	rmuser1 = Button(
		rootB, text='Download', fg='red', command=Download
	)
	rmuser1.grid(row=1, column=2, sticky=W)

	rootB.mainloop()


def File():

	global rootC

	rootC = Tk()
	rootC.title('File Path')

	intruction = Label(rootC, text='Path of file you want to Upload\n')
	intruction.grid(sticky=E)

	rmuser = Button(rootC, text='Upload', fg='blue', command=File_path)
	rmuser.grid(row=1, column=1, sticky=W)

	rootC.mainloop()


def File_path():
	global name
	global size
	global ip
	global file_path
	nme = askopenfilename(
		initialdir="./tkinter/",
		filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
		title="Choose a file.")

	try:
		with open(nme, 'r') as UseFile:
			file_path = nme
			name = os.path.basename(nme)
			size = os.path.getsize(nme) / (1024 * 1024), "MB"
			# ip = socket.gethostbyname(socket.gethostname())
			ip = getip.getIP()


# ip = ni.ifaddresses('wlp5s0')[ni.AF_INET][0]['addr']

	except:
		print("No file exists")

	rootC.destroy()


def Upload():
	global my_request
	print("Upload your File")
	my_request = 'U'
	rootB.destroy()
	rootB.quit()


def Download():
	global my_request
	print("Download your File")
	my_request = 'D'
	rootB.destroy()
	rootB.quit()

def file_download_list(headers,queue_url,ip,userID,files_online,fileEL,rootZ):
	ddf = fileEL.get()
	print ddf
				
	#d_f = input("Enter the file number you want to download")
	d_f = ddf
	name = files_online[int(d_f)-1]
	req = (json.dumps({
		"Operation": "DL",
		"File_Name": name,
		"User_IP": ip,
		"UserID": userID
	}))
	r2 = requests.post(queue_url, data=json.dumps(req), headers=headers)
	rootZ.destroy()
	rootZ.quit()

def FSSignin():
	global my_request
	global name
	global fileEL
	global rootZ
				
	Log = nameEL.get()
	Psd = pwordEL.get()
	masterIP = "10.20.24.43"
	master_url = "http://" + masterIP + ":5005/userauth"
	print master_url
	headers = {'Content-Type': 'application/json'}
	r = requests.post(
		master_url,
		data=json.dumps({
			"Username": Log,
			"Password": Psd
		}),
		headers=headers)
	json_data = r.text.split(':')
	queue_url = "http://" + json_data[1] + ":8005/queue"
	userID = json_data[2]
	# print queue_url
	# print userID
	rootA.destroy()
	if (json_data[0] == "1"):
		t1 = threading.Thread(target=run_threaded_server)
		t1.setDaemon(True)
		t1.start()
		while True:
			Upload_Download()
			print my_request
			if my_request=="U":
				File()
				req = (json.dumps({
					"Operation": my_request,
					"File_Name": name,
					"File_Path": file_path,
					"File_Size": size,
					"User_IP": ip,
					"UserID": userID
				}))
				print req

				r1 = requests.post(
					queue_url, data=json.dumps(req), headers=headers)
			elif my_request == "D":
				req = (json.dumps({
					"Operation": my_request,
					"User_IP": getip.getIP(),
					"UserID": userID
				}))
				print req
				r1 = requests.post(
					queue_url, data=json.dumps(req), headers=headers)
				received_text = sock_comm.recv()
				files_online = json.loads(received_text)
				i = 1
				files = ""
				for f in files_online:
					print str(i) + ": "+f['filename']
					files += str(i) + ": "+f['filename'] + "\n"
					i = i + 1
				
				#file_str = ''.join(files)
				
				rootZ = Tk()
				rootZ.title('Your Files')

				var = StringVar()
				var.set(files)

				intruction = Label(rootZ, text=files, anchor='w')
				intruction.grid(sticky=E)

				fileL = Label(rootZ, text='Enter file no. you want to download: ')
				fileL.grid(row=1, sticky=W)
				

				fileEL = Entry(rootZ)
				fileEL.grid(row=1, column=1)
				

				rmuser = Button(
					rootZ, text='Submit', fg='blue',command= lambda:file_download_list(\
					headers,queue_url,getip.getIP(),userID,files_online,fileEL,rootZ))  # This makes the deluser button. blah go to the deluser def.
				rmuser.grid(row=2, column=1, sticky=W)
				rootZ.mainloop()
				#rootZ.destroy()
				#rootZ.quit()
				"""
				ddf = fileEL.get()
				print ddf
				
				#d_f = input("Enter the file number you want to download")
				d_f = ddf
				name = files_online[int(d_f)-1]
				req = (json.dumps({
				"Operation": "DL",
				"File_Name": name,
				"User_IP": getip.getIP(),
				"UserID": userID
			}))
				r2 = requests.post(queue_url, data=json.dumps(req), headers=headers)
			"""
	else:
		print "Authentication Failed"
	# print(json.dumps({"Username": Log, "Password": Psd}))'''
	rootA.quit()


# Flow-
# 0. Prompt upload download (op)
# my_request['op']=op
# 1. File Selection Window (return file path)
# my_request['file']=file

# Functions to perform
Login()
