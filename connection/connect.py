import psycopg2
from .config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connecting to the PostgreSQL server
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    config = load_config()
    connect(config)