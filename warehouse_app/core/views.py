from flask import render_template,request, Blueprint, redirect, url_for
import pandas as pd

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
def misa():
    if request.method == 'POST':
        f = request.files['file']
        f_name = f.filename
        if f_name:
            df = pd.read_excel(request.files.get('file'))
            return render_template('misa_uploaded.html', f_name=f_name)

    return render_template('misa.html')

# @core.route('/misa_uploaded', methods=['POST'])
# def misa_uploaded():
#     if request.method == 'POST':
#         f = request.files['file']
#         return render_template('misa_uploaded.html')