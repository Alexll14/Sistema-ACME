from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '6e04daf1f05946a9039cf78bc82427b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acme.db'

database = SQLAlchemy(app)

from acme import routes