from app import app
from db import db_con
from flask import request, render_template, make_response, jsonify 
from datetime import date, timedelta
import json


conn = db_con.Database()

@app.route('/')
@app.route('/index')
def index():
  response = make_response(render_template("index.html"))
  return response

""" Henry's Code Start """
@app.route('/api/search', methods=["GET", "POST"])
def search():
	cur = conn.get_cursor()
	#search_terms = json.loads(request.args['search'])
	search_terms = request.args
	singer = str(search_terms['leadsinger']).lower()
	title = str(search_terms['title'])
	category = str(search_terms['category'])
	if len(singer) > 100:
		return "Invalid input"
	if len(title) > 100:
		return "Invalid input"
	if len(category) > 100:
		return "Invalid input"
	cur.execute("SELECT * from Item I, LeadSinger L WHERE LOWER(L.name)=%s AND I.title=%s AND I.category=%s", (singer, title, category) )
	search_result = stringify(cur.fetchall())
	conn.con.commit()
	return jsonify({'result':search_result})

@app.route('/api/registration', methods=["POST"])
def registration():
	cur = conn.get_cursor()
	customer = json.loads(request.form['customer'])
	cid = str(customer['cid'])

	if not is_customer_valid(customer):
		return "Invalid input"

	cur.execute("SELECT * from Customer WHERE cid=%s", cid)
	if cur.fetchall():
		conn.con.commit()
		return "CID is already exist"

	cid = str(customer['cid'])
	password = str(customer['password'])
	name = str(customer['name'])
	address = str(customer['address'])
	phone = str(customer['phone'])
	input_args = (cid, password, name, address, phone)

	cur.execute("INSERT INTO Customer VALUES (%s, %s, %s, %s, %s)", input_args)
	conn.con.commit()
	return "Registration complete"
	

@app.route('/api/price', methods=["GET"])
def price_request():
	items = json.loads(request.args['arr'])

	if is_valid(items):
		return str(price(items))
	else:
		return 'Invalid input'

@app.route('/api/online_purchase', methods=["POST"])
def purchase_online():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])
	expected = str(expected_delivery())
	customer = json.loads(request.form['customer'])

	if not is_valid(items):
		return 'Invalid input'

	if not is_legal_quantity(cur, items):
		return 'Illegal quantity'

	result = authenticate(cur, customer)
	if not result=='Success': 
		return result

	credit = json.loads(request.form['credit'])
	insert_args = (today, str(credit['cardnum']), str(credit['expirydate']), expected, str(customer['cid']) )
	cur.execute("INSERT INTO Purchase (purchasedate, cardnum, expirydate, expecteddate, cid) VALUES (%s,%s,%s,%s, %s)", insert_args)

	cur.execute("SELECT last_insert_id()")
	pid = cur.fetchone()['last_insert_id()']
	purchase_item(cur, items)
	conn.con.commit()

	context = receipt_base(cur, pid, today, items)
	context['cardnum'] = str(credit['cardnum'])[-5:]
	context['expecteddate'] = expected

	return jsonify(context)


@app.route('/api/store_purchase/credit', methods=["POST"])
def purchase_credit():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])

	if not is_valid(items):
		return 'Invalid input'

	credit = json.loads(request.form['credit'])
	insert_args = (today, str(credit['cardnum']), str(credit['expirydate']) )
	cur.execute("INSERT INTO Purchase (purchasedate, cardnum, expirydate) VALUES (%s,%s,%s)", insert_args)

	cur.execute("SELECT last_insert_id()")
	pid = cur.fetchone()['last_insert_id()']
	purchase_item(cur, items)
	conn.con.commit()

	context = receipt_base(cur, pid, today, items)
	context['cardnum'] = str(credit['cardnum'])[-5:]

	return jsonify(context)

@app.route('/api/store_purchase/cash', methods=["POST"])
def purchase_cash():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])

	if not is_valid(items):
		return 'Invalid input'

	cur.execute("INSERT INTO Purchase (purchasedate) VALUES (%s)", today) 

	cur.execute("SELECT last_insert_id()")
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
		purchased_items[item['upc']] = item['quantity']

	curr.execute("SELECT upc,SUM(quantity) FROM ReturnItem,ReturnTable WHERE receiptid= %s GROUP BY upc", receiptid)
	returned_items = {}
	for item in curr.fetchall():
		returned_items[item['upc']] = item['SUM(quantity)']
	for item in items:
		upc = item['upc']
		quantity = item['quantity']
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

def authenticate(cur, customer):
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
	cur.execute("select * from Purchase, PurchaseItem, Item where Purchase.receiptid=%s and Purchase.receiptid=Purchaseitem.receiptid and PurchaseItem.upc = Item.upc", pid)
	conn.con.commit()
	context = {}
	context['purhcaseitems'] = stringify(cur.fetchall())
	context['price'] = str(price(items))
	context['date'] = str(today)
	context['pid'] = str(pid)
	return context;

def purchase_item(cur, items):
	for item in items:
		cur.execute( "INSERT INTO PurchaseItem (SELECT last_insert_id() ,%s, %s)", (str(item['upc']), str(item['quantity'])) )
		cur.execute( "UPDATE Item SET stock = stock-%s WHERE upc = %s", (str(item['quantity']), str(item['upc'])) )

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
		total += price*item['quantity']
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
	cid = len(str(customer['cid']))
	password = len(str(customer['password']))
	name = len(str(customer['name']))
	address = len(str(customer['address']))
	phone = len(str(customer['phone']))

	if cid > 20 or cid < 1:
		return False
	if password > 20 or password < 1:
		return False
	if name > 50 or name < 1:
		return False
	if address > 50 or address < 1:
		return False
	if phone > 20 or phone < 1:
		return False
	return True

"""Henry's Code End"""

@app.route('/api/items', methods=["GET"])
def get_items():
  return jsonify({ "data": stringify(conn.read("SELECT * FROM Item")) })

@app.route('/api/items/<item_upc>', methods=["GET"])
def get_item(item_upc):
  curr = conn.get_cursor()
  curr.execute("SELECT * FROM Item WHERE upc = %s", item_upc)
  item = curr.fetchall()
  curr.execute("SELECT * FROM HasSong WHERE upc = %s", item_upc)
  songs = curr.fetchall()
  conn.con.commit()
  return jsonify({ "data": stringify(item), "songs": stringify(songs)})

@app.route('/api/items/<item_upc>', methods=["PUT"])
def update_item(item_upc):
  return item_upc

@app.route('/api/items/<item_upc>', methods=["DELETE"])
def delete_item(item_upc):
  return item_upc

@app.route('/api/checkout/expected', methods=["GET"])
def expected_delivery():
  cur = conn.get_cursor()
  cur.execute("SELECT COUNT(delivereddate) FROM Purchase")
  pending = cur.fetchone()['COUNT(delivereddate)']
  expected = pending/10
  expect_date = str(date.today()+timedelta(days=expected))
  return expect_date

