from flask import render_template,request, Blueprint, redirect, url_for
import pandas as pd
from warehouse_app.models import engine, session
from warehouse_app.function import misa_column_check, misa_constraints_check, add_modi_info, misa_process

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/xuat_hang')
def xuat_hang():
    return render_template('xuat_hang.html')


@core.route('/nhap_hang')
def nhap_hang():
    return render_template('nhap_hang.html')


@core.route('/misa_request', methods=['GET', 'POST'])
def misa_request():
    if request.method == 'POST':
        f = request.files['file']
        f_name = f.filename
        err_list = []
        
        if f_name:
            try: df = pd.read_excel(request.files.get('file'))
            except: 
                err_list.append('Must be Excel file')
                return render_template('misa_refuse.html', err_list=err_list)

            if misa_column_check(df) and misa_constraints_check(df, err_list):
                add_modi_info(df)
                df.to_sql('tmp_misa', engine, if_exists='replace', index=False)
                return redirect(url_for('core.misa_uploaded'))
            else:
                return render_template('misa_refuse.html', err_list=err_list) 
    return render_template('misa.html')



@core.route('/misa_uploaded', methods=['GET', 'POST'])
def misa_uploaded():
    query = """
    SELECT *
        FROM tmp_misa
    """
    df = pd.read_sql_query(query, engine)
    rows = df.values.tolist()
    column_names = df.columns.values
    return render_template('misa_uploaded.html', rows=rows, column_names=column_names)



@core.route('/misa_confirmed', methods=['GET', 'POST'])
def misa_confirmed():
    query = """SELECT * FROM tmp_misa """

    # write new rows to misa table
    df = pd.read_sql_query(query, engine)
    df.to_sql('misa', engine, if_exists='append', index=False)

    # # delete tmp table after use
    # delete_query = """ DELETE FROM tmp_misa """
    # session.execute(delete_query)
    # session.commit()

    # call misa process
    misa_process()
    
    return render_template('transaction_confirmed.html')