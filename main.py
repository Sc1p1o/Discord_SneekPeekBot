import discord
import logging.handlers

from sneekbot import SneekBot

# create logger and set up logging handler to log data in different files depending on log level
logging.basicConfig(level=logging.DEBUG)  # Setze die unterste Stufe für das Logging

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

debug_handler = logging.FileHandler('logs/debug.log')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

warning_handler = logging.FileHandler('logs/warning.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)

error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

critical_handler = logging.FileHandler('logs/critical.log')
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(critical_handler)

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = SneekBot(command_prefix="!",intents=intents, sneek_logger=logger)

# startet den Bot
bot.run(bot.BOT_TOKEN)
