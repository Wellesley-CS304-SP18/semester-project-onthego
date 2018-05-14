# @author Heidi Cho, Eliza McNair, Chloe Blazey
# On the Go
# app.py
#
# DESCRIBE APPLICATION HERE


from flask import Flask, render_template, flash, request, redirect, url_for, make_response, jsonify, session, send_from_directory
import sys, os, random
import MySQLdb
import dbconn2
import functions, auth
import bcrypt
from decimal import *
import unicodedata

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# route for the main page
@app.route('/', methods=['POST', 'GET'])
def home():
	return render_template('home.html', title = "On the Go")

# route for the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
	# POST case: a login attempt is made
    if request.method == 'POST':
        retUsername = request.form['ret-username']
        retPassword = request.form['ret-password']

        conn = dbconn2.connect(dsn)
        row = auth.getPassword(retUsername, conn)

        # check if the user exists
        if row is None: # if not, redirect to login
            # Wrong username response:
            flash("Incorrect login information: please re-enter your username and password, or create an account.")
            return redirect(url_for('login'))

        # if the user exists, test for password correctness
        hashed = row['password']
        bPasswd = bcrypt.hashpw(retPassword.encode('utf-8'), hashed.encode('utf-8')) # decrypt password
        if hashed == bPasswd: # if password is correct, successful login!
        	# save username, login status, bnum  to the session
            session['username'] = retUsername
            session['logged_in'] = True
            retuser = auth.usernameLookup(retUsername, conn)
            bnum = retuser['bnum']
            session['bnum'] = bnum
            adminID = retuser['admin']

            flash('Successfully logged onto On-the-Go as ' + retUsername + '.')

            # if the user has an adminid, redirect them to the admin page
            if adminID != None:
            	session['admin'] = adminID # add admin status to the session
            	return redirect(url_for('admin'))
            # if the user has no adminid, set it to 0 and redirect to the order page
            else:
            	session['admin'] = 0 # add admin status to the session
            	return redirect(url_for('order'))
        # if the password is incorrect, redirect to login page
        else:
        	flash("Incorrect login information: please re-enter your username and password, or create an account.")
        	return redirect(url_for('login'))
    else:
        # GET case: no form submission
        return render_template('login.html', title="Welcome to On-the-Go!", script=url_for('login'))

# route for the join page
@app.route('/join/', methods=["GET", "POST"])
def join():
    # POST case: the join form is submitted on the page:
    if request.method == "POST":
        bNum = request.form['b-num']
        name = request.form['name']
        newUsername = request.form['new-username']
        newPassword = request.form['new-password']
        confirmPass = request.form['confirm-password']

        # to check admin authentification:
        org = request.form['org-list']
        adminUser = request.form['admin-username']
        adminPass = request.form['admin-pass']

        # redirect to join page if passwords don't match
        if newPassword != confirmPass:
            flash("Error: Passwords do not match")
            return redirect(url_for('join'))

        # redirect to join page if password not secure
        if len(newPassword) < 10:
            flash("Error: Password must be at least 10 characters long")
            return redirect(url_for('join'))

        # password is valid
        hashed = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
        conn = dbconn2.connect(dsn)

        # if the username is already taken, redirect to join page
        row = auth.usernameLookup(newUsername, conn)
        if row is not None:
            flash ("Error: The username you entered is already taken. Please try again with a new username.")
            return redirect(url_for('join'))

        # if an account already exists for that bnum, redirect to join page
        row = auth.bnumLookup(bNum, conn)
        if row is not None:
            flash ("Error: An account already exists for the B-number you entered.")
            return redirect(url_for('join'))
	
	# check that bnum does not begin with a 'B' or 'b' by confirming
	# that every value in the string is numeric with the .isnumeric() method
	# for unicode - cast bNum as string, then convert to unicode for check
	uniBnum = unicode(str(bNum), 'utf-8') 
	if (not uniBnum.isnumeric()): 
            flash("Error: Your B-number should not include any non-numeric characters. Do not include a B or b at the beginning. Please try again with a valid B-number.")
	    return redirect(url_for('join'))
	elif (len(str(bNum)) != 8):
            flash("Error: Your B-number should only be 8 digits long. Please try again with a valid B-number.")
	    return redirect(url_for('join'))

        # Neither the username nor the B-number have been used already:
        # Now check admin privilege (if applicable)
        if org != "Choose One":
        	# the user has identified themselves as an admin
            # org, adminUser, adminPass to verify - org value is
            conn = dbconn2.connect(dsn)
            # the admin password stored in the table must be extracted before the 
	    # checkAdmin method can be used so that the salt used to hash the admin password, 
	    # which is extracted from the password by the hashpw method, can be used to hash
	    # the admin password entered for comparison; if salt is different, comparison 
	    # in the checkAdmin method will fail: 
            tblPassword = auth.getPassword(adminUser, conn)
	    # extract the password from the dictionary object returned by the query
	    tblHashed = tblPassword['password']
	    hashedAdmin = bcrypt.hashpw(adminPass.encode('utf-8'), tblHashed.encode('utf-8'))
	    tblAdmin = auth.checkAdmin(adminUser, hashedAdmin, conn)
	    # extract the admin org # from the dictionary object returned by the query
	    adminOrg = tblAdmin['admin']
            if adminOrg is None:
                flash("Error: No such administrator exists. Please try again.")
                return redirect(url_for('join'))
	    # Cast unicode 'org' as an int for comparison to the 'long' value 
	    # from the database query 'checkAdmin'
            elif adminOrg != int(org):
                flash("Error: Administrator's organization does not match the organization you selected. Please try again.")
                return redirect(url_for('join'))
            elif adminOrg == int(org):
            	conn = dbconn2.connect(dsn)
                auth.createUserAdmin(bNum, name, newUsername, hashed, org, conn)
                # add bnum, username, admin and login status to the session
                session['bnum'] = bNum
                session['username'] = newUsername
                session['admin'] = org
                session['logged_in'] = True
                # successful join!
                return redirect(url_for('admin'))

        elif org == "Choose One":
            # no attempt to create an account as an administrator
            conn = dbconn2.connect(dsn)
            auth.createUser(bNum, name, newUsername, hashed, conn)
            # add bnum, username, admin and login status to the session
            session['bnum'] = bNum
            session['username'] = newUsername
            session['admin'] = 0
            session['logged_in'] = True
            flash('You have successfully joined!')
            # successful join!
            return redirect(url_for('order'))
    else:
        # GET case: no form submission
        conn = dbconn2.connect(dsn)
        orgs = functions.getDistributors(conn)
        return render_template('join.html', title="Welcome to On-the-Go!", script=url_for('join'), orgs = orgs)

