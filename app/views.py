from app import app
from db import db_con
from flask import request, render_template, make_response, jsonify
from flask import url_for, redirect, session
from datetime import date, timedelta
import json
import MySQLdb as mdb

conn = db_con.Database()

"""
==================================================
Index
==================================================
"""

@app.route('/')
@app.route('/index')
def index():
  response = make_response(render_template("index.html"))
  return response

"""
==================================================
Login and Logout
==================================================
"""

@app.route('/api/logout', methods=["POST"])
def logout():
	if 'login' in session:
		cid = session['cid']
		del session['cart']
		del session['login']
		del session['cid']
		return cid + ' Logged out'
	else:
		return 'Logged out'

@app.route('/api/login', methods=["POST"])
def login():
	cur = conn.get_cursor()
	customer = request.form
	if login(cur, customer):
		return jsonify({'success': "Login Successful"})
	else:
		return jsonify({'error': "Login Required"})

@app.route('/api/user', methods=["GET"])
def get_user():
	if 'login' in session:
		return jsonify({'success':str(session['cid'])})
	else:
		return jsonify({'error': ''})
	
@app.route('/api/get_cart', methods=['GET'])
def get_cart():
	if is_logged_in():
		return jsonify(session['cart'])
	else:
		return jsonify({'error': "Login Required"})

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
	if is_logged_in():
		item = request.form
		upc = item['upc']

		try:
			quantity = int(item['quantity'])
		except ValueError:
			return jsonify({'error':'invalid quantity'})

		cur = conn.get_cursor()
		cur.execute("SELECT upc,stock FROM Item WHERE upc=%s", upc)
		stock = cur.fetchone()['stock']

		if not stock:
			return jsonify({'error':'item not exist'})

		conn.con.commit()

		if upc in session['cart']:
			current_cart = session['cart'][upc]
			cart_quantity  = current_cart + quantity
		else:
			current_cart = 0
			cart_quantity = quantity

		if cart_quantity > stock:
			available = max(0, stock-current_cart)
			if available == 0:
				return jsonify({'error':'Item out of stock'})
			return jsonify({'available':available})
		else:
			session['cart'][upc] = cart_quantity

		return jsonify({"success": 'add successful'})

	else:
		return jsonify({'error': "login Required"})

@app.route('/api/update_cart', methods=['POST'])
def update_cart():
	if is_logged_in():
		item = request.form
		upc = item['upc']
		
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return jsonify({'error':'invalid quantity'})

		cur = conn.get_cursor()
		cur.execute("SELECT upc,stock FROM Item WHERE upc=%s", upc)
		stock = cur.fetchone()['stock']

		if not stock:
			conn.con.commit()
			return jsonify({'error':'item not exist'})

		if quantity <= session['cart'][upc]:
			session['cart'][upc] = quantity
			conn.con.commit()
			if session['cart'][upc] == 0:
					del session['cart'][upc]
			return jsonify({"success": 'Update successful'})

		conn.con.commit()
		if upc in session['cart']:
			if quantity > stock:
				available = stock
				return jsonify({'error':'Not Enough Stock', 'available':available})
			else:
				session['cart'][upc] = quantity
		else:
			session['cart'][upc] = quantity


		return jsonify({"success": 'Update successful'})

	else:
		return jsonify({'error': "login Required"})
	
"""
==================================================
Search, Registration, Online Purchase, Price Request
==================================================
"""
@app.route('/api/search', methods=["GET"])
def search():
	cur = conn.get_cursor()
	search_terms = request.args
	query = "SELECT * from Item I, LeadSinger L WHERE I.upc=L.upc "

	if 'leadsinger' in search_terms:
		singer = str(search_terms['leadsinger']).lower()
		if len(singer) > 100:
			return "Invalid input"
		query += "AND LOWER(L.name) LIKE '%" + singer + "%' "
		

	if 'title' in search_terms:
		title = str(search_terms['title'])
		if len(title) > 100:
			return "Invalid input"
		query += "AND I.title LIKE '%" + title + "%' "

	if 'category' in search_terms:
		category = str(search_terms['category'])
		if len(category) > 100:
			return "Invalid input"
		query += "AND I.category='" + category + "' "

	cur.execute(query)
	search_result = stringify(cur.fetchall())
	conn.con.commit()
	return jsonify({'result':search_result})

