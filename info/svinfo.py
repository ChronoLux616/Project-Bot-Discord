from discord.ext import commands
import discord

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def svinfo(self, ctx):
        """Shows server info"""

        server = ctx.message.guild

        roles = str(len(server.roles))
        emojis = str(len(server.emojis))
        channels = str(len(server.channels))

        embeded = discord.Embed(title=server.name, description='Server Info', color=0xEE8700)
        embeded.set_thumbnail(url=server.icon_url)
        embeded.add_field(name="Created on:", value=server.created_at.strftime('%d %B %Y at %H:%M UTC+3'), inline=False)
        embeded.add_field(name="Server ID:", value=server.id, inline=False)
        embeded.add_field(name="Users on server:", value=server.member_count, inline=True)
        embeded.add_field(name="Server owner:", value=server.owner, inline=True)

        # embeded.add_field(name="Default Channel:", value=server.default_channel, inline=True)
        embeded.add_field(name="Server Region:", value=server.region, inline=True)
        embeded.add_field(name="Verification Level:", value=server.verification_level, inline=True)

        embeded.add_field(name="Role Count:", value=roles, inline=True)
        embeded.add_field(name="Emoji Count:", value=emojis, inline=True)
        embeded.add_field(name="Channel Count:", value=channels, inline=True)

        await ctx.send(embed=embeded)

    @commands.command()
    async def profile(self, ctx, *, user:discord.Member = None):
        if user is None:
            user = ctx.author

        embed = discord.Embed(colour=discord.Colour(0x36393F), title=f"{user.name}'s Stats and Information.")
        embed.set_footer(text=f"ID: {user.id}")
        embed.set_thumbnail(url=user.avatar_url_as(format="png"))
        embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
                                                                   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}\n")
                                                                #    f"**Status:** {discord.Status(user)}\n"
                                                                #    f"**Activity:** {discord.Activity(user)}", inline=False)
        embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                          f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                          f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
        return await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=0xEE8700)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        embed.set_thumbnail(url = str(ctx.guild.icon_url))
        embed.add_field(name = f"Information About **{ctx.guild.name}**: ", value = f":white_small_square: ID: **{ctx.guild.id}** \n"
                                                                                    f":white_small_square: Owner: **{ctx.guild.owner}** \n"
                                                                                    f":white_small_square: Location: **{ctx.guild.region}** \n"
                                                                                    f":white_small_square: Creation: **{ctx.guild.created_at.strftime('%d %B %Y at %H:%M UTC+3')}** \n"
                                                                                    f":white_small_square: Members: **{ctx.guild.member_count}** \n:"
                                                                                    f"white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n"
                                                                                    f":white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n"
                                                                                    f":white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))