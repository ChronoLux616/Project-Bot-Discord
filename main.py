import discord
import settings
from discord.ext import commands
import others.utils as utils

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents().all()
    intents.message_content = True
    intents.members = True
    intents.reactions = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix="+", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id}")
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.change_presence(status=discord.Status.online , activity=discord.Activity(type = discord.ActivityType.watching, name = 'for +help'))
        await bot.tree.sync(guild=settings.GUILDS_ID)
        await utils.load_videocmds(bot)
        
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                
    @bot.command()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)
    
if __name__ == "__main__":
    run()