import aiosqlite


async def dbconnect(db_file, logger):
    db_conn = None
    try:
        db_conn = await aiosqlite.connect(db_file)
        return db_conn
    except aiosqlite.Error as e:
        logger.error(e)

    return db_conn
