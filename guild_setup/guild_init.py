import os
import shutil
import asyncio
import numpy as np

from functions import *
from checks import *
from guild_setup.roles_and_permissions import *


class GuildInitiation(commands.Cog):
    """Initiation Commands for evaluating if a guild is ready to play the game

    :param bot: bot to be run"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Creates folder for guild"""

        if check_guild(guild):
            #  Creating Directory
            path = f'guilds/{guild.name}'
            try:
                os.mkdir(path)
            except OSError:
                await guild.channels[0].send('```Guild Directory could not be created```')

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        """Deletes guild folder on guild leave"""

        if check_guild(guild):
            shutil.rmtree(f'guilds/{guild.name}')

    #  Utility commands

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            await member.add_roles(get_role(member, 'Spectator'))
        except AttributeError:
            pass

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
        shutil.rmtree(f'guilds/{ctx.guild.name}')
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

    @commands.command()
    @is_mod()
    async def reset_players(self, ctx):
        for channel in ctx.guild.channels:
            if channel.category is None:
                pass
            elif channel.category.name == 'Confession Dial' or channel.category.name == 'Private Conversations':
                await channel.delete()
            else:
                pass
        for member in ctx.guild.members:
            if get_role(ctx, 'Participant') in member.roles:
                await member.remove_roles(*[role for role in member.roles if role.name != '@everyone'])
                await member.add_roles(get_role(ctx, 'Spectator'))
            else:
                pass
        await ctx.send('Players Reset')

    @commands.command(name='get_template')
    async def print_template(self, ctx):
        """Generates template link"""

        await ctx.send('https://discord.new/zqSamRGVfN5S')

    @commands.command(name='check_guild')
    async def check_guild_command(self, ctx):
        """Checks if guild is an appropriate server to start playing according to the rules

        :param ctx: discord context

        :return: response to context whether the guild is appropriate to play"""

        checker = check_guild(ctx.guild)
        if checker:
            response = '```This server can be used to play```'
        else:
            response = '```This server cannot be used to play.\n' \
                       'Please check the rules on how to organize your server for the game```'
        await ctx.send(str(response))

    @commands.command(name='test_roles')
    async def test_roles(self, ctx):
        """Testing for the role creation, console only"""

        participant = get_role(ctx, 'Participant')
        spectator = get_role(ctx, "Spectator")
        follower = get_role(ctx, 'Follower')
        mod = get_role(ctx, 'mod')
        dreader = get_role(ctx, 'Dreader')
        print(participant.name, spectator.name, follower.name, mod.name, dreader.name)

    #  Setup Commands
    @commands.command()
    async def _create_numbered_roles(self, ctx, n=1):
        while n <= 12:  # NUMBER MUST BE CONFIGURABLE
            await ctx.guild.create_role(name=f'{n}', permissions=no_permissions, mentionable=False)
            n += 1

    @commands.command()
    async def _create_roles(self, ctx):
        await asyncio.sleep(1)
        await ctx.send('```Creating Rolls```')
        await ctx.guild.create_role(name='Dreader', permissions=no_permissions, hoist=True,
                                    color=discord.Colour.gold(), mentionable=True)
        await ctx.guild.create_role(name='Veto Power', permissions=no_permissions,
                                    color=discord.Colour.green(), mentionable=True)
        await ctx.guild.create_role(name='Follower', permissions=no_permissions,
                                    color=discord.Colour.blue(), mentionable=True)

        await ctx.invoke(self.bot.get_command('_create_numbered_roles'))

        await ctx.guild.create_role(name='Participant', permissions=participant_permissions,
                                    hoist=True, mentionable=True)
        await ctx.guild.create_role(name='Spectator', permissions=spectator_permissions,
                                    hoist=True, mentionable=True)

    @commands.command()
    async def _create_categories(self, ctx):

        await ctx.send('```Creating Categories for Channels```')
        await ctx.guild.create_category('Information', position=1)
        await ctx.guild.create_category('Game Channels', position=2)
        await ctx.guild.create_category('Moderation', position=5)

        await ctx.guild.create_category('Confession Dial', position=3)
        await ctx.guild.create_category('Private Conversations', position=4)

    @commands.command()
    async def _create_channels(self, ctx):

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
        await ctx.guild.create_text_channel(name='commands',
                                            overwrites={get_role(ctx, 'Spectator'): cannot_see,
                                                        get_role(ctx, 'Participant'): cannot_see,
                                                        get_role(ctx, 'mod'): can_see_and_write},
                                            category=ctx.guild.categories[4])
        await ctx.send('```Channels Created```')

    @commands.command()
    async def _distribute_role(self, ctx, role_name):

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

    @commands.command(name='setup')
    @is_mod()
    async def guild_setup(self, ctx):
        """Initiates guild setup, creating the basic roles and channels to play the game

        It will invoke a series of internal commands to create the necessary roles, channels and categories for a guild
        This command will only work in guilds which follow the specified template
        """

        if check_guild(ctx.guild):

            #  Creating Directory
            path = f'guilds/{ctx.guild.name}'
            try:
                os.mkdir(path)
            except OSError:
                await ctx.send('```Guild Directory could not be created```')

            #  Create Rolls
            await ctx.invoke(self.bot.get_command('_create_roles'))
            await asyncio.sleep(1)

            #  Create Categories
            await ctx.invoke(self.bot.get_command('_create_categories'))
            await asyncio.sleep(1)

            #  Create Channels
            await ctx.invoke(self.bot.get_command('_create_channels'))
            await asyncio.sleep(1)

            #  Distributing Roles
            await ctx.invoke(self.bot.get_command('_distribute_role'), role_name='Spectator')
            await asyncio.sleep(1)

            await ctx.send("```This guild is setup```")

        else:
            await ctx.send('```This server cannot be setup```')

    @commands.command()
    async def _send_welcome_message(self, ctx):
        for channel in ctx.guild.text_channels:
            try:
                number = int(channel.name)
                message = f'Welcome {get_player(number, ctx.guild)}!'
                await channel.send(message)
            except ValueError:
                pass

    @commands.command(name='players')
    @is_mod()
    @game_has_not_started()
    async def players(self, ctx, *members_tuple: discord.Member):
        """Add players to the game. This command should only be invoked once

        :param ctx: discord context.
        :param members_tuple: a list of members that will become players. All members in this list will be assigned
        a number and will be designated a participant of the game

        :returns: configures the guild according the list of players"""
        if len(members_tuple) >= 5:

            #  Generate Player Data
            data = []
            members = list(members_tuple)
            numbers = [str(n) for n in range(1, len(members) + 1)]
            for member in members:
                member_number = numbers[np.random.randint(0, len(numbers))]
                numbers.remove(member_number)
                await member.remove_roles(get_role(ctx, 'Spectator'))
                await member.add_roles(get_role(ctx, 'Participant'),
                                       get_role(ctx, member_number))
                data.append([member_number, str(member.display_name), '10', '0', 'True', 'None'])
            create_hate_fandom_csv(data, ctx)
            for role in ctx.guild.roles:
                try:
                    number = int(role.name)
                    if number <= len(members):
                        await ctx.guild.create_text_channel(name=f'{number}',
                                                            overwrites={get_role(ctx, f'{number}'): can_see_and_write,
                                                                        get_role(ctx, 'Participant'): cannot_see,
                                                                        get_role(ctx, 'Spectator'): can_read},
                                                            category=ctx.guild.categories[2])
                    else:
                        pass
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

            await ctx.invoke(self.bot.get_command('_send_welcome_message'))
            await ctx.send('``` Roles Distributed ```')
        else:
            await ctx.send('``` Too few players, please add at least 5 ```')
