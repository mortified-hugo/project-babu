import discord
from discord.ext import commands
from checks import *
from functions import *


class GameCommands(commands.Cog):
    """Defines commands for playing the game itself"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_mod()
    async def add_hate(self, ctx, player: discord.Member, hate_change: int):
        """Allow mods to alter the hate value of a player"""
        player_name = str(player.display_name)
        alter_variable('hate', player_name, ctx.guild, hate_change)
        await ctx.send(f'{player_name} had their hate changed by {hate_change}')
