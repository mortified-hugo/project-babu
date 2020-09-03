from discord.ext import commands

template_guild_id = 750515487825199225


def template_server():
    """Definition of the template server to be used to overrule server config"""

    def predicate(ctx):
        return ctx.guild and ctx.guild.id == template_guild_id

    return commands.check(predicate)


def is_mod():
    """Definition of a moderator"""

    def predicate(ctx):
        role_names = [role.name for role in ctx.author.roles]
        return 'mod' in role_names

    return commands.check(predicate)
