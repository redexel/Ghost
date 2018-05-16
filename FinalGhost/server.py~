#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	usuario = db.Column(db.String(20))
	contrasena = db.Column(db.String(20))


@app.route('/')
def index():
	return render_template('login.html')

@app.route('/insert/default')
def insert_default():
	new_post = Posts(id="50")
	db.session.add(new_post)
	db.session.commit()
	return "The default post was created."

@app.route('/select/default')
def select_default():
	post = Posts.query.filter_by(id="50").first()
	print(post.id)
	return "Query Done."

	
if __name__=='__main__':
	db.create_all()
	app.run(debug=True)


