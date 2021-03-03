import os
from discord.ext import commands
from settings import *

bot = commands.Bot(command_prefix="+")

# agrega los arhivos de carpeta cogs necesarios
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

# agrega los arhivos de carpeta tools necesarios
for filename in os.listdir("./tools"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'tools.{filename[:-3]}')

bot.run(DISCORD_BOT_TOKEN)
