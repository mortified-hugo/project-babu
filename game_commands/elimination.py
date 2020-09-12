import pickle
import discord
from varname import nameof

from checks import *
from functions import *
from game_commands.Contestant import Contestant


class EliminationContest(commands.Cog):
    """Elimination Contest Cog with the commands for creating the elimination contest and simulating it"""

    def __init__(self, bot):
        self.bot = bot

    #  Preparing a list of players to join the elimination contest
    @commands.command()
    @is_mod()
    async def indicate_player(self, ctx, *players: discord.Member):
        """Indicates a player or multiple player for the elimination contest"""
        try:
            contestant_names = load_variable(ctx.guild, 'contestant_names')
        except FileNotFoundError:
            contestant_names = []
        for player in players:
            if player.display_name in contestant_names:
                pass
            else:
                contestant_names.append(player.display_name)
        save_variable(ctx.guild, contestant_names, nameof(contestant_names))
        await ctx.send('Players set as contestants for elimination')

    @commands.command()
    async def check_contestants(self, ctx):
        contestant_names = load_variable(ctx.guild, 'contestant_names')
        response = '```The following players are indicated for an elimination contest:\n'
        for name in contestant_names:
            line = name + '\n'
            response = response + line

        await ctx.send(response + '```')

    @commands.command()
    @is_mod()
    async def reset_contestants(self, ctx):
        contestant_names = []
        save_variable(ctx.guild, contestant_names, nameof(contestant_names))
        await ctx.send('```Contestants reset```')

    @commands.command()
    @is_mod()
    async def revoke_indication(self, ctx, *players: discord.Member):
        contestant_names = load_variable(ctx.guild, 'contestant_names')
        for player in players:
            if player.display_name in contestant_names:
                contestant_names.remove(player.display_name)
            else:
                await ctx.send(f'```{player.display_name} is not indicated```')
        save_variable(ctx.guild, contestant_names, nameof(contestant_names))

        await ctx.send("```list updated```")

    # ADD TRANSFORMATION INTO A PROPER LIST OF CONTESTANT OBJECTS
    @commands.command()
    async def _start_contest(self, ctx):
        contestant_names = load_variable(ctx.guild, 'contestant_names')
        on_the_hook = [Contestant(player, ctx.guild) for player in contestant_names]
        save_variable(ctx.guild, on_the_hook, nameof(on_the_hook))

    # ADD ROUNDS
    # ADD COMMANDS FOR CONCLUDING THE ELIMINATION PROCESS

