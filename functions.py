# @author Heidi Cho
# On the Go
# 4.25.18
# functions.py
#
# Thie file contains helper functions for app.py.

import sys, os, random
import dbconn2
import MySQLdb

# Returns first 20 menu items from db starting at 0
def getMenu(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('select * from menu limit 20')
	results = curs.fetchall()
	return results

def addPurchase(conn, id):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO purchase (student, distributor) VALUES (%s, 1)', [id])

def addPurchaseItems(conn, pid, mid, quantity):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO purchaseItems (pid, mid, quantity) VALUES (%s,%s,%s)', [pid, mid, quantity])

def getPurchaseID(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT MAX(pid) AS LargestPid FROM purchase')
	id = curs.fetchone()
	return id

def getPurchaseItems(conn, pid):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT * from purchaseItems where pid = %s', [pid])
	results = curs.fetchall()
	return results

def getMID(conn, thing):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT mid from menu where menu.name=%s', [thing])
	id = curs.fetchone()
	return id

def getName(conn, thing):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT name from menu where mid=%s', [thing])
	id = curs.fetchone()
	return id

# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {name} nm".format(name=sys.argv[0])
    else:
        DSN = dbconn2.read_cnf()
        DSN['db'] = 'hcho5_db'     # the database we want to connect to
        dbconn2.connect(DSN)
        print lookupByNM(sys.argv[1])
