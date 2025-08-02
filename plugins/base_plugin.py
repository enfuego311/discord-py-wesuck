from discord.ext import commands

class BasePlugin:
    def __init__(self, bot: commands.Bot, config: dict):
        self.bot = bot
        self.config = config

    def setup(self):
        """Register commands/events onto self.bot.""" 
        raise NotImplementedError
