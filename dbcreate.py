import sqlite3
from dbconn import dbconnect
import codecs

db_conn = dbconnect('database/commandsDB.db')

# add here when adding commands
commands = ["tableflip", "gitgud", "heresy"]

commands_create_sql = []
for command in commands:
    commands_create_sql.append(f""" CREATE TABLE IF NOT EXISTS {command} (
                                id integer PRIMARY KEY,
                                response text NOT NULL
                                ); """)  # TODO maybe switch this to a dictionary so I can debug it by command

try:
    c = db_conn.cursor()

    # remove old tables
    for command in commands:
        c.execute(f"DROP TABLE IF EXISTS {command}")

    # create new tables
    for command in commands_create_sql:
        c.execute(command)

    # insert data from files to table
    for command in commands:
        with codecs.open(f'commands/{command}.txt', encoding='utf-8') as f:
            print(f"opened commands/{command}.txt")
            data = f.readlines()
            for line in data:
                c.execute(f'INSERT INTO {command} (id, response) VALUES ({data.index(line)}, "{line}")')

    db_conn.commit()

    # show our work in the console
    for command in commands:
        check = c.execute(f'SELECT * FROM {command}')
        for row in check:
            print(f"{command} ID: {row[0]} - Response: {row[1]}")



except sqlite3.Error as e:
    print(e)

