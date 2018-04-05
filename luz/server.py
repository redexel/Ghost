#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = 'esto-es-una-clave-muy-secreta'


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)


@app.route('/', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(username=request.form["username"]).first()
		if user and check_password_hash(user.password, request.form["password"]):
			##la idea es que ueses esta variable para consultar si esta logueado
			## como???? preguntando si session['logueado'] == "si"  puede entrar
			session['logueado'] = "si"
			session['userlogueado'] = request.form["username"]

			return "Has iniciado sesion "
		return "Tus credenciales son invalidas,revisa e intenta nuevamente"
	return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == "POST":	
		hashed_pw = generate_password_hash(request.form["password"], method="sha256")
		new_user = Users(username=request.form["username"], password=hashed_pw)
		db.session.add(new_user)
		db.session.commit()
		return "Has sido registrado correctamente"
	return render_template("signup.html")	

@app.route('/select/default')
def select_default():
	post = Posts.query.filter_by(id="50").first()
	print(post.id)
	return "Query Done."

	
if __name__=='__main__':
	db.create_all()
	app.run(debug=True, host='0.0.0.0')

