from discord.ext import commands

from functions import *


class GuildInitiation(commands.Cog):
    """Initiation Commands for evaluating if a guild is ready to play the game

    :param bot: bot to be run"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guild_pattern')
    async def create_guild_pattern(self, ctx):
        """Overrides the definition of a valid server to play"""
        with open('guild_check.txt', mode='w') as file:
            code = str(gen_checker(guild_info(ctx)))
            file.write(code)
        await ctx.send('Pattern overridden')

    @commands.command(name='check_guild')
    async def check_guild_command(self, ctx):
        """Checks if guild is an appropriate server to start playing according to the rules

        :param ctx: discord context

        :return: response to context whether the guild is appropriate to play"""
        checker = check_guild(ctx)
        if checker:
            response = '```This server can be used to play```'
        else:
            response = '```This server cannot be used to play.\n' \
                       'Please check the rules on how to organize your server for the game```'
        await ctx.send(str(response))
