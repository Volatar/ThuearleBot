import os
import discord
import random
import datetime
from dotenv import load_dotenv
from discord.ext import commands


def main():
    print(f"{datetime.datetime.utcnow()}: Starting bot")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    print("Loading commands into memory:")
    with open('commands/tableflip.txt') as f:
        tableflip_responses = f.readlines()
        print('tableflip loaded')
    with open('commands/heresy.txt') as f:
        heresy_responses = f.readlines()
        print('heresy loaded')

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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content == '(╯°□°）╯︵ ┻━┻':
            response = random.choice(tableflip_responses)
            await message.channel.send(response)

        if message.content == '<:remfive:469906494163255316>':
            await message.channel.send('<:ramfive:469906460134866956>')

        if message.content == '<:ramfive:469906460134866956>':
            await message.channel.send('<:remfive:469906494163255316>')

        # needed for the bot to process regular commands after parsing the message for custom text
        await bot.process_commands(message)

    @bot.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as errorlog:
            if event == 'on_message':
                errorlog.write(f'{datetime.datetime.utcnow()}: Unhandled message: {args[0]}\n')
            else:
                raise

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
