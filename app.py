# @author Heidi Cho,
# On the Go
# 4.25.18
# app.py
#
# DESCRIBE APPLICATION HERE


from flask import Flask, render_template, flash, request, redirect, url_for, make_response, jsonify, session, send_from_directory
import sys, os, random
import MySQLdb
import dbconn2
import functions
import bcrypt

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
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        # called password in our table but assumption is hashed
        curs.execute('SELECT password FROM student WHERE username = %s',
                     [retUsername])
        row = curs.fetchone()
        if row is None:
            # Wrong password response:
            flash("Incorrect login information: please re-enter your username and password, or create an account.")
            return redirect(url_for('login'))
        hashed = row['password']
        bPasswd = bcrypt.hashpw(retPassword.encode('utf-8'), hashed.encode('utf-8'))
        print bPasswd # for debugging
        if hashed == bPasswd:
            flash('Successfully logged onto On-the-Go as ' + username + '.')
            session['username'] = username
            session['logged_in'] = True
            return #Where are we going next?
        else:
            flash("Incorrect login information: please re-enter your username and password, or create an account.")
            return redirect(url_for('login'))
    else:
        # GET case: no form submission
        return render_template('login.html', title="Log-in", script=url_for('login'))

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
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT username FROM student WHERE username = %s',
                     [newUsername,])
        row = curs.fetchone()
        if row is not None:
            flash ("Error: The username you entered is already taken. Please try again with a new username.")
            return redirect(url_for('join'))
        conn = dbconn2.connect(dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT bnum FROM student WHERE bnum = %s',
                     [bNum,])
        row = curs.fetchone()
        if row is not None:
            flash ("Error: An account already exists for the B-number you entered.")
            return redirect(url_for('join'))

        # Neither the username nor the B-number have been used already:
        # Now check admin privilege (if applicable)
        if org != "Choose One":
            # org, adminUser, adminPass to veryify - org value is
            conn = dbconn2.connect(dsn)
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            hashedAdmin = bcrypt.hashpw(adminPass.encode('utf-8'), bcrypt.gensalt())
            curs.execute('SELECT admin FROM student WHERE username = %s AND password = %s',
                         [adminUser, hashedAdmin])
            adminOrg = curs.fetchone()
            if adminOrg is None:
                flash("Error: No such administrator exists. Please try again.")
                return redirect(url_for('join'))

            elif adminOrg != org:
                flash("Error: Administrator's organization does not match the organization you selected. Please try again.")
                return redirect(url_for('join'))

            elif adminOrg == org: # Q: is the logic tight enough to use an 'else'?

            	conn = dbconn2.connect(dsn)
            	curs = conn.cursor(MySQLdb.cursors.DictCursor)
                curs.execute('INSERT INTO student(bnum, name, username, password, admin) VALUES(%s, %s, %s, %s, %s)', [bNum, name, newUsername, hashed, org])
                session['username'] = newUsername
                session['logged_in'] = True
                return # Where to next?

        elif org == "Choose One":
            # no attempt to create an account as an administrator
            conn = dbconn2.connect(dsn)
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('INSERT INTO student (bnum, name, username, password) VALUES(%s, %s, %s, %s)', [bNum, name, newUsername, hashed])
            session['username'] = newUsername
            session['logged_in'] = True
            return # Where to next?

    else:
        # GET case: no form submission
        conn = dbconn2.connect(dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM distributor')
        orgs = curs.fetchall()
        return render_template('join.html', title="Welcome to On-the-Go!", script=url_for('join'), orgs = orgs)

@app.route('/logout/')
def logout():
    if 'username' in session:
        username = session['username']
        session.pop('username')
        session.pop('logged_in')
        flash("You are now logged out!")
        return redirect(url_for('index'))
    else:
        flash('Error: You are not currently logged in. Please login or create an account.')
        return redirect(url_for('index'))

# route for the page to rate movies
@app.route('/order/cart', methods=['POST', 'GET'])
def order():
	conn = dbconn2.connect(dsn)
	results = functions.getMenu(conn) # get the menu items
	if 'cart' in session:
		cart = session['cart']
	else:
		cart = {}
		for item in results:
			cart[item['name']] = 0
	if (request.method == 'GET'):
		conn = dbconn2.connect(dsn)
		results = functions.getMenu(conn)
		return render_template('order.html', title = "Order Now", menu = results, cart=cart)
	else:
		if 'submit' in request.form:
			action = request.form['submit']
			if action == 'addToCart': # if the user adds an item to the cart
				quantity = request.form['item-quantity']
				if quantity == 0:
					flash('You did not add anything to your cart.')
				else:
					itemName = request.form['menu_name']
					cart[itemName] = quantity
					flash('You added ' + quantity + ' of '+ itemName + ' to your cart.')
			else: # if the user clicks the order button
				conn = dbconn2.connect(dsn)
				# id = session['bnum']
				id = 20729654
				functions.addPurchase(conn, id)
				pid = functions.getPurchaseID(conn)
				pid_final=pid['LargestPid']
				for thing in cart:
					if (cart[thing] != 0):
						mid = functions.getMID(conn, thing)
						functions.addPurchaseItems(conn, pid_final, mid['mid'], cart[thing])
				return redirect(url_for('yourOrder', pid=pid_final))
		session['cart'] = cart
		return render_template('order.html', title = "Order Now", menu = results, cart=cart)

@app.route('/yourOrder/<pid>/', methods=['POST', 'GET'])
def yourOrder(pid):
	conn = dbconn2.connect(dsn)
	items = functions.getPurchaseItems(conn, pid)
	order = []
	for thing in items:
		order.append(functions.getName(conn, thing['mid']))
	session['cart'] = {}
	return render_template('yourOrder.html',title = "Thank you!", order=order)

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
