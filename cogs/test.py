from discord.ext import commands
import discord

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send(" - ".join(args))
    
    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send('{0} joined on {0.joined_at}'.format(member))

def setup(bot):
    bot.add_cog(Test(bot))