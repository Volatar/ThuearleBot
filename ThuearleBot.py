import os
import discord
import random
import datetime
import codecs
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
from dbconn import dbconnect

import tbregex


def main():
    print(f"{datetime.datetime.utcnow()}: Starting bot")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    print(f"{datetime.datetime.utcnow()}: Loading commands into memory:")
    try:
        print(f"{datetime.datetime.utcnow()}: Connecting to database")
        db_conn = dbconnect('database/commandsDB.db')

        cursor = db_conn.cursor()

        tableflip_responses = []
        data = cursor.execute(f'SELECT response FROM tableflip')
        for row in data:
            tableflip_responses.append(row[0])
        print(f"{datetime.datetime.utcnow()}: loaded tableflip")

        heresy_responses = []
        data = cursor.execute(f'SELECT response FROM heresy')
        for row in data:
            heresy_responses.append(row[0])
        print(f"{datetime.datetime.utcnow()}: loaded heresy")

        gitgud_responses = []
        data = cursor.execute(f'SELECT response FROM gitgud')
        for row in data:
            gitgud_responses.append(row[0])
        print(f"{datetime.datetime.utcnow()}: loaded gitgud")

    except sqlite3.Error as e:
        print(e)  # TODO: replace with proper error logging code

    @bot.event
    async def on_ready():
        print(f'{datetime.datetime.utcnow()}: {bot.user.name} has connected to Discord!')

        print(f'{bot.user.name} is connected to the following guilds:')
        for guild in bot.guilds:
            print(f'{guild.name} (id: {guild.id})')
            members = '\n - '.join([member.name for member in guild.members])
            print(f'Guild Members:\n - {members}')

    @bot.command(name='heresy', help='Responds with a heresy detected gif')
    async def heresy(ctx):
        response = random.choice(heresy_responses)
        await ctx.send(response)

    @bot.command(name='gitgud', help='Responds with a \"Git Gud\" or Dark Souls gif')
    async def gitgud(ctx):
        response = random.choice(gitgud_responses)
        await ctx.send(response)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content == '(╯°□°）╯︵ ┻━┻':
            response = random.choice(tableflip_responses)
            await message.channel.send(response)

        # TODO: Make it wait and see if someone else responds first before responding. Gotta learn timers.
        if tbregex.remfive.match(message.content):
            await message.channel.send('<:ramfive:469906460134866956>')

        if tbregex.ramfive.match(message.content):
            await message.channel.send('<:remfive:469906494163255316>')

        # needed for the bot to process regular commands after parsing the message for custom text
        await bot.process_commands(message)

    @bot.event
    async def on_error(event, *args, **kwargs):
        with open('errorLog.log', 'a') as errorLog:   # TODO: replace with proper error logging code
            if event == 'on_message':
                errorLog.write(f'{datetime.datetime.utcnow()}: Unhandled message: {args[0]}\n')
            else:
                raise

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
