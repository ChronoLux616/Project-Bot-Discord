from discord.colour import Color
from discord.ext import commands
from utils import text_to_owo
import discord

bot = commands.Bot(command_prefix="+")

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, x):
        print(x)
        await ctx.send("Please check +help")

    @commands.command(brief="Show avatar user")
    async def avatar(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        avatar = discord.Embed(color= discord.Color.dark_blue())
        avatar.add_field(name=user.name, value=f"[display avatar in browser]({user.avatar_url})")
        avatar.set_image(url=user.avatar_url)
        avatar.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=avatar)

    @commands.command(brief="Any message to owo")
    async def owo(self, ctx):
        await ctx.send(text_to_owo(ctx.message.content))

    @commands.command(brief="Create an invite link to the channel")
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

def setup(bot):
    bot.add_cog(Basic(bot))