# route for the account page
# this page shows current unfilled orders
@app.route('/account/', methods=["GET"])
def account():
	if (request.method == "GET"):
		# GET request: the user is just looking at their orders
		# don't let the user see this page if not logged in
		if 'logged_in' not in session:
			flash('Please log in first.')
			return redirect(url_for('login')) # redirect to login page

		# if they are logged in
		if 'bnum' in session:
			bnum = session['bnum']
		conn = dbconn2.connect(dsn)
		# get the users orders from the database
		orders = functions.getUsersOrders(conn, bnum)
		names = {}
		times = {}

		# show the user's orders on the webpage
		for item in orders:
			names[item['mid']] = functions.getName(conn, item['mid'])
			times[item['pid']] = functions.getTime(conn, item['pid'])

		return render_template('account.html', title="Your Account", orders=orders, names=names, times=times)

# route for students who are also admins to select role
@app.route('/admin/', methods=['POST', 'GET'])
def admin():
	if (request.method == 'GET'):
		if 'admin' in session: # if the user is logged in
			adminID	= session['admin']
			if adminID != 0: # if the user is an admin
				conn = dbconn2.connect(dsn)
				orders = functions.getActiveOrders(conn) # get the current orders
				names = {}
				times = {}
				students = {}
				for item in orders:
					names[item['mid']] = functions.getName(conn, item['mid'])
					times[item['pid']] = functions.getTime(conn, item['pid'])
					students[item['pid']] = functions.getStudent(conn, item['student'])

				return render_template('admin.html',title="Admin View", orders = orders, names=names, times=times, students = students)
			else: # if the user isn't an admin
				flash('You do not have access to the admin page.')
				return redirect(url_for('order'))
		else: # if the user isn't logged in
			flash('You need to log in')
			return redirect(url_for('login'))
	else: # if the user clicks the markAsComplete button
		conn = dbconn2.connect(dsn)
		# get purchase and menu id for the item whose 'mark as complete'
		# submit button was clicked
		pid = request.form['pid']
		mid = request.form['mid']
		functions.markItemAsComplete(conn, pid, mid) # mark item in an order as complete
		# check whether all items in an order have been marked as complete
		incompletes = functions.getIncompletePurchases(conn, pid) 
		# if no incomplete purchase items exist, mark purchase as complete
		if len(incompletes) == 0: 
                    functions.markPurchaseAsComplete(conn, pid)

		orders = functions.getActiveOrders(conn) # get the new list of current orders
		names = {}
		times = {}
		students = {}
		for item in orders:
			names[item['mid']] = functions.getName(conn, item['mid'])
			times[item['pid']] = functions.getTime(conn, item['pid'])
			students[item['pid']] = functions.getStudent(conn, item['student'])
		return render_template('admin.html',title="Admin View", orders = orders, names=names, times=times, students = students)


