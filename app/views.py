from app import app
from db import db_con
from flask import render_template, make_response, jsonify


conn = db_con.Database()

@app.route('/')
@app.route('/index')
def index():
  response = make_response(render_template("index.html"))
  return response

@app.route('/api/songs', methods=["GET"])
def get_songs():
  return jsonify({ "songs": conn.read("SELECT * FROM Songs") })

@app.route('/api/songs/<item_upc>', methods=["GET"])
def get_song():
  return jsonify({ "songs": conn.read("SELECT * FROM Songs") })

@app.route('/api/songs/<item_upc>', methods=["POST"])
def add_song(item_upc):
  return item_upc

@app.route('/api/songs/<item_upc>', methods=["PUT"])
def update_song(item_upc):
  return item_upc

@app.route('/api/songs/<item_upc>', methods=["DELETE"])
def delete_song(item_upc):
  return item_upc

@app.route('/api/songs/purchase', methods=["POST"])
def purchase_song(item_upc):
  return item_upc

