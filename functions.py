# @author Heidi Cho
# On the Go
# 4.25.18
# functions.py
#
# Thie file contains helper functions for app.py.

import sys, os, random
import dbconn2
import MySQLdb

# Create new user with admin privilege
def createUserAdmin(bnum, name, username, hashed, org, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT INTO student(bnum, name, username, password, admin) VALUES (%s, %s, %s, %s, %s)', [bnum, name, username, hashed, org])
	return

# Create new user without admin privilege
def createUser(bnum, name, username, hashed, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT INTO student(bnum, name, username, password\
) VALUES (%s, %s, %s, %s)',[bnum, name, username, hashed])
	return

# Get list of distributors
def getDistributors(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM distributor')
	orgs = curs.fetchall()
	return orgs

# Returns the password associated with a given username
def getPassword(username, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT password FROM student WHERE username = %s', [username,])
	# entry is called password in table but assumption is hashed
	password = curs.fetchone()
	return password

# Returns first 20 menu items from db starting at 0
def getMenu(conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('select * from menu limit 20')
	results = curs.fetchall()
	return results

# Returns the name of a distributor after lookup by id
def getOrg(adminID, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name FROM distributor WHERE (did = %s)',[adminID,])
	org = curs.fetchone()
	return org

# Check a student's admin status with a particular org
def checkAdmin(username, password, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT admin FROM student WHERE username = %s AND password = %s', [username, password])
	adminOrg = curs.fetchone()
	return adminOrg

# Returns a user's bnum and admin from Username
def usernameLookup(username, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT bnum, admin FROM student WHERE (username = %s)', [username,])
	student = curs.fetchone()
	return student

# Lookup user bnum to see if an entry already exists
def bnumLookup(bnum, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT bnum FROM student WHERE bnum = %s', [bnum,])
	bnum = curs.fetchone()
	return bnum

# Returns all active orders for a given distributor (lookup by id)
def getActiveOrders(adminID, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT purchaseItems.pid, purchase.student, purchaseItems.id, purchaseItems.quantity, purchase.complete from purchaseItems INNER JOIN USING (pid) WHERE (purchase.distributor = %s)',[adminID,])
	orders = curs.fetchall()
	return orders

# Creates a new order
def addPurchase(conn, id):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO purchase (student, distributor) VALUES (%s, 1)', [id])

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
