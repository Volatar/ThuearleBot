import os
import discord
from dotenv import load_dotenv


def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')


    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

        print(f'{client.user} is connected to the following guilds:')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')

    client.run(TOKEN)


if __name__ == '__main__':
    main()
