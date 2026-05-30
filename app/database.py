import sqlite3
from sqlite3 import Error

DATABASE_FILE = "app/data/reservations.db"

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement """
    try:
        sql_create_reservations_table = """ CREATE TABLE IF NOT EXISTS reservations (
                                        id integer PRIMARY KEY,
                                        plate text NOT NULL,
                                        vin text NOT NULL,
                                        phone text NOT NULL,
                                        status text NOT NULL,
                                        timestamp text NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_reservations_table)
    except Error as e:
        print(e)

def create_reservation(conn, reservation):
    """
    Create a new reservation into the reservations table
    :param conn:
    :param reservation:
    :return: project id
    """
    sql = ''' INSERT INTO reservations(plate,vin,phone,status,timestamp)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reservation)
    conn.commit()
    return cur.lastrowid

def get_all_reservations(conn):
    """
    Query all rows in the reservations table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM reservations")
    rows = cur.fetchall()
    return rows

def init_db():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    init_db()
