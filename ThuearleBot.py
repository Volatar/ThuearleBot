import os
import discord
import random
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
import logging
from MyBot import MyBot

import tbregex
from dbconn import dbconnect


def main():
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
    TOKEN = os.getenv('DISCORD_TOKEN')  # retrives the bot token from the .env file
    intents = discord.Intents.default()
    intents.members = True  # lets us read the memberlist
    bot = MyBot(command_prefix='!', intents=intents)

    # import command responses from database
    logger.info("Loading commands into memory:")
    try:
        logger.info("Connecting to database")
        db_conn = dbconnect('database/commandsDB.db', logger)
        cursor = db_conn.cursor()

        tableflip_responses = []
        data = cursor.execute(f'SELECT response FROM tableflip')
        for row in data:
            tableflip_responses.append(row[0])
        logger.debug("loaded tableflip")

        heresy_responses = []
        data = cursor.execute(f'SELECT response FROM heresy')
        for row in data:
            heresy_responses.append(row[0])
        logger.debug("loaded heresy")

        gitgud_responses = []
        data = cursor.execute(f'SELECT response FROM gitgud')
        for row in data:
            gitgud_responses.append(row[0])
        logger.debug("loaded gitgud")

        db_conn.close()
    except sqlite3.Error as e:
        logger.error(e)

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

        if not activitylog[message.author]:
            activitylog.update({message.author:
                                {"lastseen": datetime.utcnow(), "firstseen": datetime.utcnow(), "messagecount": 1}})
        elif activitylog[message.author]:
            authorinfo = activitylog.get(message.author)
            authorinfo.update({"lastseen": datetime.utcnow(), "messagecount": authorinfo.get("messagecount") + 1})
            activitylog.update({message.author: {authorinfo}})

        # needed for the bot to process regular commands after parsing the message for custom text
        await bot.process_commands(message)

    @bot.event
    async def on_error(event, error, *args, **kwargs):
        if event == 'on_message':
            logger.warning(f'Unhandled message: {args[0]}')
            logger.warning(f'Message error: {error}\n')
        else:
            raise

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
