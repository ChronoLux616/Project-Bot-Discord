from discord.colour import Color
import discord
import time
from discord.ext import commands

class Com1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Show avatar user")
    async def avatar(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        avatar = discord.Embed(color= discord.Color.dark_blue())
        avatar.add_field(name=user.name, value=f"[display avatar in browser]({user.avatar})")
        avatar.set_image(url=user.avatar)
        avatar.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar)
        await ctx.send(embed=avatar)
        
    @commands.command(brief="Create an invite link to the channel")
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)
        
    @commands.command(pass_context=True)
    async def ping(self, ctx):
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
    
async def setup(bot):
    await bot.add_cog(Com1(bot))