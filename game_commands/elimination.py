import pickle
import discord
from checks import *


class EliminationContest(commands.Cog):
    """Elimination Contest Cog with the commands for creating the elimination contest and simulating it"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_mod()
    async def indicate_player(self, *players: discord.Member):
        #Return instance of a Player class member for each player in the players list

        pass
