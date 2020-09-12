from functions import *
import numpy as np


class Contestant:
    """Contestants may be eliminated from the game soon, so some extra information about them is required

    :param name: discord.Member.display_name
    :param guild: discord.Guild"""

    def __init__(self, name, guild):
        self.name = name
        self.hate = get_hate(name, guild)
        self.fandom = get_fandom(name, guild)
        self.attack = None
        self.base = self.hate
        self.f = np.random.randint(1, 100)
        self.changed_attack = False
        self.vote = 0



