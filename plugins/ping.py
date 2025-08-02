# plugins/ping.py
def register(bot, config):
    @bot.command(name="ping")
    async def ping_cmd(ctx):
        await ctx.send(f"Pong from {bot._instance_name}!")