@app.route('/api/registration', methods=["POST"])
def registration():
	cur = conn.get_cursor()
	customer = json.loads(request.form['customer'])
	cid = str(customer['cid'])

	if not is_customer_valid(customer):
		return jsonify({'error':"invalid input"})

	cur.execute("select * from Customer where cid=%s", cid)
	if cur.fetchall():
		conn.con.commit()
		return jsonify({'error':"cid already exist"})

	if customer['password'] != customer['password_confirmation']:
		conn.con.commit()
		return jsonify({'error':"passwords do not match"})

	cid = str(customer['cid'])
	password = str(customer['password'])
	name = str(customer['name'])
	address = str(customer['address'])
	phone = str(customer['phone'])
	input_args = (cid, password, name, address, phone)

	cur.execute("insert into Customer values (%s, %s, %s, %s, %s)", input_args)
	conn.con.commit()
	login(cur, customer)
	return jsonify({'sucess':"registration complete"})
	

@app.route('/api/price', methods=["get"])
def price_request():
	items = json.loads(request.args['arr'])
	if is_valid(items):
		return str(price(items))
	else:
		return 'invalid input'

@app.route('/api/online_purchase', methods=["post"])
def purchase_online():
	cur = conn.get_cursor()
	if not is_logged_in():
		return 'login required'
		
	customer = json.loads(request.form['customer'])
	if authenticate(cur, customer) != 'Success':
		return 'Authentication failed'

	#customer = json.loads(request.form['customer'])
	#if not is_logged_in():
		#if not login(cur, customer):
			#return 'authentication failed'
		
	#items = json.loads(request.form['arr'])
	items_dict = session['cart']
	items = []
	for item in items_dict:
		temp = {}
		temp['upc'] = item
		temp['quantity'] = items_dict[item]
		items.append(temp)

	cid = session['cid']
	today = str(date.today())
	expected = str(expected_delivery())

	if not is_legal_quantity(cur, items):
		session['cart'] = {}
<<<<<<< HEAD
		return 'Illegal quantity'
=======
		return jsonify({'error':'illegal quantity'})
>>>>>>> cd1e7a60f362b374d11c62c0a365267f6442afa0

	trivial = True;
	for key in items_dict.keys():
		if items_dict[key]>0:
			trivial = False
			break;
	if trivial:
		return jsonify({'error':'Trivial quantity'})
		
	credit = json.loads(request.form['credit'])

	if 'cardnum' not in credit or 'expirydate' not in credit:
		return 'Invalid input'

	insert_args = (today, str(credit['cardnum']), str(credit['expirydate']), expected, cid )
	try:
		cur.execute("INSERT into Purchase (purchasedate, cardnum, expirydate, expecteddate, cid) VALUES (%s,%s,%s,%s, %s)", insert_args)
	except mdb.Error, e:
		return jsonify({'error':'Invalid Input'})

	cur.execute("select last_insert_id()")
	pid = cur.fetchone()['last_insert_id()']
	purchase_item(cur, items)
	conn.con.commit()

	session['cart'] = {}
	context = receipt_base(cur, pid, today, items)
	context['cardnum'] = str(credit['cardnum'])[-5:]
	context['expecteddate'] = expected

	return jsonify(context)


"""
==================================================
credit purchase, cash purchase, return, get purchases, get purchase
==================================================
"""
@app.route('/api/store_purchase/credit', methods=["post"])
def purchase_credit():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])

	if not is_valid(items):
		return 'invalid input'

	for item in items:
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return jsonify({'error':'invalid quantity'})

	credit = json.loads(request.form['credit'])
	if 'expirydate' not in credit:
		return 'invalid input'
	
	if len(str(credit['cardnum'])) != 16 or len(str(credit['expirydate'])) != 10:
		return jsonify({'error':'invalid card'})

	insert_args = (today, str(credit['cardnum']), str(credit['expirydate']) )
	try:
		cur.execute("insert into Purchase (purchasedate, cardnum, expirydate) values (%s,%s,%s)", insert_args)
	except mdb.Error, e:
		return 'invalid input'

	cur.execute("select last_insert_id()")
	pid = cur.fetchone()['last_insert_id()']
	purchase_item(cur, items)
	conn.con.commit()
	context = receipt_base(cur, pid, today, items)
	context['cardnum'] = str(credit['cardnum'])[-5:]
	return jsonify(context)

