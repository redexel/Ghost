#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask import json

import os


dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__, static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = 'esto-es-una-clave-muy-secreta'


class Users(db.Model):
	id_user = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	profile = db.Column(db.Integer, nullable=False)

class Scan(db.Model):
	id_scan = db.Column(db.Integer, primary_key=True)
	ssid = db.Column(db.String(50),  nullable=False)
	channel = db.Column(db.String(50),  nullable=False)
	encryption = db.Column(db.String(50), nullable=False)
	ssid_password = db.Column(db.String(50),  nullable=False)
	date = db.Column(db.String(50), nullable=False)
	id_user1 = db.Column(db.Integer, nullable=False)
	

@app.route('/', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(username=request.form["username"]).first()
		if user and check_password_hash(user.password, request.form["password"]):
			session['logueado'] = "si"
			session['userlogueado'] = request.form["username"]
			return redirect("/dashboard")
		return "Tus credenciales son invalidas,revisa e intenta nuevamente"
	return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
	if request.method == "POST":	
		hashed_pw = generate_password_hash(request.form["password"], method="sha256")
		new_user = Users(username=request.form["username"], password=hashed_pw, profile=request.form["profile"])
		db.session.add(new_user)
		db.session.commit()
		return "Has sido registrado correctamente"
	return render_template("signup.html")	

@app.route('/dashboard' , methods=["GET", "POST"])
def dashboard():
	if session:
		return render_template("dashboard.html")
	return redirect("/error")

@app.route('/results')	
def results():
	if session:
		data=[]
		with open('cracked.csv','r') as f:
			for i in f.readlines():
				row=i.split(',')
				target=dict()
				target['BSSID']=row[0]
				target['CIPHER']=row[1]
				target['ESSID']=row[2]
				target['PASSWORD']=row[3]
				data.append(target)
		return app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype="application/json"
		)
		
		 	
	#return redirect("/error")

@app.route('/error')
def error():
	return render_template("error.html")

@app.route('/tabla')
def tabla():
	return render_template("tabla.html")

@app.route('/tables')
def tables():
	return render_template("tables.html")



	
if __name__=='__main__':
	db.create_all()
	app.run(debug = True, port = 5000)
