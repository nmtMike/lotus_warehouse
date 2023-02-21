# warehouse_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecret'


############################
### DATABASE SETUP ##########
########################
url_object = URL.create(
    "postgresql",
    username="lotus",
    password="lotus",
    host="localhost",
    port="5433",
    database="lotusdb")
app.config['SQLALCHEMY_DATABASE_URI'] = url_object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



##################################################
from warehouse_app.core.views import core
from warehouse_app.xuat_hang.views import xuat_hang
from warehouse_app.nhap_hang.views import nhap_hang
app.register_blueprint(core)
app.register_blueprint(xuat_hang)
app.register_blueprint(nhap_hang)