@app.route('/api/store_purchase/cash', methods=["post"])
def purchase_cash():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])

	if not is_valid(items):
		return 'invalid input'

	for item in items:
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return jsonify({'error':'invalid quantity'})

	cur.execute("insert into Purchase (purchasedate) values (%s)", today) 

	cur.execute("select last_insert_id()")
	pid = cur.fetchone()['last_insert_id()']
	purchase_item(cur, items)
	conn.con.commit()
	context = receipt_base(cur, pid, today, items)
	return jsonify(context)
		

@app.route('/api/return', methods=["POST"])
def return_item():
	curr = conn.get_cursor()
	today = date.today()
	receiptid = request.form['receiptid']
	items = json.loads(request.form['arr'])

	if not is_valid(items):
		return "Invalid input"

	total = price(items)

	# Check if purchased within 15 days
	curr.execute("SELECT purchasedate, cardnum FROM Purchase WHERE receiptid= %s", receiptid)
	purchase_info = curr.fetchone()
	diff = today - purchase_info['purchasedate']

	if diff.days > 15:
		conn.con.commit()
		return "Receipt expired"

	# Check if quantity is legal
	curr.execute("SELECT upc,quantity FROM PurchaseItem WHERE receiptid= %s", receiptid)
	purchased_items = {}
	for item in curr.fetchall():
		purchased_items[str(item['upc'])] = item['quantity']

	curr.execute("SELECT upc,SUM(quantity) FROM ReturnItem,ReturnTable WHERE receiptid= %s GROUP BY upc", receiptid)
	returned_items = {}
	for item in curr.fetchall():
		returned_items[item['upc']] = item['SUM(quantity)']

	#return str(returned_items) + '\n' + str(purchased_items)
	for item in items:
		upc = item['upc']
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return "Invalid Input"

		not_returned = purchased_items[upc]
		if upc in returned_items:
			not_returned -= returned_items[upc]
		if quantity > not_returned:
			conn.con.commit()
			return "Illegal Return Quantity for item " + str(item['upc'])
		
	# Return the item
	curr.execute("INSERT INTO ReturnTable (receiptid, returndate) VALUES (%s, %s)", (receiptid, str(today)) )
	for item in items:
		curr.execute("INSERT INTO ReturnItem (select last_insert_id(),%s,%s)", (str(item['upc']), str(item['quantity'])))
		curr.execute("UPDATE Item SET stock = stock+%s WHERE upc = %s", (str(item['quantity']), str(item['upc'])))
	conn.con.commit()

	# Return message
	if purchase_info['cardnum']:
		return "Return Processed, credit $" + str(total) + " to credit card ***********" + purchase_info['cardnum'][-5:]

	return "Return Processed, return $" + str(total) + " in cash"


@app.route('/api/purchase/<receiptid>', methods=["GET"])
def get_purchase(receiptid):
	curr = conn.get_cursor()
	curr.execute("SELECT I.upc,title,price,quantity FROM Item I, PurchaseItem PI WHERE I.upc=PI.upc AND receiptid = %s", receiptid)
	items = curr.fetchall()
	curr.execute("SELECT upc, SUM(quantity) FROM ReturnItem RI, ReturnTable R WHERE RI.retid=R.retid AND receiptid=%s GROUP BY upc", receiptid)
	returned_data = curr.fetchall()
	returned = {}
	for data in returned_data:
		returned[data['upc']] = data['SUM(quantity)']

	for item in items:
		if item['upc'] in returned:
			item['quantity'] -= returned[item['upc']]

	conn.con.commit()
	return jsonify({'data': stringify(items)})

@app.route('/api/purchases', methods=["GET"])
def get_purchases():
	earliest = str(date.today() - timedelta(days=15))
	curr = conn.get_cursor()
	curr.execute("SELECT receiptid,purchasedate FROM Purchase WHERE purchasedate >= %s", earliest)
	purchases = curr.fetchall()
	conn.con.commit()
	return jsonify({'data':stringify(purchases)})

"""
==================================================
Get Item(s), Expected delivery, Add item, 
==================================================
"""
@app.route('/api/items', methods=["GET"])
def get_items():
  return jsonify({ "data": stringify(conn.read("SELECT * FROM Item I, LeadSinger LS WHERE I.upc=LS.upc")) })

@app.route('/api/items/<item_upc>', methods=["GET"])
def get_item(item_upc):
  curr = conn.get_cursor()
  curr.execute("SELECT * FROM Item WHERE upc = %s", item_upc)
  item = curr.fetchall()
  curr.execute("SELECT * FROM HasSong WHERE upc = %s", item_upc)
  songs = curr.fetchall()
  curr.execute("SELECT * FROM LeadSinger WHERE upc = %s", item_upc)
  singers = curr.fetchall()
  conn.con.commit()
  return jsonify({ "data": stringify(item), "songs": stringify(songs), "singers": stringify(singers)})

