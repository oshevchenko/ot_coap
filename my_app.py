#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, session, request, Response, send_from_directory, render_template, jsonify
from flask_cors import cross_origin

from app_db import app_db
db = app_db('myApp.db')

app = Flask(__name__, template_folder='templates')
app.secret_key = 'ASA:VTMJI~ZvPOS8W:0L2cAb?WB}R0V_'

origins_domains = '*'

##############################
# Static files
############################## 
@app.route('/frontend/')
def send_frontend_index():
	return send_from_directory('frontend/', 'index.html')

@app.route('/frontend/<path:path>')
def send_frontend_files(path):
	return send_from_directory('frontend/', path)

##############################
# Main Page
##############################
@app.route('/', methods=['GET'])
def home_page():
	return render_template('index.html'), 200


##############################
# CRUD routes for any model
##############################
@app.route('/<string:model>/', methods=['POST'])
@cross_origin(origins=origins_domains)
def client_create(model):
	return jsonify(db.getModel(model).create(request.json)), 200

@app.route('/<string:model>/', methods=['GET'])
@cross_origin(origins=origins_domains)
def client_read_all(model):
	return jsonify(db.getModel(model).read()), 200

@app.route('/<string:model>/<int:id>/', methods=['GET'])
@cross_origin(origins=origins_domains)
def client_read(model, id):
	return jsonify(db.getModel(model).read(id)), 200

@app.route('/<string:model>/<int:id>/', methods=['PUT'])
@cross_origin(origins=origins_domains)
def client_update(model, id):
	return jsonify(db.getModel(model).update(id, request.json)), 200

@app.route('/<string:model>/<int:id>/', methods=['DELETE'])
@cross_origin()
def client_delete(model, id):
	return jsonify(db.getModel(model).delete(id)), 200

##############################
# Error Pages
##############################

@ app.errorhandler(404)
def err_404(error):
	return render_template('error.html', message='Page not found'), 404

@ app.errorhandler(500)
def err_500(error):
	return render_template('error.html', message='Internal server error'), 500

##############################
# Logging configure
##############################
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('log/my_app.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('startup')

##############################
# Run app
##############################

if __name__ == '__main__':
	app.run(host='0.0.0.0')

