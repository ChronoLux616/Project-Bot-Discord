import discord
import time
from discord.ext import commands
from discord.member import Member


bot = commands.Bot(command_prefix="+")

class Ping(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.command(pass_context=True, brief="Show ur ping")
    async def ping(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.message.author
        before = time.monotonic()
        message = await ctx.reply("Here!!")
        ping = (time.monotonic() - before) * 1000

        fping = discord.Embed(title="➖➖➖➖➖➖➖➖➖", colour=discord.Colour(0x3e038c))
        fping.add_field(name='✅', value=f'☑️', inline=True)
        fping.add_field(name="📶 Your ping is", value=f"`{int(ping)}ms`", inline=True)
        fping.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=fping)
        #print(f'Ping {int(ping)}ms')

    @commands.command(pass_context=True)
    async def ms_ping(self, ctx):
        before_1 = time.monotonic()
        message = await ctx.send("☑️ Espera...")
        ping_1 = (time.monotonic() - before_1) * 1000
        before_2 = time.monotonic()
        message = await ctx.send("☑️ Espera...")
        ping_2 = (time.monotonic() - before_2) * 1000

        e = discord.Embed(title="Author of the message:", colour=discord.Colour(0x3e038c))
        e.add_field(name='✅', value=f'☑️', inline=True)
        e.add_field(name='📶 Your ping 1 is', value=f"`{int(ping_1)}ms`")
        e.add_field(name='📶 Your ping 2 is', value=f"`{int(ping_2)}ms`")
        e.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
    
def setup(bot):
    bot.add_cog(Ping(bot))
