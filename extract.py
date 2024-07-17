import pandas as pd
from sqlalchemy import create_engine
from config import load_config
import pandas as pd 
from sqlalchemy import create_engine

def connect_to_db(config):
    # Connect to Postgres database
    connection_string = f'{config["dialect"]}+{config["driver"]}://{config["username"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database_name"]}'
    engine = create_engine(connection_string)
    conn = engine.connect()
    return conn

def extract_vietnamese_administrative_units_data_from_db():

    # Connect to database
    config = load_config()
    conn = connect_to_db(config)

    # Extract data from database
    VN_address_df = pd.read_sql(
        'SELECT p.name, p.full_name, d.name, d.full_name, w.name, w.full_name\
        FROM wards as w, districts as d, provinces as p \
        WHERE w.district_code = d.code AND d.province_code = p.code'
        , con=conn
    )
    # Close connection
    conn.close()

    return VN_address_df


# Extract data raw address data from csv, excel
# if __name__ == '__main__':
    extract_vietnamese_administrative_units_data_from_db()