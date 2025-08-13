from .base_plugin import BasePlugin
import requests
import discord
from io import BytesIO

class ImageCommandsPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name='driveway')
        async def driveway(ctx):
            # Get REOURL from environment
            import os
            reourl = os.getenv('REOURL')
            
            if not reourl:
                await ctx.send("REOURL not configured.")
                return

            # Download the image data using requests
            response = requests.get(reourl, verify=False)
            image_data = response.content

            # Wrap the image data in a BytesIO object to create a file-like object
            file = BytesIO(image_data)
            file.name = "image.jpg"

            # Create an embedded message with the file
            embed = discord.Embed(title="A Driveway", description="Here's a picture of a driveway:")
            embed.set_image(url="attachment://image.jpg")

            # Send the message with the embedded file
            await ctx.send(file=discord.File(file), embed=embed)

        @self.bot.command(name='backyard')
        async def backyard(ctx):
            # Get REOURL2 from environment
            import os
            reourl2 = os.getenv('REOURL2')
            
            if not reourl2:
                await ctx.send("REOURL2 not configured.")
                return

            # Download the image data using requests
            response = requests.get(reourl2, verify=False)
            image_data = response.content

            # Wrap the image data in a BytesIO object to create a file-like object
            file = BytesIO(image_data)
            file.name = "image.jpg"

            # Create an embedded message with the file
            embed = discord.Embed(title="A Back Yard", description="Here's a picture of a back yard:")
            embed.set_image(url="attachment://image.jpg")

            # Send the message with the embedded file
            await ctx.send(file=discord.File(file), embed=embed)
