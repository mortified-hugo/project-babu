from discord.ext import commands
import discord
import os
import asyncio

from guild_setup.functions import *
from guild_setup.checks import *
from guild_setup.roles_and_permissions import *


class GuildInitiation(commands.Cog):
    """Initiation Commands for evaluating if a guild is ready to play the game

    :param bot: bot to be run"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guild_pattern')
    @template_server()
    async def create_guild_pattern(self, ctx):
        """Overrides the definition of a valid server to play"""

        with open('guild_check.txt', mode='w') as file:
            code = str(gen_checker(guild_info(ctx)))
            file.write(code)
        await ctx.send('Pattern overridden')

    @commands.command(name='get_template')
    async def print_template(self, ctx):
        """Generates template link"""

        await ctx.send('https://discord.new/zqSamRGVfN5S')

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

    @commands.command(name='setup')  # DO NOT USE THIS COMMAND YET
    @is_mod()
    async def guild_setup(self, ctx):
        """Initiates guild setup, creating the basic roles and channels to play the game"""

        if check_guild(ctx):
            #  Creating Directory
            path = f'guilds/{ctx.guild.name}'
            try:
                os.mkdir(path)
            except OSError:
                await ctx.send('```Guild Directory could not be created```')

            #  Create Rolls
            await asyncio.sleep(1)
            await ctx.send('```Creating Rolls```')
            await ctx.guild.create_role(name='Dreader', permissions=no_permissions, hoist=True,
                                        color=discord.Colour.gold(), mentionable=True)
            await ctx.guild.create_role(name='Veto Power', permissions=no_permissions,
                                        color=discord.Colour.green(), mentionable=True)
            await ctx.guild.create_role(name='Follower', permissions=no_permissions,
                                        color=discord.Colour.blue(), mentionable=True)
            n = 1
            while n <= 20:
                await ctx.guild.create_role(name=f'{n}', permissions=no_permissions, mentionable=False)
                n += 1

            await ctx.guild.create_role(name='Participant', permissions=participant_permissions,
                                        hoist=True, mentionable=True)
            await ctx.guild.create_role(name='Spectator', permissions=spectator_permissions,
                                        hoist=True, mentionable=True)

            #  Create Categories
            await ctx.send('```Creating Categories for Channels```')
            await ctx.guild.create_category('Information', position=1)
            await ctx.guild.create_category('Game Channels', position=2)
            await ctx.guild.create_category('Confession Dial', position=3)
            await ctx.guild.create_category('Private Conversations', position=4)
            await ctx.guild.create_category('Moderation', position=5)
            await asyncio.sleep(1)

            await ctx.send('```Initial Setup Complete, please type .create_channels next```')

        else:
            await ctx.send('```This server cannot be setup```')

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Allows the role of spectator to be distributed to everyone else in the server"""

        #  Distribute roles
        if role.name == 'Spectator':
            for member in role.guild.members:
                if 'mod' in [role.name for role in member.roles]:
                    pass
                else:
                    await member.add_roles(role)
        else:
            pass
        await asyncio.sleep(1)

    @commands.command(name='create_channels')
    @is_mod()
    async def create_channels(self, ctx):
        """Setup command for creating the channels"""

        await ctx.send('```Creating Text Channels```')
        await ctx.guild.create_text_channel(name='spectator-hub',
                                            overwrites={get_role(ctx, 'Participant'): cannot_see,
                                                        get_role(ctx, 'Spectator'): can_see_and_write},
                                            category=ctx.guild.categories[0])
        await ctx.guild.create_text_channel(name='main-lounge',
                                            overwrites={get_role(ctx, 'Spectator'): can_read},
                                            category=ctx.guild.categories[1])
        await ctx.guild.create_text_channel(name='game-room',
                                            overwrites={get_role(ctx, 'Spectator'): can_read},
                                            category=ctx.guild.categories[1])
        await ctx.guild.create_voice_channel(name='Speaker',
                                             category=ctx.guild.categories[1])
        await ctx.guild.create_text_channel(name='feed',
                                            overwrites={get_role(ctx, 'Participant'): can_read,
                                                        get_role(ctx, 'Spectator'): can_read},
                                            category=ctx.guild.categories[0])
        await ctx.guild.create_text_channel(name='war-room',
                                            overwrites={get_role(ctx, 'Spectator'): can_read,
                                                        get_role(ctx, 'Participant'): cannot_see,
                                                        get_role(ctx, 'Follower'): can_see_and_write,
                                                        get_role(ctx, 'Dreader'): can_see_and_write},
                                            category=ctx.guild.categories[1])
        await ctx.guild.create_text_channel(name='mod-hub',
                                            overwrites={get_role(ctx, 'Spectator'): cannot_see,
                                                        get_role(ctx, 'Participant'): cannot_see,
                                                        get_role(ctx, 'mod'): can_see_and_write},
                                            category=ctx.guild.categories[4])
        await ctx.send("```This guild is setup```")

    @commands.command(name='test_roles')
    async def test_roles(self, ctx):
        participant = get_role(ctx, 'Participant')
        spectator = get_role(ctx, "Spectator")
        follower = get_role(ctx, 'Follower')
        mod = get_role(ctx, 'mod')
        dreader = get_role(ctx, 'Dreader')
        print(participant.name, spectator.name, follower.name, mod.name, dreader.name)

    @commands.command(name='give')
    async def give_roll(self, ctx, *members: discord.Member):
        for member in members:
            await member.add_roles(get_role(ctx, 'Participant'))
