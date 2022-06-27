import aiosqlite
from dbconn import dbconnect
import codecs
import logging
import asyncio


async def dbcreate(debug=True):
    # starting logger
    logger = logging.getLogger('log')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)
    file_logger = logging.FileHandler('errorLog.log', 'a')
    file_logger.setLevel(logging.ERROR)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)

    db_conn = await dbconnect("database/DB.db", logger)

    # add here when adding commands
    commands = ["tableflip", "gitgud", "heresy"]

    commands_create_sql = []
    for command in commands:
        commands_create_sql.append(f""" CREATE TABLE IF NOT EXISTS {command} (
                                    id integer PRIMARY KEY,
                                    response text NOT NULL
                                    ); """)  # TODO maybe switch this to a dictionary so I can debug it by command

    try:
        # remove old tables
        for command in commands:
            await db_conn.execute(f"DROP TABLE IF EXISTS {command}")

        # create new tables
        for command in commands_create_sql:
            await db_conn.execute(command)

        # insert data from files to table
        for command in commands:
            with codecs.open(f"commands/{command}.txt", encoding="utf-8") as f:
                print(f"opened commands/{command}.txt")
                data = f.readlines()
                for line in data:
                    await db_conn.execute(f'INSERT INTO {command} (id, response) VALUES ({data.index(line)}, "{line}")')

        await db_conn.commit()

        if debug:  # show our work in the console
            for command in commands:
                check = await db_conn.execute(f"SELECT * FROM {command}")
                rows = await check.fetchall()
                for row in rows:
                    logger.debug(f"{command} ID: {row[0]} - Response: {row[1]}")

    except aiosqlite.Error as e:
        logger.error(e)

if __name__ == '__main__':
    asyncio.run(dbcreate())