@app.route('/api/outstanding', methods=["GET"])
def oustanding():
	curr = conn.get_cursor()
	curr.execute("SELECT * from Purchase WHERE cid IS NOT NULL AND delivereddate is NULL")
	purchases = curr.fetchall()
	conn.con.commit()
	return jsonify({'data':stringify(purchases)})

@app.route('/api/checkout/expected', methods=["GET"])
def expected_delivery():
  cur = conn.get_cursor()
  cur.execute("SELECT COUNT(delivereddate) FROM Purchase")
  pending = cur.fetchone()['COUNT(delivereddate)']
  expected = pending/10
  expect_date = str(date.today()+timedelta(days=expected))
  conn.con.commit()
  return expect_date

@app.route('/api/items/add', methods=["POST"])
def add_item():
	cur = conn.get_cursor()
	item = request.form
	upc = str(item['upc'])
	quantity = str(item['quantity'])
	if 'price' in item:
		price = str(item['price'])
		if len(price) > 30:
			return 'Invalid Input'
	else:
		price = None

	if len(upc) > 30 or len(quantity) > 30:
		return 'Invalid Input'

	cur.execute("SELECT * FROM Item WHERE upc=%s", upc)
	if not cur.fetchone():
		conn.con.commit()
		return 'Item not exist'

	if 'price' in item:
		cur.execute("UPDATE Item SET price=%s, stock=stock+%s WHERE Item.upc=%s", (price, quantity, upc) )
	else:
		cur.execute("UPDATE Item SET stock=stock+%s WHERE Item.upc=%s", (quantity, upc) )
	cur.execute("SELECT * from Item WHERE upc=%s", upc)
	result = cur.fetchone()
	conn.con.commit()

	if 'price' in item:
		return 'Item ' + upc + ' now has stock ' + str(result['stock']) + ' and price ' + str(result['price'])
	else:
		return 'Item ' + upc + ' now has stock ' + str(result['stock']) + ' and price is not changed' 


"""
==================================================
Sales Report, Top Items, Delivery Update
==================================================
"""

@app.route('/api/manager/sales_report', methods=["GET", "POST"])
def sales_report():
	cur = conn.get_cursor()
	if not 'date' in request.form:
		return jsonify({'error':'Invalid Input'})
	date = str(request.form['date'])	
	if len(date) > 10 or len(date) < 1:
		return jsonify({'error':'Invalid Input'})

	query = " SELECT I.upc, category, SUM(quantity) units, I.price, I.price*SUM(quantity) total " + \
		"FROM Item I,Purchase P,PurchaseItem PI " + \
		"WHERE I.upc = PI.upc AND P.receiptid = PI.receiptid " + \
    		"AND purchasedate = '" + date + "' " \
		"GROUP BY I.upc, I.price, category " + \
		"ORDER BY category"

	cur.execute(query)
	data = cur.fetchall()
	conn.con.commit()
	partition = {}
	for entry in data:
		if entry['category'] not in partition:
			partition[entry['category']] = [entry]
		else:
			partition[entry['category']].append(entry)
	for part in partition.keys():
		partition[part] = stringify(partition[part])

	return jsonify({'success': partition})

@app.route('/api/manager/top_items', methods=["GET"])
def top_items():
	cur = conn.get_cursor()
	date = str(request.args['date'])
	try:
		n = int(request.args['n'])
	except ValueError:
		return jsonify({'error':'Invalid Input'})

	if len(date) > 10:
		return jsonify({'error':'Invalid Input'})
	
	query = " SELECT I.upc, I.title, I.company, I.stock, SUM(quantity) units " + \
		"FROM Item I,Purchase P,PurchaseItem PI " + \
		"WHERE I.upc = PI.upc AND P.receiptid = PI.receiptid " + \
    		"AND purchasedate = '" + date + "' " \
		"GROUP BY I.upc, I.title, I.company, I.stock " + \
		"ORDER BY SUM(quantity) DESC"

	cur.execute(query)
	data = []
	for i in range(0,n):
		entry = cur.fetchone()
		if not entry:
			break
		data.append(entry)
		
	conn.con.commit()
	return jsonify({'success':stringify(data)})
		
