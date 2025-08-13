import json
import os
import asyncio
import importlib
import pkgutil
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

    # load plugin enablement info for this instance
    plugins_conf = conf.get("plugins", {})  # could be per-bot or global depending on layout

    # Discover all plugin modules in plugins/
    import plugins  # the package
    for finder, module_name, ispkg in pkgutil.iter_modules(plugins.__path__):
        module = importlib.import_module(f"plugins.{module_name}")
        enabled = True
        # Example: config.json nests under top-level "plugins", adjust as needed
        bot_plugins = conf.get("plugins", {})
        plugin_entry = bot_plugins.get(module_name, {})
        if isinstance(plugin_entry, dict):
            enabled = plugin_entry.get("enabled", True)
        if not enabled:
            continue

        # Support both class-based and function-style
        if hasattr(module, "register"):
            # function style: ping.py
            module.register(bot, conf)
        else:
            # class style: look for a class with predictable naming
            # e.g., KeywordResponsePlugin in keyword_response.py
            cls_candidates = [getattr(module, attr) for attr in dir(module)
                              if attr.lower().endswith("plugin")]
            for cls in cls_candidates:
                try:
                    inst = cls(bot, conf)
                    inst.setup()
                except Exception:
                    pass  # or log
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
