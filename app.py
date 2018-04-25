# @author Heidi Cho, 
# On the Go
# 4.25.18
# app.py
#
# DESCRIBE APPLICATION HERE


from flask import Flask, render_template, flash, request, redirect, url_for, make_response, jsonify
import sys, os, random
import dbconn2
import functions

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# route for the main page
@app.route('/', methods=['POST', 'GET'])
def process():
	return render_template('base.html', title = "WMDB Interactions")

# route for the login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html', title = "Login")
    else:
        conn = dbconn2.connect(DSN)

		# get login info from form
        id = request.form['userid']
        pwd = request.form['passwd']

		# check to see if the staff member exists
        result = functions.searchStaff(conn, id)

		# if the staff member exists
        if (result and pwd == 'secret'): # and password is secret
			flash('You are logged in as ' + id)
			resp = make_response(render_template('login.html', title = "Login"))
			resp.set_cookie('user', id) # set cookie
			return resp
        else:
			flash('Incorrect login credentials') # flash that login failed
			return render_template('login.html', title = "Login")

# route for the page to rate movies
@app.route('/order', methods=['POST', 'GET'])
def order():
	user = request.cookies.get('user') # get the cookie
	if not user: # if none
		flash('Please log in first') # ask the user to login
	else: # if they're already logged in
		if (request.method == 'GET'):
			conn = dbconn2.connect(DSN)
			results = functions.getMenu(conn)
			return render_template('order.html',
									title = "Order Now",
									userid = user,
									menu = results)
		else:
			conn = dbconn2.connect(DSN)
			results = functions.getMenu(conn) # get the first 20 movies

			if 'item-quantity' in request.form: # if the user selected a rating value
				# get info from the form
				mid = request.form['menu_mid']
				quantity = request.form['item-quantity']
				user = request.cookies.get('user') # get the user id from cookie



				flash("User " + user + " sucessfully added item to cart")
				return render_template('order.html',
										title = "Order Now",
										userid = user,
										menu = results)
			else: # if the user didn't select a rating value
				flash("Error: Please add items to your cart")
				return render_template('order.html',
										title = "Order Now",
				 						userid = user,
										menu = results)


# route for ajax method to set ratings
@app.route('/setRatingAjax/', methods=['POST', 'GET'])
def setRatingAjax():
	# get info from the form
	tt = request.form.get('movie_tt')
	rating = request.form.get('stars')
	user = request.cookies.get('user') # get the user id

	conn = dbconn2.connect(DSN)
	average = functions.makeAndUpdateRating(conn, tt, rating, user)

	# return json file with tt and the movie's average rating
	return jsonify({"tt": tt, "avgrating": average['avg(rating)']})


if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
		assert(port>1024)
	else:
		port = os.getuid()
	DSN = dbconn2.read_cnf()
	DSN['db'] = 'hcho5_db' # database we want to connect to
	app.debug = True
	app.run('0.0.0.0', port)
