import discord


#  Spectator Role
spectator_permissions = discord.Permissions(read_messages=True, read_message_history=True,
                                            add_reactions=True, connect=True)

#  Participant Role
participant_permissions = discord.Permissions(read_messages=True, send_messages=True, embed_links=True,
                                              attach_files=True, read_message_history=True, add_reactions=True,
                                              connect=True, mention_everyone=True)

#  Follower Role
follower_permissions = discord.Permissions()

#  Veto Power Role
veto_power_permissions = discord.Permissions()

#  Dreader Role
dreader_permissions = discord.Permissions()
