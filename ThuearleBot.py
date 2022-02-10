import os
import discord
import random
from dotenv import load_dotenv


def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

        print(f'{client.user} is connected to the following guilds:')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')
            members = '\n - '.join([member.name for member in guild.members])
            print(f'Guild Members:\n - {members}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        wh40k_responses = [
            'https://tenor.com/view/heresy-detected-war-hammer-40k-gif-9829547',
            'https://tenor.com/view/40k-astartes-bolter-boltgun-dakka-gif-17604583',
        ]

        if message.content == '!wh40k':
            response = random.choice(wh40k_responses)
            await message.channel.send(response)

    client.run(TOKEN)


if __name__ == '__main__':
    main()
