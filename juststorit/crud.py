import MySQLdb as mdb
import sys
global con
duplicate = False


def insertTable(host, table, val):
	# print 'crud: '+host
	with con:
		cur = con.cursor()
		try:
			cur.execute("INSERT INTO {0} VALUES ('{1}','{2}')".format(
				table, str(host), val))
		except:
			# print 'Storage Node: '+host+' LIVE'
			duplicate = True


def insertSharddetails(table, val1, val2, val3):
	# print 'crud: '+host
	with con:
		cur = con.cursor()
		try:
			cur.execute("INSERT INTO {0} VALUES ('{1}','{2}','{3}')".format(
				table, val1, val2, val3))
		except:
			# print 'Storage Node: '+host+' LIVE'
			duplicate = True


def list_files(userID):
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute(
			"SELECT filename FROM files WHERE uid='{0}'".format(userID))
		file_list = cur.fetchall()
		return file_list


def get_shard_sn_list(filename, uid):
	with con:
		filename = filename['filename']
		cur = con.cursor(mdb.cursors.DictCursor)
		sn_list = cur.execute(
			"SELECT shard.shard_id, shard.storage_id FROM shard, files WHERE shard.fid=files.fid and files.uid={0} and files.filename='{1}'".format(uid, filename))
		shard_list = cur.fetchall()
		return shard_list


def insertFiledetails(val1, val2):
	# print 'crud: '+host
	with con:
		cur = con.cursor()
		try:
			cur.execute(
				"insert into files (uid,filename) values ({0},'{1}')".format(val1, val2))
			cur.execute(
				"SELECT fid from files where filename='{1}' and uid='{0}'".format(val1, val2))
			f_id = cur.fetchall()
			return f_id[0][0]
		except:
			# print 'Storage Node: '+host+' LIVE'
			duplicate = True

# RETRIEVE TABLE ROWS


def retrieveTable(table):
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM {0}".format(table))
		rows = cur.fetchall()
		return rows


def auth(username):
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT {0} FROM {1} where {2}='{3}'".format(
			'password,id', 'users', 'username', username))
		rows = cur.fetchall()
		return rows


# UPDATE ROW
def updateRow(table, var, val, condition, equatingVal):
	with con:
		cur = con.cursor()
		cur.execute("UPDATE {0} SET {1} = '{2}' WHERE {3} = '{4}'".format(
			table, var, val, condition, equatingVal))


# SELECT TABLE ROWS
def selectFromTable(selection, table, condition, equatingVal):
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT {0} FROM {1} WHERE {2}={3}".format(
			selection, table, condition, equatingVal))
		rows = cur.fetchall()
		return rows


# DELETE ROW
def deleteRow(status):
	with con:

		cur = con.cursor()
		cur.execute(
			"DELETE FROM heartbeat WHERE status = '{0}'".format(status))
		print "Number of rows deleted:", cur.rowcount


# SET UP THE CONNECTION
try:
	con = mdb.connect('10.20.24.17', 'storj', 'root', 'cc')

	cur = con.cursor()
	cur.execute("SELECT VERSION()")

	ver = cur.fetchone()

	# print "Database version : %s " % ver

	# CRUD OPERATIONS
	# createTable(con)
	# insertTable("10.20.24.900",'heartbeat')
	'''retrieveTable(con)
	updateRow(con,"10.20.24.43","0")
	deleteRow(con,"0")'''

except mdb.Error, e:

	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)

finally:
	if con:
		print 'Connected to db'
		# con.close()
