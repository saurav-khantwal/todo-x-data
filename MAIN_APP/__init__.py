from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:prototype@localhost/TODO'

else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://iczafidiqrxser:b2e6e6e1d43d0ca5d29d2e5cd25287823d72fdc746e78cb2bdf02f0faf0f2de4@ec' \
                                     '2-3-229-8-233.compute-1.amazonaws.com:5432/d1occs2h6gn0ln'

app.config['SECRET_KEY'] = '5252ff2ac905b9acd329d6e2'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from MAIN_APP import routes

