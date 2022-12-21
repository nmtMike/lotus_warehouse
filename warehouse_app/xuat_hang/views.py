from flask import render_template, Blueprint
import pandas as pd
from warehouse_app.models import engine

xuat_hang = Blueprint('xuat_hang', __name__)

@xuat_hang.route('/soan_hang')
def soan_hang():
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
    return render_template('danh_sach_soan_hang.html', rows=rows, column_names=column_names)