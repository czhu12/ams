from app import app
from db import db_con
from flask import render_template, make_response, jsonify


conn = db_con.Database()

@app.route('/')
@app.route('/index')
def index():
  response = make_response(render_template("index.html"))
  return response

@app.route('/api/items', methods=["GET"])
def get_items():
  return jsonify({ "items": conn.read("SELECT * FROM Songs") })

@app.route('/api/items/<item_upc>', methods=["GET"])
def get_item():
  return jsonify({ "items": conn.read("SELECT * FROM Songs") })

@app.route('/api/items/<item_upc>', methods=["PUT"])
def update_item(item_upc):
  return item_upc

@app.route('/api/items/<item_upc>', methods=["DELETE"])
def delete_item(item_upc):
  return item_upc

@app.route('/api/items/purchase', methods=["POST"])
def purchase_item(item_upc):
  return item_upc

