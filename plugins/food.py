from .base_plugin import BasePlugin

class FoodPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="food")
        async def food(ctx, upc_code: str = None):
            """Stub for food command; port original logic here.""" 
            await ctx.send("Food command not implemented yet.")
