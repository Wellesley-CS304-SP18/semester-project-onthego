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

# Returns the name of a distributor after lookup by id
def getOrg(adminID, conn): 
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name FROM distributor WHERE (did = %s)',[adminID,])
	org = curs.fetchone()
	return org

# Returns a user's bnum and admin 
def getUser(username, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT bnum, admin FROM student WHERE (username = %s)', [username,])
	student = curs.fetchone()
	return student

# Returns all active orders for a given distributor (lookup by id)
def getActiveOrders(adminID, conn): 
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT purchaseItems.pid, purchase.student, purchaseItems.id, purchaseItems.quantity, purchase.complete from purchaseItems INNER JOIN USING (pid) WHERE (purchase.distributor = %s)',[adminID,])
	orders = curs.fetchall()
	return orders

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
