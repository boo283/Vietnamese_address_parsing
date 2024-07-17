import config
import psycopg2


def connect_to_postgres(config):    
    # Load configuration
    try:
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL")
            return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    config = config.load_config()
    conn = connect_to_postgres(config)
