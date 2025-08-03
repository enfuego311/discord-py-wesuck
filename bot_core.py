import json
from discord.ext import commands

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

import importlib
import pkgutil
import os

def create_bot_instance(name, conf):
    prefix = conf.get("prefix", "!")
    bot = commands.Bot(command_prefix=prefix, help_command=None)
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


def main():
    config = load_config()
    for instance_name, conf in config.items():
        token = conf.get("token")
        bot = create_bot_instance(instance_name, conf)
        print(f"Would start bot '{instance_name}' with its token here.")
        bot.run(token)  # Uncomment when ready

if __name__ == "__main__":
    main()
