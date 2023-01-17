import discord
from discord.ext import commands
import settings
import random
import os
import json
import requests


logger = settings.logging.getLogger(__name__)
intents = discord.Intents().all()
intents.members=True
client = discord.Client(intents=intents)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def server(self, ctx):
        """ Shows basic information about Guild """
        
        embed = discord.Embed(title=f"{ctx.guild.name} - Server Info ", description="Server information")
        embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
        embed.add_field(name="GUID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Created at", value=discord.utils.format_dt(ctx.guild.created_at), inline=False)
        embed.add_field(name="Server Description", value=ctx.guild.description, inline=False)
        embed.add_field(name="Owner Name", value=ctx.guild.owner, inline=False)
        embed.add_field(name="Owner Account Created", value=discord.utils.format_dt(ctx.guild.owner.created_at), inline=False)    
        embed.add_field(name="Server Users", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="Voice", value=len(ctx.guild.voice_channels), inline=True)
        embed.add_field(name="Stage", value=len(ctx.guild.stage_channels), inline=True)
        embed.add_field(name="Text", value=len(ctx.guild.text_channels), inline=True)
        embed.add_field(name="Categories", value=len(ctx.guild.categories), inline=True)
        embed.add_field(name="Forums", value=len(ctx.guild.forums), inline=True)
        embed.add_field(name="File Size Limit", value=f"%.2f Mb" % float(ctx.guild.filesize_limit / 1024 / 1024), inline=False)
        embed.add_field(name="Bitrate Limit", value=f"%.2f kbit" %  float(ctx.guild.bitrate_limit / 1000), inline=False)  
        embed.add_field(name="Tier", value=ctx.guild.premium_tier, inline=True)
        embed.add_field(name="Sub Count", value=ctx.guild.premium_subscription_count, inline=True)
        
        if len(ctx.guild.features):
            features = ":".join(ctx.guild.features)
            embed.add_field(name="Features", value=features, inline=False)
        
        embed.add_field(name="MFA", value="Disabled" if ctx.guild.mfa_level == discord.MFALevel.disabled else "Enabled", inline=False)
        embed.add_field(name="Is large?", value="Yes" if ctx.guild.large else "No", inline=False)
        embed.add_field(name="AFK Channel", value=ctx.guild.afk_channel, inline=False)
        embed.add_field(name="Rules Channel", value=ctx.guild.rules_channel, inline=False)
        embed.add_field(name="System Channel", value=ctx.guild.system_channel, inline=False)
        embed.add_field(name="Default Role", value=ctx.guild.default_role.name, inline=True)
        
        if ctx.guild.premium_subscriber_role:
            embed.add_field(name="Premium Subscriber Role", value=ctx.guild.premium_subscriber_role.name, inline=True)
            
        embed.add_field(name="# Roles", value=len(ctx.guild.roles), inline=True)
            
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner:        
            embed.set_image(url=ctx.guild.banner.url)
        embed.set_footer(text="Created by GenericUser201")
        await ctx.send(embed=embed)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Only owner can use this command")
    
    
    @commands.command()
    async def purge(self, ctx, channel : discord.TextChannel = None, limit : int = 100):
        """ Delete N number of messages in a channel """
        if channel is None:
            channel = ctx.message.channel
        await channel.purge(limit=limit)
    
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'Hey there! do +prefixsetup to make your moderation role')
            break
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member, search="anime welcome"):
        # gif de tenor
        tenor_api = os.getenv("TENOR_API")
        ckey = "New Project"
        lmt = 9
        r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search, tenor_api, ckey,  lmt))
        data = json.loads(r.content)
        gif_choice = random.randint(0, 9)
        result_gif = data["results"][gif_choice]["media_formats"]["gif"]["url"]
        
        channel = member.guild.get_channel(1060369749277679656)
        if channel is not None:
            role = discord.utils.get(member.guild.roles, id=1061420615858393159)
            embed=discord.Embed(title=f"Bienvenido (a) {member.name}", description=f"Gracias por ingresar a {member.guild.name}!") # F-Strings!
            embed.add_field(name=f"Eres el miembro N° ", value=f"{member.guild.member_count}", inline=True)
            embed.set_image(url=result_gif)
            embed.set_thumbnail(url=member.avatar) # Set the embed's thumbnail to the member's avatar image!
            await channel.send(embed=embed)
            await member.add_roles(role)
    
    
    @commands.Cog.listener()
    async def on_member_remove(self, member, search="anime bye"):
        # gif de tenor
        tenor_api = os.getenv("TENOR_API")
        ckey = "New Project"
        lmt = 9
        r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search, tenor_api, ckey,  lmt))
        data = json.loads(r.content)
        gif_choice = random.randint(0, 9)
        result_gif = data["results"][gif_choice]["media_formats"]["gif"]["url"]
        # parte del embed de despedida
        channel = member.guild.get_channel(1064611090941628536)
        if channel is not None:
            embed=discord.Embed(title=f"Adios {member.name}", description=f"Regresa si gustas de nuevo") # F-Strings!
            embed.set_image(url=result_gif)
            embed.set_thumbnail(url=member.avatar) # Set the embed's thumbnail to the member's avatar image!
            await channel.send(embed=embed)
                   
async def setup(bot):
    await bot.add_cog(Admin(bot))