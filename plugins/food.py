from .base_plugin import BasePlugin
import requests
import discord

class FoodPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(name="food")
        async def food(ctx, upc_code: str = None):
            if not upc_code:
                await ctx.send('Please provide a UPC code.')
                return

            url = f"https://world.openfoodfacts.org/api/v0/product/{upc_code}.json"
            response = requests.get(url)
            data = response.json()

            if data.get('status') != 1:
                await ctx.send('No nutrition information found for the provided UPC code.')
                return

            product = data['product']
            embed = discord.Embed(
                title=product.get('product_name', 'Unknown Product'),
                description=f"Nutrition information for {product.get('product_name', 'this product')}",
                color=0x00ff00
            )
            embed.add_field(name="Brand", value=product.get('brands', 'N/A'), inline=False)
            embed.add_field(name="Serving Size", value=product.get('serving_size', 'N/A'), inline=False)
            embed.add_field(name="Calories", value=product.get('nutriments', {}).get('energy-kcal_100g', 'N/A'), inline=True)
            embed.add_field(name="Total Fat", value=product.get('nutriments', {}).get('fat_100g', 'N/A'), inline=True)
            embed.add_field(name="Saturated Fat", value=product.get('nutriments', {}).get('saturated-fat_100g', 'N/A'), inline=True)
            embed.add_field(name="Cholesterol", value=product.get('nutriments', {}).get('cholesterol_100g', 'N/A'), inline=True)
            embed.add_field(name="Sodium", value=product.get('nutriments', {}).get('sodium_100g', 'N/A'), inline=True)
            embed.add_field(name="Total Carbohydrates", value=product.get('nutriments', {}).get('carbohydrates_100g', 'N/A'), inline=True)
            embed.add_field(name="Dietary Fiber", value=product.get('nutriments', {}).get('fiber_100g', 'N/A'), inline=True)
            embed.add_field(name="Sugars", value=product.get('nutriments', {}).get('sugars_100g', 'N/A'), inline=True)
            embed.add_field(name="Protein", value=product.get('nutriments', {}).get('proteins_100g', 'N/A'), inline=True)

            await ctx.send(embed=embed)
