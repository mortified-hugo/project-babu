def concatenate_list_data(input_list):
    """Creates a single string from every element of a list

    :param input_list: list input

    :return: an output string with the contents of list"""
    output_str = ''
    for element in input_list:
        output_str += str(element)
    return output_str


def guild_info(guild):
    """Creates a reference list for contents of a guild that need to be checked

    :param guild: context of command in discord

    :return: list of channels and roles"""
    channels = [channel.name for channel in guild.channels]
    roles = [role.name for role in guild.roles]
    return channels + roles


def gen_checker(discord_info):
    """Generates Check
    :param discord_info: information from a discord guild

    :return: int for a single check of the guild"""
    initial_info = concatenate_list_data(discord_info).casefold()
    numerals = "0123456789abcdefghijklmnopqrstuvwxyz"
    info_dump = concatenate_list_data([item for item in list(initial_info) if item in numerals])
    return int(info_dump, 36) * 101279  # Babu's birthday


def check_guild(guild):
    """Checks if guild is an appropriate server to start playing according to the rules
    :param guild: discord context

    :return: bool for the check"""
    guild_code = str(gen_checker(guild_info(guild)))
    with open('guild_check.txt', mode='r') as file:
        correct_code = str(file.read())
    return correct_code == guild_code


def get_role(ctx, role_name):
    """Returns the role object based on the role name

    :param ctx: context of the discord guild
    :param role_name: str representing the discord role name

    :return: discord.Role Object"""
    desired_role = None
    for role in ctx.guild.roles:
        if str(role.name) == str(role_name):
            desired_role = role
        else:
            pass
    return desired_role


def get_category(ctx, category_name):
    """Returns the category object based on the category name

    :param ctx: context of the discord guild
    :param category_name: str representing the discord role name

    :return: discord.Role Object"""
    desired_category = None
    for category in ctx.guild.roles:
        if str(category.name) == str(category_name):
            desired_category = category
        else:
            pass
    return desired_category