@app.route('/api/deliver_update', methods=["POST"])
def deliver_update():
	cur = conn.get_cursor()
	date = str(request.form['date'])
	receiptid = str(request.form['receiptid'])
	if len(date) > 10 or len(receiptid) > 10:
		return "Invalid input"

	cur.execute("SELECT expecteddate FROM Purchase WHERE receiptid=%s", receiptid)
	data = cur.fetchone()
	if not data:
		conn.con.commit()
		return "Receipt ID does not exist"
	if not data['expecteddate']:
		conn.con.commit()
		return "Not online purchase"
	
	cur.execute("UPDATE Purchase SET delivereddate=%s WHERE receiptid=%s", (date, receiptid))
	conn.con.commit()
	return "Purchase " + receiptid + "'s delivered date is updated to " + date

	
"""
==================================================
	Helper Functions
==================================================
"""
def is_logged_in():
	if not 'login' in session:
		return False
	if not session['login']=='Success':
		return False
	return True

def login(cur, customer):
	if authenticate(cur, customer) =='Success':
		session['login'] = 'Success'
		session['cid'] = customer['cid']
		session['cart'] = {}
		return True;
	else:
		return False

def authenticate(cur, customer):
	if 'cid' not in customer or 'password' not in customer:
		return 'Invalid input'

	cur.execute("SELECT password FROM Customer WHERE cid = %s", str(customer['cid']))
	result = cur.fetchone()
	if not result:
		conn.con.commit()
		return 'User not exist'
	if customer['password'] != result['password']:
		conn.con.commit()
		return 'Wrong password'
	conn.con.commit()
	return 'Success'


def is_legal_quantity(cur, items):
	for item in items:
		cur.execute("SELECT stock FROM Item WHERE Item.upc = %s", str(item['upc']) )
		if cur.fetchone()['stock'] < item['quantity']:
			conn.con.commit()
			return False
	return True
	
def receipt_base(cur, pid, today, items):
	cur.execute("select * from Purchase, PurchaseItem, Item where Purchase.receiptid=%s and Purchase.receiptid=PurchaseItem.receiptid and PurchaseItem.upc = Item.upc", pid)
	conn.con.commit()
	context = {}
	context['purchaseitems'] = stringify(cur.fetchall())
	context['price'] = str(price(items))
	context['date'] = str(today)
	context['pid'] = str(pid)
	return context;

def purchase_item(cur, items):
	for item in items:
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return False
		cur.execute( "INSERT INTO PurchaseItem (SELECT last_insert_id() ,%s, %s)", (str(item['upc']), str(item['quantity'])) )
		cur.execute( "UPDATE Item SET stock = stock-%s WHERE upc = %s", (str(item['quantity']), str(item['upc'])) )
	return True

def is_valid(items):
	for item in items:
		if len(str(item['upc'])) > 10 or len(str(item['quantity']))> 10:
			return False;
	return has_items(items)

def has_items(items):
	curr = conn.get_cursor()
	for item in items:
		curr.execute("select * from Item WHERE upc=%s", str(item['upc']) )
		if not curr.fetchall():
			conn.con.commit()
			return False
	conn.con.commit()
	return True

def price(items):
	curr = conn.get_cursor()
	total = 0
	for item in items:
		curr.execute("SELECT price from Item WHERE upc=%s", str(item['upc']) )
		price = curr.fetchone()['price']
		try:
			quantity = int(item['quantity'])
		except ValueError:
			return 0
		total += price*int(item['quantity'])
	conn.con.commit()
	return total

def stringify(items):
	for item in items:
		for attribute in item.keys():
			if item[attribute] is not None:
				item[attribute] = str(item[attribute])
			else:
				item[attribute] = 'NULL'
	return items

def is_customer_valid(customer):
	if 'cid' not in customer:
		return False
	if 'password' not in customer:
		return False
	if 'password_confirmation' not in customer:
		return False
	if 'name' not in customer:
		return False
	if 'address' not in customer:
		return False
	if 'phone' not in customer:
		return False

	cid = len(str(customer['cid']))
	password = len(str(customer['password']))
	password_conf = len(str(customer['password_confirmation']))
	name = len(str(customer['name']))
	address = len(str(customer['address']))
	phone = len(str(customer['phone']))

	if cid > 20 or cid < 1:
		return False
	if password > 20 or password < 1:
		return False
	if not password == password_conf:
		return False
	if name > 50 or name < 1:
		return False
	if address > 50 or address < 1:
		return False
	if phone > 20 or phone < 1:
		return False
	return True