# route for the order page
@app.route('/order/cart', methods=['POST', 'GET'])
def order():
	conn = dbconn2.connect(dsn)
	results = functions.getMenu(conn) # get the menu items

	if 'logged_in' not in session: # if the user isn't logged
		flash('Please log in first.')
		return redirect(url_for('login'))

	if 'cart' in session: # if the user already has a cart in use
		cart = session['cart']
	else: # if not, create an empty cart
		cart = list()
		for item in results:
			cart.append({"mid": item['mid'], "quantity": 0, "name":item['name']})

	if 'cost' in session: # if the user already has a cart in use
		cost = session['cost'] # get the cost of the cart
	else: # if not, set cost to 0
		cost=0

	if (request.method == 'GET'):
		conn = dbconn2.connect(dsn)
		results = functions.getMenu(conn)
		return render_template('order.html', title = "Order Now", menu = results, cart=cart, price = cost)
	else: # if the user clicks a button
		# action = request.form['submit']
		# if action == 'submitCart':
		isFull = False
		for thing in cart:
			if (thing['quantity'] != 0):
				isFull = True

		if (isFull): # if it isn't empty
			conn = dbconn2.connect(dsn)
			notes = request.form['comment']

			id = session['bnum']
			functions.addPurchase(conn, id, notes) # record the purchase in the database
			pid = functions.getPurchaseID(conn)
			pid_final=pid['LargestPid']

			# add each of the items in the cart to the database
			for thing in cart:
				if (thing['quantity'] != 0):
					mid = thing['mid']
					quantity = thing['quantity']
					functions.addPurchaseItems(conn, pid_final, mid, quantity)
			flash('Thank you for ordering!')
			session.pop('cart') # reset the cart and cost
			session.pop('cost')
			return redirect(url_for('account'))
		else: # if the cart is empty when the user submits it
			flash('Please select items before submitting an order.')
			return render_template('order.html', title = "Order Now", menu = results, cart=cart, price =cost)

# route for ajax method to set ratings
@app.route('/orderAjax/', methods=['POST', 'GET'])
def orderAjax():
	conn = dbconn2.connect(dsn)
	results = functions.getMenu(conn) # get the menu items

	if 'cart' in session: # if the user already has a cart in use
		cart = session['cart']
	else: # if not, create an empty cart
		cart = list()
		for item in results:
			cart.append({"mid": item['mid'], "quantity": 0, "name":item['name']})

	if 'cost' in session: # if the user already has a cart in use
		cost = session['cost'] # get the cost of the cart
	else: # if not, set cost to 0
		cost=0

	quantity = request.form.get('item-quantity')
	itemName = request.form.get('menu_name')
	itemMid = request.form.get('menu_mid')

	for item in cart:
		mid = int(item['mid'])
		itemMid = int(itemMid)
		if mid == itemMid:
			item['quantity'] = quantity

	# calculate the cost of the cart
	cost = 0
	for item in cart:
		if (item['quantity'] != 0):
			name = item['name']
			q = item['quantity']
			price = functions.getPrice(conn, name) # get price
			price = price['price']
			price = Decimal(price)
			q = Decimal(q)
			cost += q * price # multiply price and quantity

	session['cart'] = cart # set the cart
	session['cost'] = cost # set the cost

	# return json file with tt and the movie's average rating
	return jsonify({"quantity": quantity, "name":itemName, "cost":cost, "mid":itemMid})

@app.route('/logout/')
def logout():
	session.pop('username')
	session.pop('logged_in')
	session.pop('bnum')
	if 'admin' in session:
		session.pop('admin')
	if 'cart' in session:
		session.pop('cart')
	if 'cost' in session:
		session.pop('cost')
	flash("You are now logged out!")
	return redirect(url_for('home'))

if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
		assert(port>1024)
	else:
		port = os.getuid()
	dsn = dbconn2.read_cnf()
	dsn['db'] = 'onthego_db' # database we want to connect to
	app.debug = True
	app.run('0.0.0.0', port)
