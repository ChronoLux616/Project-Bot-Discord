from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='+')


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def to_upper(argument):
        return argument.upper()

    @commands.command(brief='simple math plus')
    async def sum(self, ctx, a: int, b: int):
        await ctx.send(a + b)
        # await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

    @commands.command()
    async def up(self, ctx, *, content: to_upper):
        await ctx.send(content)


def setup(bot):
    bot.add_cog(Math(bot))
