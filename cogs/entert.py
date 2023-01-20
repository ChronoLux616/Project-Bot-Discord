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
            
    @commands.command()
    async def anime(self, ctx, *, query="naruto"): # 'anime' is the name of the command
        # This command can be used as `?anime character_name_here`
        # The default value will be 'naruto' for the query
        try:
            reqcont = requests.get(f"https://www.animecharactersdatabase.com/api_series_characters.php?character_q={query}")
            if reqcont.content==-1 or reqcont.content=='-1': # i found out that the website returns: -1 if there are no results, so here, we implement it
                await ctx.send("[-] Unable to find results! - No such results exists!")

            else:
                # If the website doesnt return: -1 , this will happen
                try:
                    reqcont = reqcont.json()
                except Exception as e:

                    # Please enable this line only while you are developing and not when deplying
                    await ctx.send(reqcont.content)

                    await ctx.send(f"[-] Unable to turn the data to json format! {e}")
                    return # the function will end if an error happens in creating a json out of the request

                # selecting a random item for the output
                rand_val = len(reqcont["search_results"])-1
                get_index = random.randint(0, rand_val)
                curent_info = reqcont["search_results"][get_index]

                # Creting the embed and sending it
                embed=discord.Embed(title="Anime Info", description=":smiley: Anime Character Info result for {query}", color=0x00f549)
                embed.set_author(name="YourBot", icon_url="https://cdn.discordapp.com/attachments/877796755234783273/879295069834850324/Avatar.png")
                embed.set_thumbnail(url=f"{curent_info['anime_image']}")
                embed.set_image(url=f"{curent_info['character_image']}")
                embed.add_field(name="Anime Name", value=f"{curent_info['anime_name']}", inline=False)
                embed.add_field(name="Name", value=f"{curent_info['name']}", inline=False)
                embed.add_field(name="Gender", value=f"{curent_info['gender']}", inline=False)
                embed.add_field(name="Description", value=f"{curent_info['desc']}", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.mention}")
                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"[-] An error has occured: {e}")
            

async def setup(bot):
    await bot.add_cog(Fun(bot))