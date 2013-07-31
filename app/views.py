from app import app
from app import db
from flask import render_template, make_response

@app.route('/')
@app.route('/index')
def index():
  response = make_response(render_template("index.html"))
  return response

@app.route('/songs', methods=["GET", "POST", "PUT", "DELETE"])
def rest_songs():
  return db.test()



  
