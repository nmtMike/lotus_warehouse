from flask import render_template,request, Blueprint, redirect, url_for
import pandas as pd
from warehouse_app.models import engine
from warehouse_app.function import misa_check

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


@core.route('/misa_request', methods=['GET', 'POST'])
def misa_request():
    if request.method == 'POST':
        f = request.files['file']
        f_name = f.filename
        
        if f_name:
            try: df = pd.read_excel(request.files.get('file'))
            except: return render_template('misa_refuse.html')

            if misa_check(df):
                df.to_sql('tmp', engine, if_exists='replace', index=False)
                return redirect(url_for('core.misa_uploaded'))
            else:
                return render_template('misa_refuse.html') 
    return render_template('misa.html')

@core.route('/misa_uploaded', methods=['GET', 'POST'])
def misa_uploaded():
    query = """
    SELECT *
        FROM tmp
    """
    df = pd.read_sql_query(query, engine)
    rows = df.values.tolist()
    column_names = df.columns.values
    return render_template('misa_uploaded.html', rows=rows, column_names=column_names)

@core.route('/misa_confirmed', methods=['GET', 'POST'])
def misa_confirmed():
    query = """
    SELECT *
        FROM tmp
    """
    pd.read_sql_query(query, engine).to_sql('misa', engine, if_exists='append', index=False)
    return render_template('misa_confirmed.html')