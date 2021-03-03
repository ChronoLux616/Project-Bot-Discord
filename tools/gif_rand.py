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


bot = commands.Bot(command_prefix="+")
tenor_api = 'api'
giphy_api = 'api'

class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="gifs from Giphy")
    async def gifs(self, ctx, *, q="anime"):
        api_key = 'api'
        api_instance = giphy_client.DefaultApi()
        try:
            api_responce = api_instance.gifs_search_get(api_key, q, limit=4, rating='pg')
            lst = list(api_responce.data)
            giff = random.choice(lst)

            emb = discord.Embed(title=q)
            emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            await ctx.send(embed=emb)
        
        except ApiException as e:
            print("Error with API")
        
    @commands.command(brief="gifs from Tenor")
    async def gif(self, ctx, *, search, user: discord.Member=None):
        if user is None:
            user = ctx.message.author
            
        search.replace('','+')
        apikey = "api"
        lmt = 4
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search, apikey, lmt))
        data = json.loads(r.text)
        gif_choice = random.randint(0, 3)
        result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

        gifs = discord.Embed(colour=0x0760B8)
        gifs.add_field(name=search, value=f"🧿")
        gifs.set_image(url=result_gif)
        gifs.set_footer(text=f'Request by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=gifs)

def setup(bot):
    bot.add_cog(Gifs(bot))