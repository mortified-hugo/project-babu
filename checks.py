from discord.ext import commands

template_guild_id = 750515487825199225


#  Special Guild Check
def template_server():
    """Definition of the template server to be used to overrule server config"""

    def predicate(ctx):
        return ctx.guild and ctx.guild.id == template_guild_id

    return commands.check(predicate)


#  Role Checkers
def is_mod():
    """Definition of a moderator"""

    def predicate(ctx):
        role_names = [role.name for role in ctx.author.roles]
        return 'mod' in role_names

    return commands.check(predicate)


def is_player():
    """Definition of a moderator"""

    def predicate(ctx):
        role_names = [role.name for role in ctx.author.roles]
        return 'Participant' in role_names

    return commands.check(predicate)


#  Game Status Checkers
def game_has_not_started():
    """Definition of a game yet to start"""

    def predicate(ctx):
        text_channels = [text_channel.name for text_channel in ctx.guild.text_channels]
        return '1' not in text_channels

    return commands.check(predicate)
