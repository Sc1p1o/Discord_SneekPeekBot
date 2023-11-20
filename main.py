import requests
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup

load_dotenv()

bot_token = os.getenv('DISCORD_TOKEN')

if bot_token is None:
    print("Der Discord Token wurde nicht gefunden. Stelle sicher, dass die Umgebungsvariable gesetzt ist.")
else:
    intents = discord.Intents.all()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)


    @bot.event
    async def on_ready():
        print(f'Bot is online and connected to Discord as {bot.user.name}')


    @bot.command()
    async def sneek(ctx):
        sneek_preview = "Hallo"
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
                        sneek_preview = movie
                    counter = counter + 1
        else:
            print(f'Fehler beim Abrufen der Seite. Statuscode: {response.status_code}')

        await ctx.send(sneek_preview)


    bot.run(bot_token)