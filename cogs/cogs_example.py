from discord.ext import commands


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def hello(self, ctx):
        await ctx.send('Hello world!')

    @commands.hybrid_command()
    async def add(self, ctx, left: int, right: int = 0):
        await ctx.send(left + right)
