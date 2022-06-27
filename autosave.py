import aiosqlite
import discord
import asyncio
import logging
import codecs


async def autosave(bot, logger, activitylog, db_conn):
    await save(logger, activitylog, db_conn)
    await asyncio.sleep(60)  # saves every 60 seconds


async def save(logger, activitylog, db_conn, debug=True):

    create_sql = [f""" CREATE TABLE IF NOT EXISTS activitylog (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            lastseen text,
                            firstseen text,
                            messagecount integer ); 
                            DELETE FROM activitylog; """]

    for user in activitylog:
        create_sql.append(f""" INSERT INTO activitylog (name, lastseen, firstseen, messagecount)
                                VALUES ({user}, {activitylog[user]['lastseen']},
                                {activitylog[user]['firstseen']}, {activitylog[user]['messagecount']})""")

    try:
        for command in create_sql:
            await db_conn.execute(command)

        if debug:  # show our work in the console
            check = await db_conn.execute(f"SELECT * FROM activitylog")
            rows = await check.fetchall()
            for row in rows:
                logger.debug(f"ID: {row[0]} - Name: {row[1]} - Lastseen: {row[2]} "
                             f"- Firstseen: {row[3]} - Messagecount: {row[4]}")

    except aiosqlite.Error as e:
        print(e)
