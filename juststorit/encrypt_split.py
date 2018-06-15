from hashlib import md5, sha512
from Crypto.Cipher import AES
from Crypto import Random
import os
import json
import math
import ntpath
import base64
import shutil


def splitFile(inputFile, dir_name):
    f = open(inputFile, 'rb')
    data = f.read()
    f.close()

    size_in_bytes = len(data)
    digits = int(math.log10(size_in_bytes))
    chunkSize = int(math.pow(10, digits))

    noOfChunks = size_in_bytes / chunkSize
    if (size_in_bytes % chunkSize):
        noOfChunks += 1

    file_name = ntpath.basename(inputFile)
    count = 0
    for i in range(0, size_in_bytes + 1, chunkSize):
        fl = file_name + "_shard_%s" % count
        fl_name = dir_name + '/' + base64.b64encode(fl)
        f = open(fl_name, 'wb')
        f.write(data[i:i + chunkSize])
        f.close()
        count += 1


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]


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


def encrypt_split(filename):
    #filename = 'Wildlife.wmv'
    in_filename = filename  #give the name with path if not in same dir
    if not os.path.isdir("shards"):
        os.makedirs('shards')
    out_filename = 'shards/' + filename
    with open(in_filename, 'rb') as in_file, open(out_filename,'wb') as out_file:
        encrypt(
            in_file, out_file,
            '5es1rj/IYk=4iHJj&tjbh;3V<Ok&eQ)tV~DZ%2Q^R uoSetUL}?KetH]KLuJd>6L')
    splitFile(out_filename, 'shards')
    os.remove(out_filename)
    '''
	#execute it after sending shards to storage nodes
	if os.path.isdir('shards'):
		shutil.rmtree('shards')
	'''
