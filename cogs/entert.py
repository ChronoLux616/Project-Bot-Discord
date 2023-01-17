import discord
from discord import colour
from discord import user
from discord.ext import commands
from discord.ext.commands.core import command
import giphy_client
from giphy_client.rest import ApiException
import requests
import json
import random
import os


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gifs(self, ctx, *, q="."):
        """ Busca gifs desde Giphy """
        giphy_api = os.getenv("GIPHY_API")
        api_instance = giphy_client.DefaultApi()
        try:
            api_responce = api_instance.gifs_search_get(giphy_api, q, limit=4, rating='g')
            lst = list(api_responce.data)
            giff = random.choice(lst)

            emb = discord.Embed(title=q)
            emb.add_field(name='Gif from Giphy', value=f'☑️', inline=False)
            emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.send(embed=emb)
        
        except ApiException as e:
            print("Error with API")
        
        except IndexError as o:
            await ctx.send('No se puede elegir de una secuencia vacía')
        
    @commands.command()
    async def gif(self, ctx, *, search, user: discord.Member=None):
        """ Busca gifs desde Tenor """
        if user is None:
            user = ctx.message.author
        
        search.replace('','+')
        tenor_api = os.getenv("TENOR_API")
        ckey = "New Project"
        lmt = 9
        r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search, tenor_api, ckey,  lmt))
        data = json.loads(r.content)
        gif_choice = random.randint(0, 9)
        result_gif = data["results"][gif_choice]["media_formats"]["gif"]["url"]
        # Crear embed con gif
        gifs = discord.Embed(colour=0x0760B8)
        gifs.add_field(name='Gif from Tenor', value=f'☑️', inline=False)
        gifs.add_field(name=search, value=f"🧿")
        gifs.set_image(url=result_gif)
        gifs.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar)
        await ctx.send(embed=gifs)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Necesitas un argumento mas!")
            

async def setup(bot):
    await bot.add_cog(Fun(bot))