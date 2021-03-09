from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='+')
client = discord.Client()

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='simple math plus')
    async def add(self, ctx, *sum):
        suma = " + ".join(sum)
        adds = discord.Embed()
        await ctx.send(f'{suma} = {eval(suma)}')
        # await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

# ===================================================================================

    @commands.command()
    async def calc(self, ctx, operation, *nums):
        if operation not in ['+', '-', '*', '/']:
            await ctx.send('Please type a valid operation type.')
        var = f' {operation} '.join(nums)
        await ctx.send(f'{var} = {eval(var)}')

def setup(bot):
    bot.add_cog(Math(bot))
