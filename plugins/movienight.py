from .base_plugin import BasePlugin
import os
import random

class MovieNightPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="movienight")
        async def movienight(ctx, *args):
            """Respond with a random movie night message."""
            try:
                filepath = os.path.join('txt', 'movienight.txt')
                with open(filepath, 'r') as f:
                    lines = f.read().splitlines()
                if lines:
                    await ctx.send(random.choice(lines))
                else:
                    await ctx.send("No movie night quotes found.")
            except Exception as e:
                await ctx.send(f"Error reading movie night lines: {e}")
