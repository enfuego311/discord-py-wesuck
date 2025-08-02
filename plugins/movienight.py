from .base_plugin import BasePlugin

class MovieNightPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="movienight")
        async def movienight(ctx, *args):
            """Stub for movie night logic.""" 
            await ctx.send("Movie night command not implemented yet.")
