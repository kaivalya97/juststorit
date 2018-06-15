from hashlib import md5,sha512
from Crypto.Cipher import AES
from Crypto import Random
import os
import json
import math
import ntpath
import base64
import shutil

def joinFiles(fileName,noOfChunks,dir_in,dir_out):
	dataList = []
	count = 0
	for i in range(0,noOfChunks,1):
		fl = fileName+"_shard_"+ str(count)
		chunkName = base64.b64encode(fl)
		f = open(chunkName, 'rb')
		dataList.append(f.read())
		f.close()
		count+=1
	f = open(dir_out+'/'+fileName, 'wb')
	for data in dataList:
		f.write(data)
	f.close()

def derive_key_and_iv(password, salt, key_length, iv_length):
	d = d_i = ''
	while len(d) < key_length + iv_length:
		d_i = md5(d_i + password + salt).digest()
		d += d_i
	return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
	bs = AES.block_size
	salt = Random.new().read(bs - len('Salted__'))
	key, iv = derive_key_and_iv(password, salt, key_length, bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	out_file.write('Salted__' + salt)
	finished = False
	while not finished:
		chunk = in_file.read(1024 * bs)
		if len(chunk) == 0 or len(chunk) % bs != 0:
			padding_length = (bs - len(chunk) % bs) or bs
			chunk += padding_length * chr(padding_length)
			finished = True
		out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
	bs = AES.block_size
	salt = in_file.read(bs)[len('Salted__'):]
	key, iv = derive_key_and_iv(password, salt, key_length, bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	next_chunk = ''
	finished = False
	while not finished:
		chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
		if len(next_chunk) == 0:
			padding_length = ord(chunk[-1])
			chunk = chunk[:-padding_length]
			finished = True
		out_file.write(chunk)

def decrypt_merge(filename,noOfChunks):
	#file = 'Wildlife.wmv'
	if not os.path.isdir("merge"):
		os.makedirs('merge')
	joinFiles(filename,noOfChunks,'','merge')
	in_filename = 'merge/'+filename
	out_filename = filename
	print out_filename
	with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
		decrypt(in_file, out_file, '5es1rj/IYk=4iHJj&tjbh;3V<Ok&eQ)tV~DZ%2Q^R uoSetUL}?KetH]KLuJd>6L')
	if os.path.isdir('merge'):
		shutil.rmtree('merge')
	if os.path.isdir('shards'):
		shutil.rmtree('shards')

