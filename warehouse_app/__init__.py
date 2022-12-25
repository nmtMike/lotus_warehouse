# warehouse_app/__init__.py
from flask import Flask

app = Flask(__name__)


from warehouse_app.core.views import core
from warehouse_app.xuat_hang.views import xuat_hang
from warehouse_app.nhap_hang.views import nhap_hang
app.register_blueprint(core)
app.register_blueprint(xuat_hang)
app.register_blueprint(nhap_hang)