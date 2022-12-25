import pandas as pd
from warehouse_app.models import engine, session

def misa_check(df:pd.DataFrame):
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


    DELETE
        FROM misa
        WHERE substring(ma_don_hang, 1, 2) IN ('BH', 'BT');
    """

    session.execute(don_hang_xuat)
    session.commit()