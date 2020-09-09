import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

from guild_setup.guild_init import GuildInitiation
from game_commands.game_commands import GameCommands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    """Read Guilds"""

    print(f'{bot.user.name} has connected to Discord!')
    print(f'This bot is currently on {len(bot.guilds)} guilds')


@bot.event
async def on_guild_join(guild: discord.Guild):
    with open('hail.txt') as file:
        response = file.read()
    await guild.channels[0].send(response)


@bot.command(name='get_id')
async def get_id(ctx):
    await ctx.send(ctx.guild.id)

bot.add_cog(GuildInitiation(bot))
bot.add_cog(GameCommands(bot))
bot.run(TOKEN)
