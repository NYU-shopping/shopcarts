"""
Microservice module
This module contains the microservice code for
    server
    models
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# These next lines are positional:
# 1) We need to create the Flask app
# 2) Then configure it
# 3) Then initialize SQLAlchemy after it has been configured

app = Flask(__name__)
# Load the confguration
app.config.from_object('config')
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

# Initialize SQLAlchemy
db = SQLAlchemy(app)