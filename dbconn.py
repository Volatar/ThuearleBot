import sqlite3


def dbconnect(db_file, logger):
    db_conn = None
    try:
        db_conn = sqlite3.connect(db_file)
        return db_conn
    except sqlite3.Error as e:
        logger.error(e)

    return db_conn
