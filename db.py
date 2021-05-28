import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """

    c = conn.cursor()
    create_table_sql = """ CREATE TABLE IF NOT EXISTS SCORES (
                                     name text PRIMARY KEY,
                                     score integer NOT NULL
                                 ); """
    c.execute(create_table_sql)


def insert_row(conn, value):
    """
    Create a new row
    :param conn:
    :param value:
    :return:
    """

    sql = ''' INSERT or REPLACE into SCORES(name,score) VALUES (?,?) '''
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()


def get_all_rows(conn):
    """
    getting all rows from score table
    :param conn:
    :return: all the rows
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM scores where score > 0 Order  by score DESC limit 5")
    rows = cur.fetchall()
    return rows






