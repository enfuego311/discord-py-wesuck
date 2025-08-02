import json
from discord.ext import commands

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

def create_bot_instance(name, conf):
    prefix = conf.get("prefix", "!")
    bot = commands.Bot(command_prefix=prefix, help_command=None)
    bot._instance_name = name  # metadata

    # Plugins should be imported here dynamically in real usage.
    # from plugins import ALL_PLUGINS
    # for plugin_cls in ALL_PLUGINS:
    #     plugin = plugin_cls(bot, conf)
    #     plugin.setup()
    return bot

def main():
    config = load_config()
    for instance_name, conf in config.items():
        token = conf.get("token")
        bot = create_bot_instance(instance_name, conf)
        print(f"Would start bot '{instance_name}' with its token here.")
        # bot.run(token)  # Uncomment when ready

if __name__ == "__main__":
    main()
