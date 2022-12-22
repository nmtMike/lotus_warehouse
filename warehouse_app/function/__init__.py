import pandas as pd
from warehouse_app.models import engine

def misa_check(df:pd.DataFrame):
    """check wether the uploaded file meets the Misa template
    """

    query = """
    SELECT *
        FROM misa
        LIMIT 0
    """
    misa_cols = pd.read_sql_query(query, engine).columns
    try: 
        if sum(df.columns == misa_cols) == len(misa_cols):
            return True
    except:
        return False