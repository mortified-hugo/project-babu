from discord.ext import commands
import discord
import os
import asyncio
import numpy as np
import pandas as pd

from guild_setup.functions import *
from guild_setup.checks import *
from guild_setup.roles_and_permissions import *


class GuildInitiation(commands.Cog):
    """Initiation Commands for evaluating if a guild is ready to play the game

    :param bot: bot to be run"""

    def __init__(self, bot):
        self.bot = bot

    #  Utility commands

    @commands.command(name='guild_pattern')
    @template_server()
    async def create_guild_pattern(self, ctx):
        """Overrides the definition of a valid server to play"""

        with open('guild_check.txt', mode='w') as file:
            code = str(gen_checker(guild_info(ctx)))
            file.write(code)
        await ctx.send('Pattern overridden')

    @commands.command(name='reset_guild')
    @is_mod()
    async def reset_server(self, ctx):
        os.rmdir(f'guilds/{ctx.guild.name}')
        for channel in ctx.guild.channels:
            if channel.name != 'entrance':
                await channel.delete()
            else:
                pass
        for role in ctx.guild.roles:
            if role.name != 'mod' and role.name != self.bot.user.name and role.name != '@everyone':
                await role.delete()
            else:
                pass
        await ctx.send('```Guild reset```')

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

    @commands.command(name='test_roles')
    async def test_roles(self, ctx):
        participant = get_role(ctx, 'Participant')
        spectator = get_role(ctx, "Spectator")
        follower = get_role(ctx, 'Follower')
        mod = get_role(ctx, 'mod')
        dreader = get_role(ctx, 'Dreader')
        print(participant.name, spectator.name, follower.name, mod.name, dreader.name)

    #  Setup Commands

    @commands.command(name='create_roles')
    async def create_roles(self, ctx):
        await asyncio.sleep(1)
        await ctx.send('```Creating Rolls```')
        await ctx.guild.create_role(name='Dreader', permissions=no_permissions, hoist=True,
                                    color=discord.Colour.gold(), mentionable=True)
        await ctx.guild.create_role(name='Veto Power', permissions=no_permissions,
                                    color=discord.Colour.green(), mentionable=True)
        await ctx.guild.create_role(name='Follower', permissions=no_permissions,
                                    color=discord.Colour.blue(), mentionable=True)
        n = 1
        while n <= 8:
            await ctx.guild.create_role(name=f'{n}', permissions=no_permissions, mentionable=False)
            n += 1

        await ctx.guild.create_role(name='Participant', permissions=participant_permissions,
                                    hoist=True, mentionable=True)
        await ctx.guild.create_role(name='Spectator', permissions=spectator_permissions,
                                    hoist=True, mentionable=True)

    @commands.command(name='create_categories')
    async def create_categories(self, ctx):
        """Creates the necessary categories"""

        await ctx.send('```Creating Categories for Channels```')
        await ctx.guild.create_category('Information', position=1)
        await ctx.guild.create_category('Game Channels', position=2)
        await ctx.guild.create_category('Moderation', position=5)

        await ctx.guild.create_category('Confession Dial', position=3)
        await ctx.guild.create_category('Private Conversations', position=4)

    @commands.command(name='create_channels')
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
        await ctx.send('```Channels Created```')

    @commands.command()
    async def distribute_role(self, ctx, role_name):
        """Allows the role of spectator to be distributed to everyone else in the server"""

        #  Distribute roles
        role = get_role(ctx, role_name)
        for member in ctx.guild.members:
            if 'mod' in [role.name for role in member.roles]:
                pass
            else:
                await member.add_roles(role)
        else:
            pass
        await asyncio.sleep(1)

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
            await ctx.invoke(self.bot.get_command('create_roles'))
            await asyncio.sleep(1)

            #  Create Categories
            await ctx.invoke(self.bot.get_command('create_categories'))
            await asyncio.sleep(1)

            #  Create Channels
            await ctx.invoke(self.bot.get_command('create_channels'))
            await asyncio.sleep(1)

            #  Distributing Roles
            await ctx.invoke(self.bot.get_command('distribute_role'), role_name='Spectator')
            await asyncio.sleep(1)

            await ctx.send("```This guild is setup```")

        else:
            await ctx.send('```This server cannot be setup```')

    @commands.command(name='players')
    @is_mod()
    async def player(self, ctx, *members_tuple: discord.Member):
        data = []
        members = list(members_tuple)
        numbers = [str(n) for n in range(1, len(members) + 1)]
        for member in members:
            member_number = numbers[np.random.randint(0, len(numbers))]
            numbers.remove(member_number)
            await member.remove_roles(get_role(ctx, 'Spectator'))
            await member.add_roles(get_role(ctx, 'Participant'),
                                   get_role(ctx, member_number))
            data.append([member_number, str(member.display_name), '10', '0'])
        df = pd.DataFrame(data=data, columns=['Number', 'Participant', 'Hate', 'Fandom'])
        df.to_csv(f'guilds/{ctx.guild.name}/hate-fandom.csv')
        for role in ctx.guild.roles:
            try:
                number = int(role.name)
                if number > len(members):
                    await role.delete()
                else:
                    await ctx.guild.create_text_channel(name=f'{number}',
                                                        overwrites={get_role(ctx, f'{number}'): can_see_and_write,
                                                                    get_role(ctx, 'Participant'): cannot_see,
                                                                    get_role(ctx, 'Spectator'): can_read},
                                                        category=ctx.guild.categories[2])
            except ValueError:
                pass
        n = 1
        while n <= len(members) - 1:
            m = n + 1
            while m <= len(members):
                await ctx.guild.create_text_channel(name=f'{n} and {m}',
                                                    overwrites={get_role(ctx, f'{n}'): can_see_and_write,
                                                                get_role(ctx, f'{m}'): can_see_and_write,
                                                                get_role(ctx, 'Participant'): cannot_see,
                                                                get_role(ctx, 'Spectator'): can_read},
                                                    category=ctx.guild.categories[3])
                m += 1
            n += 1

        await ctx.send('``` Roles Distributed ```')
