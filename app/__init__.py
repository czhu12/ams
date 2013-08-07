from flask import Flask, session
from db import db_con


app = Flask(__name__)

from app import views

conn = db_con.Database()

def current_user():
  return conn.read("SELECT FROM Users WHERE user_id = %s" % (session['userid']))
