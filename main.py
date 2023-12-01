import discord
import os
import requests
import asyncio

import functions as f

from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands

SNEEK_CHANNEL_ID = 1175914936082382913
bot_token = os.getenv('DISCORD_TOKEN')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
steve = os.getenv('STEVE_ID')

if bot_token is None:
    print("Token not found. Please Make sure the environmental variables are set correctly.")
else:
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


    @bot.event
    async def on_ready():
        print(f'Bot is online and connected to Discord as {bot.user.name}')


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if f.ist_noob(message.content):
            print('keyword detected ... ')
            if message.author.name.lower() == steve:
                print('... and user is Steve! Answering Steve...')
                await message.channel.send('Selber Noob Steve!')
            else:
                print('...but user is not Steve!')
        await bot.process_commands(message)


    @bot.command(name='suggest')
    async def suggest(ctx, *args):
        movie_title: str = ' '.join(args)

        embed = discord.Embed(title=f"Informationen zu {movie_title}", color=0x00ff00)

        movie_info = f.get_movie_info(movie_title)

        embed.add_field(name="IMDb Wertung", value=movie_info['imdb_rating'], inline=False)
        embed.add_field(name="Trailer", value=movie_info['trailer_url'], inline=False)

        await ctx.send(embed=embed)


    @bot.hybrid_command(name='peek')
    async def sneek(ctx: commands.Context):

        target_channel = bot.get_channel(SNEEK_CHANNEL_ID)
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
            print(f'An Error occurred while trying to connect to the website: {response.status_code}')

        sneek_preview = sneek_preview.replace('</li><li>', '\n')
        sneek_preview = sneek_preview.replace('<li>', '')
        sneek_preview = sneek_preview.replace('</li>', '')

        sub_sneek = sneek_preview.split('&&')

        embed = discord.Embed(title='Aktuelle Sneek Peek Vorhersage', color=0x00ff00)
        embed.add_field(name='Hohe Wahrscheinlichkeit', value=sub_sneek[0], inline=True)
        embed.add_field(name='Mittlere Wahrscheinlichkeit', value=sub_sneek[1], inline=False)
        embed.add_field(name='Niedrige Wahrscheinlichkeit', value=sub_sneek[2], inline=True)
        embed.set_footer(text='Stand: ')
        embed.timestamp = datetime.now()

        if target_channel:
            # Sende die Antwort nur im Zielkanal
            await target_channel.send(embed=embed)
        else:
            # Falls der Zielkanal nicht gefunden wurde
            print("Could not find Channel with saved Channel-ID")
            await ctx.send(embed=embed)




    bot.run(bot_token)
