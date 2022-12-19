# warehouse_app/__init__.py
from flask import Flask

app = Flask(__name__)


from warehouse_app.core.views import core
app.register_blueprint(core)