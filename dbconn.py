import sqlite3


def dbconnect(db_file):
    db_conn = None
    try:
        db_conn = sqlite3.connect(db_file)
        return db_conn
    except sqlite3.Error as e:
        print(e)  # TODO: replace with proper error logging code

    return db_conn
