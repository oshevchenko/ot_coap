#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, session, request, Response, send_from_directory, render_template, jsonify
from flask_cors import cross_origin

from app_db import app_db
db = app_db('myApp.db')


##############################
# Logging configure
##############################
##############################
# Run app
##############################

if __name__ == '__main__':
	while True:
		pass

