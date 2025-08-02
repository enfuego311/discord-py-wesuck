import aiohttp
import json
import os
import discord
from .base_plugin import BasePlugin


class WeatherPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(
            name="weather",
            pass_context=True,
            help="This will query the google maps api to get the latitude and longitude. Using that it will query the OpenWeather API for local conditions.",
            brief="Weather for the location specified."
        )
        async def weather(ctx, *, search):
            googleapi = os.getenv('GOOGLE_API_KEY')
            weatherapi = os.getenv('WEATHER_API_KEY')
            session = aiohttp.ClientSession()
            session2 = aiohttp.ClientSession()
            search = search.replace(' ', '+')

            # Get latitude and longitude
            georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)
            geodata = json.loads(await georesp.text())
            geolat = str(geodata['results'][0]['geometry']['location']['lat'])
            geolon = str(geodata['results'][0]['geometry']['location']['lng'])

            # Query the weather API
            weatheresp = await session2.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')
            weatherdata = json.loads(await weatheresp.text())

            # Create the embed
            locmapurl = f'https://maps.googleapis.com/maps/api/staticmap?center={geolat},{geolon}&zoom=11&size=600x300&key={googleapi}'
            temp = str(weatherdata['main']['temp'])
            city = weatherdata['name']
            country = weatherdata['sys']['country']
            cond = weatherdata['weather'][0]['description']
            feelslike = str(weatherdata['main']['feels_like'])
            humidity = str(weatherdata['main']['humidity'])
            wind_speed = str(weatherdata['wind']['speed'])

            embed = discord.Embed(title=f"Weather for {city} {country}", colour=discord.Colour.blue())
            embed.set_image(url=locmapurl)
            embed.add_field(name="Current Temp (Feels Like)", value=f"{temp}F ({feelslike}F)")
            embed.add_field(name="Conditions", value=cond)
            embed.add_field(name="Wind Speed", value=f"{wind_speed} mph")
            embed.add_field(name="Humidity", value=f"{humidity}%")

            await session.close()
            await session2.close()
            await ctx.send(embed=embed)
