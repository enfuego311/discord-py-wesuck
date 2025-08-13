#!/usr/bin/env python3
"""
Main entry point for the Discord bot.
This file provides a traditional single-bot startup for those who prefer it over the multi-bot approach.
"""

import os
import asyncio
from discord.ext import commands
import discord

# Import all plugins
from plugins import ALL_PLUGINS

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

if not TOKEN:
    print("Error: DISCORD_TOKEN environment variable not set!")
    exit(1)

# Create bot instance
intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=PREFIX, help_command=None, intents=intents)

# Load all plugins
for plugin_cls in ALL_PLUGINS:
    plugin = plugin_cls(bot, {})
    plugin.setup()
    print(f"Loaded plugin: {plugin_cls.__name__}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Tic-Tac-Toe against Joshua"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def main():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
