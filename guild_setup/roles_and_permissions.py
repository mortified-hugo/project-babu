import discord


#  Spectator Role
spectator_permissions = discord.Permissions(read_messages=True, read_message_history=True,
                                            add_reactions=True, connect=True)

#  Participant Role
participant_permissions = discord.Permissions(read_messages=True, send_messages=True, embed_links=True,
                                              attach_files=True, read_message_history=True, add_reactions=True,
                                              connect=True, mention_everyone=True)

#  No Special Permissions
no_permissions = discord.Permissions()


#  Can see but not post
can_read = discord.PermissionOverwrite(read_messages=True, send_messages=False)

#  Cannot see
cannot_see = discord.PermissionOverwrite(read_messages=False, send_messages=False)

# Can see and write
can_see_and_write = discord.PermissionOverwrite(read_messages=True, send_messages=True)