from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'   #adding key value Uniqe Resource Identifier
app.config['SECRET_KEY'] = '94c3ae1b155f0f321b76f852'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  #for Crypting Passwords of user

login_manager = LoginManager(app)  #Builtin Library for Managing Login of Users
login_manager.login_view = "login"
login_manager.login_message_category = 'info'

from market import routes             #imported all route into init file