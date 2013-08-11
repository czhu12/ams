from flask import Flask, session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_really_that_secretive'

from app import views

