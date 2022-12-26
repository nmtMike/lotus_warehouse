import pandas as pd
from warehouse_app.models import engine, session

def misa_column_check(df:pd.DataFrame):
    """check wether the uploaded file meets the Misa template: \n
    - Check PK constraints
    """

    query = """
    SELECT *
        FROM misa
        LIMIT 0
    """
    misa_cols = pd.read_sql_query(query, engine).columns[:-2]
    try: 
        if sum(df.columns == misa_cols) == len(misa_cols):
            return True
    except:
        return False

def misa_constraints_check(df:pd.DataFrame, existed_err:list = []):
    err_list = []

    # check NULL and data type
    if df.dtypes['ngay'] != 'datetime64[ns]':
        err_list.append('Sai định dạng cột "Ngày"')
    if df.dtypes['han_su_dung'] != 'datetime64[ns]':
        err_list.append('Sai định dạng cột "Hạn sử dụng"')
    if df['ma_don_hang'].isnull().sum() > 0:
        err_list.append('"Mã đơn hàng" không được trống')
    if df['ma_khach_hang'][df['ma_don_hang'].str[:2].isin(['BH', 'BT'])].isnull().sum() > 0:
        err_list.append('"Mã khách hàng" trong đơn bán không được trống')
    if df['ma_san_pham'].isnull().sum() > 0:
        err_list.append('"Mã sản phẩm" không được trống')
    if df['so_lo_ma_lo'].isnull().sum() > 0:
        err_list.append('"Số lô mã lô" không được trống')
    
    # check ma_don_hang xuat
    query = """ SELECT ma_don_hang FROM don_hang_xuat """
    ma_don_hang_existed = pd.read_sql_query(query, engine)['ma_don_hang']
    ma_don_hang_existed = df[df['ma_don_hang'].isin(ma_don_hang_existed)]['ma_don_hang']
    ma_don_hang_existed = ma_don_hang_existed.tolist()
    if len(ma_don_hang_existed) > 0:
        err_list.append(f'mã đơn hàng xuất đã tồn tại: {ma_don_hang_existed}')


    if len(err_list) == 0:
        return True
    else: 
        for err in err_list:
            existed_err.append(err)
        return False
    



def add_modi_info(df:pd.DataFrame):
    """add "updator" and "updated_time columns with user name and current time"
    """
    df['updator'] = 'user'
    df['updated_time'] = pd.Timestamp.now()
    return None


def misa_process():
    """This process must be called after new Misa request has been uploaded \n
    This process will update tables: \n
    - "don_hang_xuat"
    - "don_hang_chuyen"
    - "don_hang_nhap"
    - "san_pham"
    """

    # move rows from misa to don_hang_xuat
    don_hang_xuat = """
    INSERT INTO don_hang_xuat
    SELECT DISTINCT ngay, ma_don_hang, dien_giai_chung, 
            ma_khach_hang, dia_chi_giao_hang,
            updator, updated_time
        FROM misa
        WHERE substring(ma_don_hang, 1, 2) IN ('BH', 'BT');
        
        
    INSERT INTO san_pham
    SELECT DISTINCT ma_san_pham, ten_san_pham, dvt AS don_vi_tinh, "nhom_VTHH", '' AS nha_san_xuat, so_lo_ma_lo, han_su_dung
        FROM misa
        WHERE (ma_san_pham, so_lo_ma_lo) NOT IN (SELECT ma_san_pham, so_lo_ma_lo FROM san_pham);


    INSERT INTO don_hang_xuat
    SELECT DISTINCT ngay, ma_don_hang, dien_giai_chung, ma_khach_hang, dia_chi_giao_hang, updator, updated_time
        FROM misa
        WHERE (ma_don_hang, ma_khach_hang) NOT IN (SELECT ma_don_hang, ma_khach_hang FROM don_hang_xuat)
            AND substring(ma_don_hang, 1, 2) IN ('BH', 'BT');


    DELETE
        FROM misa
        WHERE substring(ma_don_hang, 1, 2) IN ('BH', 'BT');
    """

    session.execute(don_hang_xuat)
    session.commit()