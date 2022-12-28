from flask import render_template, Blueprint, request
import pandas as pd
from warehouse_app.function import add_modi_info, update_don_hang_xuat
from warehouse_app.models import engine

xuat_hang = Blueprint('xuat_hang', __name__)

@xuat_hang.route('/xac_nhan_don', methods=['GET', 'POST'])
def xac_nhan_don():
    query = """ 
    SELECT *
        FROM don_hang_xuat
        WHERE latest_status = 'xac_nhan_don'
    """
    df = pd.read_sql_query(query, engine)
    rows = df[['ngay', 'ma_don_hang', 'ma_khach_hang', 'dien_giai_chung', 'dia_chi_giao_hang', 'updator', 'updated_time', 'id_don_hang_xuat']].values.tolist()
    column_names = df.columns.values
    id_list = df['id_don_hang_xuat'].tolist()

    if request.method == 'POST':
        id_checked = request.form.getlist('id_don_hang')
        df = pd.DataFrame({'id_chi_tiet_don_hang':id_checked})

        # add footprint
        df['status'] = 'xac_nhan_soan_hang'
        add_modi_info(df)

        # update to transaction_xuat table
        df.to_sql('transaction_xuat', engine, if_exists='append', index=False)

        update_don_hang_xuat(new_status="'xac_nhan_soan_hang'", id_don_hang_s=id_checked)

        return render_template('transaction_confirmed.html')

    return render_template('don_hang_can_soan.html', len=len(rows), rows=rows, column_names=column_names, id_list=id_list)


@xuat_hang.route('/huy_xac_nhan_don', methods=['GET', 'POST'])
def huy_xac_nhan_don():
    query = """ 
    SELECT *
        FROM don_hang_xuat
        WHERE latest_status = 'xac_nhan_soan_hang'
    """
    df = pd.read_sql_query(query, engine)
    rows = df[['ngay', 'ma_don_hang', 'ma_khach_hang', 'dien_giai_chung', 'dia_chi_giao_hang', 'updator', 'updated_time', 'id_don_hang_xuat']].values.tolist()
    column_names = df.columns.values
    id_list = df['id_don_hang_xuat'].tolist()

    if request.method == 'POST':
        id_checked = request.form.getlist('id_don_hang')
        df = pd.DataFrame({'id_chi_tiet_don_hang':id_checked})

        # add footprint
        df['status'] = 'xac_nhan_don'
        add_modi_info(df)

        # update to transaction_xuat table
        df.to_sql('transaction_xuat', engine, if_exists='append', index=False)

        update_don_hang_xuat(new_status="'xac_nhan_don'", id_don_hang_s=id_checked)

        return render_template('transaction_confirmed.html')

    return render_template('don_hang_can_soan.html', len=len(rows), rows=rows, column_names=column_names, id_list=id_list)



@xuat_hang.route('/danh_sach_soan_hang')
def danh_sach_soan_hang():
    query = """
    SELECT ma_san_pham, ten_san_pham, so_lo_ma_lo, don_vi_tinh, SUM(so_luong) AS so_luong
        FROM chi_tiet_don_hang_xuat ctdhx
        LEFT JOIN san_pham sp USING(id_san_pham)
        LEFT JOIN don_hang_xuat dhx USING(id_don_hang_xuat)
        WHERE dhx.latest_status = 'xac_nhan_soan_hang'
        GROUP BY ma_san_pham, ten_san_pham, so_lo_ma_lo, don_vi_tinh
    """
    df = pd.read_sql_query(query, engine)
    rows = df[['ma_san_pham', 'ten_san_pham', 'so_lo_ma_lo', 'don_vi_tinh', 'so_luong']].values.tolist()
    column_names = df.columns.values

    return render_template('danh_sach_soan_hang.html', len=len(rows), rows=rows, column_names=column_names)