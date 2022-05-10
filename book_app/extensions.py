from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from book_app.config import Config
import flask_bcrypt
import os

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from book_app.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

bcrypt = flask_bcrypt.Bcrypt(app)

###########################
# Authentication
###########################

# TODO: Add authentication setup code here!



