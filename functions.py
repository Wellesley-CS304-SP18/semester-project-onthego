# @author Heidi Cho
# On the Go
# 4.25.18
# functions.py
#
# Thie file contains helper functions for app.py.

import sys, os, random
import dbconn2
import MySQLdb

# Get list of distributors
def getDistributors(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM distributor')
	orgs = curs.fetchall()
	return orgs

# Returns first 20 menu items from db starting at 0
def getMenu(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('select * from menu limit 20')
	results = curs.fetchall()
	return results

# Returns the name of a distributor after lookup by id
def getOrg(adminID, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name FROM distributor WHERE (did = %s)',[adminID])
	org = curs.fetchone()
	return org

# Returns all active orders
def getActiveOrders(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from purchaseItems INNER JOIN purchase on (purchaseItems.pid = purchase.pid) WHERE purchase.distributor = 1 and purchase.complete is NULL')
	orders = curs.fetchall()
	return orders

# Returns all active orders made by a student
def getUsersOrders(conn, bnum):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from purchaseItems INNER JOIN purchase on (purchaseItems.pid = purchase.pid) WHERE purchase.student = %s and purchase.complete is NULL', [bnum])
	orders = curs.fetchall()
	return orders

# Returns all active orders for a given distributor (lookup by id)
def markAsComplete(conn, pid):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('UPDATE purchase SET complete = 1 WHERE pid = %s',[pid])
	return

# Creates a new order
def addPurchase(conn, id, notes):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO purchase (student, distributor, dt, notes) VALUES (%s, 1, now(), %s)', [id, notes])

# adds the items of an order into the database
def addPurchaseItems(conn, pid, mid, quantity):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO purchaseItems (pid, mid, quantity) VALUES (%s,%s,%s)', [pid, mid, quantity])

# gets the order ID
def getPurchaseID(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT MAX(pid) AS LargestPid FROM purchase')
	id = curs.fetchone()
	return id

# gets the items the user ordered
def getPurchaseItems(conn, pid):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT * from purchaseItems where pid = %s', [pid])
	results = curs.fetchall()
	return results

# gets the id of a menu item using its name
def getMID(conn, name):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT mid from menu where menu.name=%s', [name])
	id = curs.fetchone()
	return id

# gets the name of a menu item using its mid
def getName(conn, mid):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT name from menu where mid=%s', [mid])
	name = curs.fetchone()
	return name

# gets the price of a menu item using its name
def getPrice(conn, name):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT price from menu where name=%s', [name])
	price = curs.fetchone()
	return price

def getTime(conn, pid):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT dt from purchase where pid=%s', [pid])
	time = curs.fetchone()
	return time

def getStudent(conn, bnum):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT name from student where bnum=%s', [bnum])
	students = curs.fetchone()
	return students

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
