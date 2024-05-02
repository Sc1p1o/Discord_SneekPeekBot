from jkunze import extract

from discord import Embed
from discord.ext import commands


class SneekCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send('test')

    @commands.hybrid_command(name='sneek', description='Returns the Sneak Preview Table\n'
                                                       'sort = not implemented yet, movies are sorted by how likely'
                                                       ' they are to be played.')
    async def sneek(self, ctx, sort='chance'):
        movies = extract.scrape_sneak()

        sneek_table = Embed(title="Sneak Peak Preview",
                            description="Here's the prognosis of the Sneak Peak in Cinestar Leipzig.\n"
                                        "Highest possible value: 95,24%",
                            color=0x00ff00)

        for movie in movies:
            sneek_table.add_field(name=movie.get('Title'), value=f"Genre: {movie.get('Genre')}\n "
                                                                 f"Release: {movie.get('Year')}\n"
                                                                 f"Rating: {movie.get('IMDB')}\n"
                                                                 f"Chance: {movie.get('Chance')}%", inline=False)

        await ctx.send(embed=sneek_table)
