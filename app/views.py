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

@app.route('/api/price', methods=["GET"])
def price_request():
	items = json.loads(request.args['arr'])
	if is_valid(items):
		return str(price(items))
	else:
		return 'Invalid input'

@app.route('/api/store_purchase', methods=["POST"])
def purchase():
	cur = conn.get_cursor()
	today = str(date.today())
	items = json.loads(request.form['arr'])
	return str(items)

	if not is_valid(items):
		return 'Invalid input'

	# Check if quantity legal for online purchase
	if request.form.has_key('customer'):
		for item in items:
			cur.execute("SELECT stock FROM item WHERE Item.upc = %s", str(item['upc']) )
			if cur.fetchone()['stock'] < item['quantity']:
				conn.con.commit()
				return "Illegal quantity for item " + str(item['upc'])

	# Insert into Purchase
	if request.form.has_key('credit'):
		credit = json.loads(request.form['credit'])
		insert_args = (today, str(credit['cardnum']), str(credit['expirydate']) )
		cur.execute("INSERT INTO Purchase (purchasedate, cardnum, expirydate) VALUES (%s,%s,%s)", insert_args)
	else:
		cur.execute("INSERT INTO Purchase (purchasedate) VALUES (%s)", today) 

	cur.execute("SELECT last_insert_id()")
	pid = str(cur.fetchone()['last_insert_id()'])
	purchase_item(cur, pid, items)
	conn.con.commit()

	# Receipt Preparation
	cur.execute("select * from purchase, purchaseitem, item where purchase.receiptid=%s and purchase.receiptid=purchaseitem.receiptid and purchaseitem.upc = item.upc", pid)
	conn.con.commit()

	context = {}
	context['purhcaseitems'] = stringify(cur.fetchall())
	context['price'] = str(price(items))
	context['date'] = str(today)
	context['pid'] = str(pid)
	if request.form.has_key('credit'):
		context['cardnum'] = str(credit['cardnum'])[-5:]

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
	curr.execute("select purchasedate, cardnum from purchase where receiptid= %s", receiptid)
	purchase_info = curr.fetchone()
	diff = today - purchase_info['purchasedate']

	if diff.days > 15:
		conn.con.commit()
		return "Receipt expired"

	# Check if quantity is legal
	curr.execute("select upc,quantity from purchaseitem where receiptid= %s", receiptid)
	purchased_items = {}
	for item in curr.fetchall():
		purchased_items[item['upc']] = item['quantity']

	curr.execute("select upc,sum(quantity) from returnitem,returntable where receiptid= %s GROUP BY upc", receiptid)
	returned_items = {}
	for item in curr.fetchall():
		returned_items[item['upc']] = item['sum(quantity)']
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
	curr.execute("INSERT INTO Returntable (receiptid, returndate) VALUES (%s, %s)", (receiptid, str(today)) )
	for item in items:
		curr.execute("INSERT INTO returnitem (select last_insert_id(),%s,%s)", (str(item['upc']), str(item['quantity'])))
		curr.execute("UPDATE Item SET stock = stock+%s WHERE upc = %s", (str(item['quantity']), str(item['upc'])))
	conn.con.commit()

	# Return message
	if purchase_info['cardnum']:
		return "Return Processed, credit $" + str(total) + " to credit card ***********" + purchase_info['cardnum'][-5:]

	return "Return Processed, return $" + str(total) + " in cash"

def purchase_item(cur, items, pid):
	for item in items:
		cur.execute( "INSERT INTO Purchaseitem %s ,%s, %s)", (pid, str(item['upc']), str(item['quantity'])) )
		cur.execute( "UPDATE Item SET stock = stock-%s WHERE upc = %s", (str(item['quantity']), str(item['upc'])) )

def is_valid(items):
	for item in items:
		if len(str(item['upc'])) > 10 or len(str(item['quantity']))> 10:
			return False;
	return has_items(items)

def has_items(items):
	curr = conn.get_cursor()
	for item in items:
		curr.execute("select * from item where upc=%s", str(item['upc']) )
		if not curr.fetchall():
			conn.con.commit()
			return False
	conn.con.commit()
	return True

def price(items):
	curr = conn.get_cursor()
	total = 0
	for item in items:
		curr.execute("select price from item where upc=%s", str(item['upc']) )
		price = curr.fetchone()['price']
		total += price*item['quantity']
	conn.con.commit()
	return total

def stringify(items):
	for item in items:
		for attribute in item.keys():
			if item[attribute]:
				item[attribute] = str(item[attribute])
			else:
				item[attribute] = 'NULL'
	return items

"""Henry's Code End"""

@app.route('/api/items', methods=["GET"])
def get_items():
  return jsonify({ "data": stringify(conn.read("SELECT * FROM Item")) })

@app.route('/api/items/<item_upc>', methods=["GET"])
def get_item(item_upc):
  curr = conn.get_cursor()
  curr.execute("SELECT * FROM Item WHERE upc = %s", item_upc)
  conn.con.commit()
  return jsonify({ "data": stringify(curr.fetchall()) })


@app.route('/api/items/<item_upc>', methods=["PUT"])
def update_item(item_upc):
  return item_upc

@app.route('/api/items/<item_upc>', methods=["DELETE"])
def delete_item(item_upc):
  return item_upc

@app.route('/api/items/purchase', methods=["POST"])
def purchase_item(item_upc):
  return item_upc

@app.route('/api/checkout/expected', methods=["GET"])
def expected_delivery():
  cur = conn.get_cursor()
  cur.execute("SELECT COUNT(delivereddate) FROM Purchase")
  pending = cur.fetchone()['COUNT(delivereddate)']
  expected = pending/10
  expect_date = str(date.today()+timedelta(days=expected))
  return expect_date

