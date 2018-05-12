# @author Heidi Cho
# On the Go
# 4.25.18
# login.py
#
# Thie file contains helper login and auth functions for app.py.

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

# Returns the password associated with a given username
def getPassword(username, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT password FROM student WHERE username = %s', [username,])
	# entry is called password in table but assumption is hashed
	password = curs.fetchone()
	return password

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