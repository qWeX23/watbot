from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy 

import json


from models import db

db.create_all()

with open("connections.json",'r') as file:
    connections =  json.loads(file.read())
    app.config['SQLALCHEMY_DATABASE_URI'] = connections['connectionString']