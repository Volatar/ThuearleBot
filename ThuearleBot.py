import os
import disnake
import random
from datetime import datetime
from dotenv import load_dotenv
import aiosqlite
import logging
from MyBot import MyBot
import asyncio

import tbregex
from dbconn import dbconnect


async def main():
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

    logger.info("Starting bot")
    load_dotenv()  # loads the .env file
    TOKEN = os.getenv('DISCORD_TOKEN')  # retrieves the bot token from the .env file
    intents = disnake.Intents.all()
    bot = MyBot(command_prefix='!', intents=intents)

    # import command responses from database
    logger.info("Loading commands into memory:")
    try:
        logger.info("Connecting to database")
        db_conn = await dbconnect('database/commandsDB.db', logger)

        tableflip_responses = []
        data = await db_conn.execute(f'SELECT response FROM tableflip')
        for row in await data.fetchall():
            tableflip_responses.append(row[0])
        logger.debug("loaded tableflip")

        heresy_responses = []
        data = await db_conn.execute(f'SELECT response FROM heresy')
        for row in await data.fetchall():
            heresy_responses.append(row[0])
        logger.debug("loaded heresy")

        gitgud_responses = []
        data = await db_conn.execute(f'SELECT response FROM gitgud')
        for row in await data.fetchall():
            gitgud_responses.append(row[0])
        logger.debug("loaded gitgud")

        await db_conn.commit()
    except aiosqlite.Error as e:
        logger.error(e)

    # TODO: load from database at program start
    activitylog = {}

    @bot.event
    async def on_ready():
        # just some feedback that it's working
        logger.info(f"{bot.user.name} has connected to Discord!")
        logger.debug(f'{bot.user.name} is connected to the following guilds:')
        for guild in bot.guilds:
            logger.debug(f'{guild.name} (id: {guild.id})')
            members = '\n - '.join([member.name for member in guild.members])
            logger.debug(f'Guild Members:\n - {members}')

    # !heresy (the WH40k kind)
    @bot.command(name='heresy', help='Responds with a heresy detected gif')
    async def heresy(ctx):
        response = random.choice(heresy_responses)
        await ctx.send(response)

    # !gitgud (the dark souls kind)
    @bot.command(name='gitgud', help='Responds with a \"Git Gud\" or Dark Souls gif')
    async def gitgud(ctx):
        response = random.choice(gitgud_responses)
        await ctx.send(response)

    # !userinfo
    @bot.command(name='userinfo',
                 help='displays user message count, when first seen, and when last seen. Case sensitive.')
    async def userinfo(ctx, arg):
        response = f"{arg} was first seen on {disnake.utils.format_dt(activitylog.get(arg).get('firstseen'))}, " \
                   f"they were last seen on {disnake.utils.format_dt(activitylog.get(arg).get('lastseen'))}, " \
                   f"and they have sent {activitylog.get(arg).get('messagecount')} messages in servers I monitor."
        await ctx.send(response)

    # !al (activity log debug command)
    @bot.command(name='al', help='dumps activity log dictionary to debug logger')
    async def al(ctx):
        logger.debug(activitylog)
        await ctx.send("activity log dumped to console")

    @bot.event
    async def on_message(message):
        # prevents bot from responding to itself
        if message.author == bot.user:
            return

        # responds when someone sends /tableflip
        if message.content == '(╯°□°）╯︵ ┻━┻':
            response = random.choice(tableflip_responses)
            await message.channel.send(response)

        # responds to remfive and ramfive with the opposite, since they are a pair emote
        # TODO: Make it wait and see if someone else responds first before responding. Gotta learn timers.
        if tbregex.remfive.match(message.content):
            await message.channel.send('<:ramfive:469906460134866956>')
        if tbregex.ramfive.match(message.content):
            await message.channel.send('<:remfive:469906494163255316>')

        # TODO: Adjust so that it uses full usernames rather than just changeable nicknames
        # TODO: save to database
        if not activitylog.get(message.author.name):
            activitylog.update({message.author.name:
                                {"lastseen": datetime.utcnow(), "firstseen": datetime.utcnow(), "messagecount": 1}})
        elif activitylog.get(message.author.name):
            authorinfo = activitylog.get(message.author.name)
            authorinfo.update({"lastseen": datetime.utcnow(), "messagecount": authorinfo.get("messagecount") + 1})
            activitylog.update({message.author.name: authorinfo})

        # needed for the bot to process regular commands after parsing the message for custom text
        await bot.process_commands(message)

    @bot.event
    async def on_error(event, error, *args, **kwargs):
        if event == 'on_message':
            logger.warning(type(error))
            logger.warning(f'Unhandled message: {args[0]}')
            logger.warning(f'Message error: {error}')
            logger.warning(f'args: {args}')
            logger.warning(f'kwargs: {kwargs}\n')

        else:
            raise

    bot.run(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
