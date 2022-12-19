from flask import render_template,request, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
import pandas as pd


url_object = URL.create(
    "postgresql",
    username="lotus",
    password="lotus",
    host="localhost",
    port="5433",
    database="lotusdb")

engine = create_engine(url_object)
session = Session(engine)


core = Blueprint('core', __name__)

@core.route('/')
def index():

    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/xuat_hang')
def xuat_hang():
    query = """ 
    SELECT ma_san_pham, so_lo_ma_lo, ma_kho_tinh_trang, SUM(so_luong_xuat) AS so_luong
        FROM misa
        GROUP BY ma_san_pham, so_lo_ma_lo, ma_kho_tinh_trang
        HAVING SUM(so_luong_xuat) > 0
        ORDER BY ma_kho_tinh_trang
    """
    df = pd.read_sql_query(query, engine)  
    df['so_luong'] = df['so_luong'].astype(int)

    rows = df.values.tolist()
    column_names = df.columns.values


    return render_template('xuat_hang.html', rows=rows, column_names=column_names)