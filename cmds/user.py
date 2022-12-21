from discord.colour import Color
import discord
import time
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Show avatar user")
    async def avatar(ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        avatar = discord.Embed(color=discord.Color.dark_blue())
        avatar.add_field(name=user.name)
        avatar.set_image(url=user.avatar)
        avatar.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar)
        await ctx.send(embed=avatar)
        
    @commands.command(brief="Create an invite link to the channel")
    @commands.guild_only()
    async def invite(ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)
        
    @commands.command(pass_context=True, brief="Show ur ping")
    async def ping(ctx, user: discord.Member=None):
        if user is None:
            user = ctx.message.author
        before = time.monotonic()
        message = await ctx.reply("Here!!")
        ping = (time.monotonic() - before) * 1000

        fping = discord.Embed(title="➖➖➖➖➖➖➖➖➖", colour=discord.Colour(0x3e038c))
        fping.add_field(name='✅', value=f'☑️', inline=True)
        fping.add_field(name="📶 Your ping is", value=f"`{int(ping)}ms`", inline=True)
        fping.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar)
        await ctx.send(embed=fping)
    
async def setup(bot):
    await bot.add_cog(User(bot))