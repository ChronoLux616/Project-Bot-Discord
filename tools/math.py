from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='+')
client = discord.Client()

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # separate operations
    @commands.command(brief='🔴 simple math +')
    async def add(self, ctx, *sum, user:discord.Member = None):
        if user is None:
            user = ctx.message.author
        suma = " + ".join(sum)
        adds = discord.Embed(color= discord.Color.dark_blue())
        adds.add_field(name="✅ Result : ", value=f'{suma} = {eval(suma)}', inline=True)
        adds.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=adds)
    
    @commands.command(brief='🔴 simple math -')
    async def less(self, ctx, *minus, user:discord.Member = None):
        if user is None:
            user = ctx.message.author
        menos = " - ".join(minus)
        adds = discord.Embed(color= discord.Color.dark_blue())
        adds.add_field(name="✅ Result : ", value=f'{menos} = {eval(menos)}', inline=True)
        adds.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=adds)
        # await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

# ===================================================================================

    # all operations in one command
    @commands.command(brief='🔴 all operations; [+ - * / ] + numbers')
    async def calc(self, ctx, operation, *nums, user:discord.Member = None):
        if user is None:
            user = ctx.message.author
        if operation not in ['+', '-', '*', '/']:
            await ctx.send('❎ Please type a valid operation type.')
        var = f' {operation} '.join(nums)
        op = discord.Embed(color= discord.Color.dark_blue())
        op.add_field(name="✅ Result : ", value=f'{var} = {eval(var)}', inline=True)
        op.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=op)

def setup(bot):
    bot.add_cog(Math(bot))
