from .base_plugin import BasePlugin
import requests
import random
import discord

class FunCommandsPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(
            help="Put a clap emoji between every word.",
            brief="I will clap for you."
        )
        async def clap(ctx, *, claptext):
            clapemoji = '👏'
            clapupper = str(claptext).upper().split()
            clapjoin = clapemoji.join(clapupper)
            await ctx.send(str(clapjoin) + clapemoji)

        @self.bot.command(
            help="Changes text provided into alternating case spongebob sarcastic memery.",
            brief="Spongebob your text."
        )
        async def sb(ctx, *, sbtext):
            sbemoji = "<:sb:755535426118484138>"
            res = ""
            for idx in range(len(sbtext)):
                if not idx % 2:
                    res = res + sbtext[idx].upper()
                else:
                    res = res + sbtext[idx].lower()
            await ctx.send(sbemoji)
            await ctx.send(str(res))

        @self.bot.command(
            help="Combines the awesome of sb and clap.",
            brief="Why not both?"
        )
        async def sbclap(ctx, *, sbclaptext):
            res = ""
            for idx in range(len(sbclaptext)):
                if not idx % 2:
                    res = res + sbclaptext[idx].upper()
                else:
                    res = res + sbclaptext[idx].lower()
            sbemoji = "<:sb:755535426118484138>"
            clapemoji = '👏'
            clapsplit = str(res).split()
            clapjoin = clapemoji.join(clapsplit)
            await ctx.send(sbemoji)
            await ctx.send(str(clapjoin) + clapemoji)

        @self.bot.command(
            help="Generates an image from inspirobot.",
            brief="Inspire me."
        )
        async def inspire(ctx):
            response = requests.get('https://inspirobot.me/api?generate=true')
            meme_url = response.text
            await ctx.send(f"{meme_url}")

        @self.bot.command(name='sgif')
        async def search_gif(ctx, *args):
            # Parse the user's input to extract the search query
            search_query = ' '.join(args)
            
            # Get GIPHY API key from environment
            import os
            giphy_api_key = os.getenv('GIPHY_API_KEY')
            
            if not giphy_api_key:
                await ctx.send("GIPHY API key not configured.")
                return

            # Retrieve the most popular GIF from the Giphy API based on the search query
            response = requests.get(f'http://api.giphy.com/v1/gifs/search?q={search_query}&api_key={giphy_api_key}&limit=1&rating=g&sort=popularity')

            gif_url = response.json()['data'][0]['images']['original']['url']

            # Create an embed with the GIF and send it to the Discord channel
            embed = discord.Embed()
            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
