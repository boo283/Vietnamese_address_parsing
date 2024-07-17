import config
import psycopg2
import pyodbc
import urllib
from sqlalchemy import create_engine

def connect_to_postgres(config):    
    # Load configuration
    try:
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL")
            return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def connect_to_mssql():
    try:
        params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=BOO\\BOO,1433;"
        "DATABASE=vietnamese_administrative_units;"
        "UID=boo283;"
        "PWD=123"
    )

        # Construct the connection string for SQLAlchemy
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

        # Create the SQLAlchemy engine without specifying schema
        engine = create_engine(connection_string)
        print("Connected to MSSQL successfully")
    except (Exception, pyodbc.DatabaseError) as error:
        print(error)

    return engine

if __name__ == '__main__':
    config = config.load_postgres_config()
    #conn = connect_to_postgres(config)
    #engine = connect_to_mssql()
