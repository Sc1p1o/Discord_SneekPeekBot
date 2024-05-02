import discord
import logging.handlers
import os

from discord.ext import tasks, commands
from typing import List, Tuple

from dotenv import load_dotenv

from cogs import cogs_example, sneek_commands


class SneekBot(commands.Bot):
    BOT_TOKEN: str
    logger: logging.Logger
    sneek_channel: List[Tuple[int, int]] = []
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    def __init__(self, command_prefix: str, sneek_logger: logging.Logger, **options):
        # create bot instance and setup intents

        super().__init__(command_prefix, **options)
        self.logger = sneek_logger
        self.update_channels = {}

        load_dotenv()
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)

        # ladet die Cogs/Erweiterungen
        self.logger.info("loading cogs...")
        #await self.add_cog(cogs_example.ExampleCog(self))
        await self.add_cog(sneek_commands.SneekCog(self))
        self.logger.info("... finished")
