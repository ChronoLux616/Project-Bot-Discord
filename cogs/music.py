import discord
from discord.ext import commands
import settings
import wavelink
import asyncio

logger = settings.logging.getLogger("bot")

class Music(commands.Cog):
    vc : wavelink.Player = None
    current_track = None
    music_channel = None
    history = None
    songs = asyncio.Queue()
    
    def __init__(self, bot):
        self.bot = bot
        self.history = list()
    
    async def setup(self):
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host="localhost",
            port=2333,
            password="root"
        )
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        logger.info(f"{node} is ready")
        
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        emb = discord.Embed(colour=discord.Color.yellow())
        emb.add_field(name='Starting playing: ', value=f'{track.title}', inline=True)
        await self.music_channel.send(embed=emb)
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name='Finished: ', value=f'{track.title}', inline=True)
        await self.music_channel.send(embed=emb)
        self.history.append(track.title)
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        self.music_channel = ctx.message.channel
        if channel:
            self.vc = await channel.connect(cls=wavelink.Player)
            await ctx.send(f"Joined {channel.name}")
        
    @commands.command()
    async def add(self, ctx, *title: str):
        choosen_track = await wavelink.YouTubeMusicTrack.search(query="".join(title), return_first=True)
        if choosen_track:
            self.current_track = choosen_track
            self.vc.queue.put(choosen_track)
    
    @commands.command()
    async def play(self, ctx):
        if self.current_track and self.vc:
            await self.vc.play(self.current_track)
    
    @commands.command()
    async def skip(self, ctx):
        if self.vc.queue.is_empty:
            await ctx.send("There are no more tracks!")
        self.current_track = self.vc.queue.get()
        await self.vc.play(self.current_track)
    
    @commands.command()
    async def pause(self, ctx):
        await self.vc.pause()
        
    @commands.command()
    async def resume(self, ctx):
        await self.vc.resume()
        
    @commands.command()
    async def stop(self, ctx):
        await self.vc.stop()
        
    @commands.command()
    async def queue(self, ctx):
        queue_item = (self.add.choosen_track[0], ctx.guild.id)
        await self.songs.put(queue_item)
        
    @commands.command()
    async def history(self, ctx):
        self.history.reverse()
        embed = discord.Embed(title="Song History")
        for track_item in self.history:
            track_info = track_item.split(" - ")
            embed.add_field(name=track_info[1], value=track_info[0])
        await ctx.send(embed=embed)
        
    @commands.command()
    async def plays(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.join)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(tracks[0])

async def setup(bot):
    music_bot = Music(bot)
    await bot.add_cog(music_bot)
    await music_bot.setup()