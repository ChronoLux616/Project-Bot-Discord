import os
from discord.ext import commands
from settings import *

bot = commands.Bot(command_prefix="+")

bot.run('TOKEN')
