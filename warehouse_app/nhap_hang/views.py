from flask import render_template,request, Blueprint, redirect, url_for
import pandas as pd
from warehouse_app.models import engine, session
from warehouse_app.function import misa_check, add_modi_info, misa_process

nhap_hang = Blueprint('nhap_hang', __name__)


@nhap_hang.route('/kiem_tra_hang_nhap')
def kiem_tra_hang_nhap():

    return 'kiem tra hang nhap'