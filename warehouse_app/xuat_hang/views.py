from flask import render_template, Blueprint, request
import pandas as pd
from warehouse_app.models import engine

xuat_hang = Blueprint('xuat_hang', __name__)

@xuat_hang.route('/soan_hang', methods=['GET', 'POST'])
def soan_hang():
    query = """ 
    SELECT *
        FROM don_hang_xuat
    """
    df = pd.read_sql_query(query, engine)
    rows = df.values.tolist()
    column_names = df.columns.values
    id_list = df['id'].tolist()

    if request.method == 'POST':
        id_checked = request.form.getlist('id_don_hang')
        return f'imported, {id_checked}'

    return render_template('danh_sach_soan_hang.html', len=len(rows), rows=rows, column_names=column_names, id_list=id_list)


