# @author Heidi Cho, Eliza McNair, Chloe Blazey
# On the Go
# app.py
#
# DESCRIBE APPLICATION HERE


from flask import Flask, render_template, flash, request, redirect, url_for, make_response, jsonify, session, send_from_directory
import sys, os, random
import MySQLdb
import dbconn2
import functions
import bcrypt
import decimal

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
    if request.method == 'POST':
        retUsername = request.form['ret-username']
        retPassword = request.form['ret-password']

        conn = dbconn2.connect(dsn)
        row = functions.getPassword(retUsername, conn)
        if row is None:
            # Wrong password response:
            flash("Incorrect login information: please re-enter your username and password, or create an account.")
            return redirect(url_for('login'))
        hashed = row['password']
        bPasswd = bcrypt.hashpw(retPassword.encode('utf-8'), hashed.encode('utf-8'))
        print bPasswd # for debugging
        if hashed == bPasswd:
            flash('Successfully logged onto On-the-Go as ' + retUsername + '.')
            session['username'] = retUsername
            session['logged_in'] = True

	    user = functions.usernameLookup(retUsername, conn)
	    bnum = user['bnum']
	    session['bnum'] = bnum
	    adminID = user['admin']

	    if adminID != None:
		    session['admin'] = adminID
		    return redirect(url_for('role'))
            return redirect(url_for('order'))
        else:
            flash("Incorrect login information: please re-enter your username and password, or create an account.")
            return redirect(url_for('login'))
    else:
        # GET case: no form submission
        return render_template('login.html', title="Welcome to On-the-Go!", script=url_for('login'))

# route for the join page
@app.route('/join/', methods=["GET", "POST"])
def join():
    #when the form is submitted on the search page:
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

        if newPassword != confirmPass:
            flash("Error: Passwords do not match")
            return redirect(url_for('join'))

        if len(newPassword) < 10:
            flash("Error: Password must be at least 10 characters long")
            return redirect(url_for('join'))

        hashed = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())

        conn = dbconn2.connect(dsn)
        row = functions.usernameLookup(newUsername, conn)
        if row is not None:
            flash ("Error: The username you entered is already taken. Please try again with a new username.")
            return redirect(url_for('join'))
        conn = dbconn2.connect(dsn)
        row = functions.bnumLookup(bNum, conn)
        if row is not None:
            flash ("Error: An account already exists for the B-number you entered.")
            return redirect(url_for('join'))

        # Neither the username nor the B-number have been used already:
        # Now check admin privilege (if applicable)
        if org != "Choose One":
            # org, adminUser, adminPass to veryify - org value is
            conn = dbconn2.connect(dsn)
            hashedAdmin = bcrypt.hashpw(adminPass.encode('utf-8'), bcrypt.gensalt())
            adminOrg = functions.checkAdmin(adminUser, hashedAdmin, conn)
            if adminOrg is None:
                flash("Error: No such administrator exists. Please try again.")
                return redirect(url_for('join'))

            elif adminOrg != org:
                flash("Error: Administrator's organization does not match the organization you selected. Please try again.")
                return redirect(url_for('join'))

            elif adminOrg == org: # Q: is the logic tight enough to use an 'else'?

            	conn = dbconn2.connect(dsn)
                functions.createUserAdmin(bNum, name, newUsername, hashed, org, conn)
		session['bnum'] = bNum
		session['username'] = newUsername
		session['admin'] = admin
                session['logged_in'] = True
                return redirect(url_for('role'))

        elif org == "Choose One":
            # no attempt to create an account as an administrator
            conn = dbconn2.connect(dsn)
            functions.createUser(bNum, name, newUsername, hashed, conn)
            session['bnum'] = bNum
	    session['username'] = newUsername
            session['logged_in'] = True
            return redirect(url_for('order'))

    else:
        # GET case: no form submission
        conn = dbconn2.connect(dsn)
        orgs = functions.getDistributors(conn)
        return render_template('join.html', title="Welcome to On-the-Go!", script=url_for('join'), orgs = orgs)

# route for the account page
@app.route('/account/', methods=["GET", "POST"])
def account():
	if (request.method == "GET"):
		return render_template('account.html', title="Your Account")
	else:
		if ('submit' in request.form):
			action = request.form['submit']
			if (action == 'logout' and 'username' in session):
				session.pop('username')
		        session.pop('logged_in')
		        flash("You are now logged out!")
			# else:
			# 	flash('Error: You are not currently logged in. Please login or create an account.')
		return render_template('account.html', title="Your Account")

# route for students who are also admins to select role
@app.route('/role/')
def role():
	return render_template('role.html',title="Select Role")

# route for the order page
@app.route('/order/cart', methods=['POST', 'GET'])
def order():
	conn = dbconn2.connect(dsn)
	results = functions.getMenu(conn) # get the menu items
	if 'cart' in session: # if the user already has a cart in use
		cart = session['cart']
	else: # if not, create an empty cart
		cart = {}
		for item in results:
			cart[item['name']] = 0
	if (request.method == 'GET'):
		conn = dbconn2.connect(dsn)
		results = functions.getMenu(conn)
		return render_template('order.html', title = "Order Now", menu = results, cart=cart)
	else: # if the user clicks a button
		if 'submit' in request.form:
			action = request.form['submit']
			if action == 'addToCart': # if the user adds an item to the cart
				quantity = request.form['item-quantity']
				itemName = request.form['menu_name']
				cart[itemName] = quantity # add item and quantity to the cart

				conn = dbconn2.connect(dsn)
				cost = 0
				for thing in cart:
					if (cart[thing] != 0):
						price = functions.getPrice(conn, thing)
						q = int(cart[thing])
						cost += q * price['price']

				flash('You added ' + quantity + ' of '+ itemName + ' to your cart.')
			else: # if the user clicks the order button
				isFull = False
				for thing in cart:
					if (cart[thing] != 0):
						isFull = True
				if (isFull):
					conn = dbconn2.connect(dsn)
					id = session['bnum']
					functions.addPurchase(conn, id) # record the purchase in the database
					pid = functions.getPurchaseID(conn)
					pid_final=pid['LargestPid']

					# add each of the items in the cart to the database
					for thing in cart:
						if (cart[thing] != 0):
							mid = functions.getMID(conn, thing)
							functions.addPurchaseItems(conn, pid_final, mid['mid'], cart[thing])
					return redirect(url_for('yourOrder'))
				else:
					flash('PLEASE SELECT ITEMS BEFORE ORDERING')
		session['cart'] = cart # set the cart
		return render_template('order.html', title = "Order Now", menu = results, cart=cart, price =cost)

# Route for the order confirmation page
@app.route('/yourOrder/', methods=['POST', 'GET'])
def yourOrder():
	cart = session['cart']
	session['cart'] = {}
	return render_template('yourOrder.html',title = "Thank you!", cart=cart)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
		assert(port>1024)
	else:
		port = os.getuid()
	dsn = dbconn2.read_cnf()
	dsn['db'] = 'hcho5_db' # database we want to connect to
	app.debug = True
	app.run('0.0.0.0', port)
