from .base_plugin import BasePlugin

class WeatherPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="weather")
        async def weather(ctx, *args):
            """Stub for weather command; port original logic here.""" 
            await ctx.send("Weather command not implemented yet.")
