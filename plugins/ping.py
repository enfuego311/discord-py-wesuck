from .base_plugin import BasePlugin

class PingPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="ping")
        async def ping_cmd(ctx):
            await ctx.send(f"Pong from {self.bot._instance_name}!")
