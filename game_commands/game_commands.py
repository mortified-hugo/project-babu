import discord
from discord.ext import commands
import csv

from checks import *
from functions import *


class GameCommands(commands.Cog):
    """Defines commands for playing the game itself"""

    def __init__(self, bot):
        self.bot = bot

    #  Simple hate and fandom alterations

    @commands.command()
    @is_mod()
    async def add_hate(self, ctx, player: discord.Member, hate_change: int):
        """Allow mods to alter the hate value of a player"""
        player_name = str(player.display_name)
        try:
            alter_variable('hate', player_name, ctx.guild, hate_change)
            await ctx.send(f'{player_name} had their hate changed by {hate_change}')
        except KeyError:
            await ctx.send('No player of that name found')

    @commands.command()
    @is_mod()
    async def add_fandom(self, ctx, player: discord.Member, fandom_change: int):
        """Allow mods to alter the fandom value of a player"""
        player_name = str(player.nick)
        try:
            alter_variable('fandom', player_name, ctx.guild, fandom_change)
            await ctx.send(f'{player_name} had their fandom changed by {fandom_change}')
        except KeyError:
            await ctx.send('No player of that name found')

    #  List of Players

    @commands.command()
    async def list_players(self, ctx):
        response = ''
        with open(f'guilds/{ctx.guild.name}/hate-fandom.csv') as file:
            for row in csv.reader(file):
                if row[0] == 'participant':
                    pass
                else:
                    line = f"{row[1]} - {row[0]}"
                    if row[4] == 'False':
                        line = '~' + line + '~'
                    response = response + line + '\n'
        await ctx.send(response)
