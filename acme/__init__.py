from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '6e04daf1f05946a9039cf78bc82427b2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acme.db'

database = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_admin'
login_manager.login_message_category = 'alert-info'

from acme import routes