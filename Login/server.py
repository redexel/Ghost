#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

ghost=Flask(__name__, template_folder='templates/')

@ghost.route('/')

def index():
	return render_template('login.html')
	
if __name__=='__main__':
	ghost.run(debug=True, port=8800);
