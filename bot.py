import os
from discord.ext import commands
from dotenv import load_dotenv

from guild_init import GuildInitiation


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    """Read Guilds"""
    print(f'{bot.user.name} has connected to Discord!')
    print(f'This bot is currently on {len(bot.guilds)} guilds')

bot.add_cog(GuildInitiation(bot))
bot.run(TOKEN)
