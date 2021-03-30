from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="+")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helps(self, ctx):
        await ctx.send("Help")

def setup(bot):
    bot.add_cog(Help(bot))