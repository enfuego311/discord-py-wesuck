from .base_plugin import BasePlugin
import requests
import subprocess
import re
import discord

class UtilityPlugin(BasePlugin):
    def setup(self):
        # Allowed users for repeat command
        self.allowed_ids = [340495492377077905, 181093076960411648]

        @self.bot.command(name='ping')
        async def ping_host(ctx, host):
            try:
                # Run the ping command and capture the output
                process = subprocess.Popen(['ping', '-c', '3', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()

                # Extract the round-trip time from the output
                output_str = output.decode('utf-8')
                rtts = [float(x.split('=')[-1].split(' ')[0]) for x in output_str.split('\n') if 'time=' in x]

                # Calculate the average round-trip time and send it to the Discord channel
                avg_rtt = sum(rtts) / len(rtts)
                await ctx.send(f'Average round-trip time to {host}: {avg_rtt:.2f} ms')

            except Exception as e:
                await ctx.send(f'Error: {e}')

        @self.bot.command(name="ip")
        async def ip(ctx):
            ip = requests.get('https://api.ipify.org').text
            await ctx.send(f"My public IP: {ip}")

        @self.bot.command(name="repeat")
        async def repeat(ctx, channel_mention, *, message):
            if ctx.author.id not in self.allowed_ids:
                await ctx.send("You are not allowed to use this command.")
                return

            channel_id = re.findall(r'\d+', channel_mention)[0]
            channel = self.bot.get_channel(int(channel_id))
            await channel.send(message)

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Game(name="Tic-Tac-Toe against Joshua"))
            print('Logged in as')
            print(self.bot.user.name)
            print(self.bot.user.id)
            print('------')
