import json
import os
import asyncio
from discord.ext import commands
import discord

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

def create_bot_instance(name, conf):
    prefix = conf.get("prefix", "!")
    intents = discord.Intents.all()
    intents.typing = False
    intents.presences = False
    
    bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
    bot._instance_name = name  # metadata
    
    # Load plugins dynamically
    from plugins import ALL_PLUGINS
    for plugin_cls in ALL_PLUGINS:
        plugin = plugin_cls(bot, conf)
        plugin.setup()
    
    return bot

async def run_bot(bot, token):
    try:
        await bot.start(token)
    except Exception as e:
        print(f"Error starting bot {bot._instance_name}: {e}")

async def main():
    config = load_config()
    bots = []
    
    for instance_name, conf in config.items():
        token = conf.get("token")
        if not token or token == f"YOUR_{instance_name.upper()}_TOKEN_HERE":
            print(f"Warning: No valid token found for {instance_name}")
            continue
            
        bot = create_bot_instance(instance_name, conf)
        bots.append((bot, token))
    
    if not bots:
        print("No valid bot configurations found. Please check your config.json and tokens.")
        return
    
    # Run all bots concurrently
    tasks = [run_bot(bot, token) for bot, token in bots]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
