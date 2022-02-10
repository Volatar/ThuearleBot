import os
import discord
import random
import datetime
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
            'https://tenor.com/view/warhammer-gif-19055033',
            'https://tenor.com/view/heavy-flamer-heresy-purge-warhammer40k-lightning-claws-gif-16488791',
            'https://tenor.com/view/warhammer-heresy-newspaper-gif-8197244',
            'https://tenor.com/view/fulgore-devastation-killer-instinct-killer-instinct-gif-17301589',
            'https://tenor.com/view/warhammer-40k-heresy-blasphemy-gif-18901767',
            'https://tenor.com/view/penny-polendina-rwby-heresy-heretic-rooster-teeth-gif-15607459',
        ]

        if message.content == '!wh40k':
            response = random.choice(wh40k_responses)
            await message.channel.send(response)

        tableflip_responses = [
            '┬─┬ ノ( ゜-゜ノ) Here you go, flip it again.',
            '┬─┬ ノ( ゜-゜ノ) Why are you so angry onii-chan?',
            'https://tenor.com/view/so-pissed-im-work-mad-gif-23416426',
            'https://tenor.com/view/fat-gordo-gif-22200250',
            'https://tenor.com/view/table-flip-furious-pissed-mad-angry-gif-4502191',
            'https://tenor.com/view/table-flip-mad-angry-furious-rage-gif-3962583',
            'https://tenor.com/view/teresa-giudice-rhonj-real-housewives-gif-9728056',
            'https://tenor.com/view/anger-gif-20959048',
            'https://tenor.com/view/anger-flipping-table-table-flipping-flip-table-table-flip-gif-15852149',
            'https://tenor.com/view/catan-tableflip-i-quit-you-cheater-angry-gif-4955758',
            'https://tenor.com/view/snape-table-flip-flipping-tables-flip-table-anger-gif-15852143',
            'https://tenor.com/view/table-flip-tableflip-flip-table-anime-flip-gif-5738472',
            'https://tenor.com/view/tuvedlacom-swann-table-flip-disappointed-rage-gif-17686266',
            'https://tenor.com/view/30rock-liz-lemon-tina-fey-table-flip-mad-gif-4427407',
        ]

        if message.content == '(╯°□°）╯︵ ┻━┻':
            response = random.choice(tableflip_responses)
            await message.channel.send(response)

    @client.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'{datetime.datetime.utcnow()}: Unhandled message: {args[0]}\n')
            else:
                raise

    client.run(TOKEN)


if __name__ == '__main__':
    main()
