import discord
import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands


bot_token = os.getenv('DISCORD_TOKEN')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
steve = os.getenv('STEVE_ID')

if bot_token is None:
    print("Token not found. Please Make sure the environmental variables are set correctly.")
else:
    intents = discord.Intents.all()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)


    @bot.event
    async def on_ready():
        print(f'Bot is online and connected to Discord as {bot.user.name}')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        easteregg = 'nob'
        regex_keyword = re.compile(rf'{"".join(f"({c}|{c.upper()})?" for c in keyword)}', re.IGNORECASE)
        if regex_keyword.search(message.content):
            print(f'keyword {easteregg} detected')
            if message.author.name.lower() == steve:
                print('responding to steve in chat')
                await message.channel.send('Selber Noob Steve!')    # jk bro
            else:
                print('but user is not steve, keyword ignored')

    @bot.command()
    async def sneek(ctx):
        sneek_preview = ""
        url = 'https://www.sneak-kino.de/sneak-prognose/'
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            article = soup.find_all('article')
            counter = 0

            for ul_object in article:
                list_objects = ul_object.find_all('ul')

                for movie_list in list_objects:
                    if 1 <= counter <= 3:
                        movie = movie_list.find_all('li')
                        movie_string = ''.join(map(str, movie))
                        sneek_preview = sneek_preview + movie_string + '&&\n'
                    counter = counter + 1
        else:
            print(f'Fehler beim Abrufen der Seite. Statuscode: {response.status_code}')

        sneek_preview = sneek_preview.replace('</li><li>', '\n')
        sneek_preview = sneek_preview.replace('<li>', '')
        sneek_preview = sneek_preview.replace('</li>', '')

        sub_sneek = sneek_preview.split('&&')

        webhook_movies = {
            'embeds': [
                {
                    'title': f'Aktuelle Sneek Peek Vorhersage',
                    'color': 16711680,
                    'footer': {
                        'text': f'Stand'
                    },
                    'fields': [
                        {
                            'name': "Hohe Wahrscheinlichkeit",
                            'value': f'{sub_sneek[0]}',
                            'inline': True
                        },
                        {
                            'name': 'Mittlere Wahrscheinlichkeit',
                            'value': f'{sub_sneek[1]}',
                            'inline': False
                        },
                        {
                            'name': 'Niedrige Wahrscheinlichkeit',
                            'value': f'{sub_sneek[2]}',
                            'inline': True
                        }
                    ],
                    'timestamp': f'{datetime.now().date()}'
                }
            ]
        }

        response = requests.post(webhook_url, json=webhook_movies)

        if response.status_code == 204:
            print('posted new sneek preview successfully via webhook client')
        else:
            print(f'An Error occurred while waiting for response of the webhook client:\n{response.status_code}')


    bot.run(bot_token)
