import sys
import psycopg2


def postgres_connection(username, password, port, database, hostname):
    """
    Returns Postgres_connection object
    """
    try:
        pgre_conn = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=port)
        return pgre_conn
    except psycopg2.OperationalError as _:
        print('Unable to connect to postgres!')
        sys.exit(1)
