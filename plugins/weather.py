import aiohttp
import json
import os
import discord
from .base_plugin import BasePlugin


class WeatherPlugin(BasePlugin):
    def setup(self):
        @self.bot.command(
            name="weather",
            help="This will query the google maps api to get the latitude and longitude. Using that it will query the OpenWeather API for local conditions.",
            brief="Weather for the location specified."
        )
        async def weather(ctx, *, search):
            # Get API keys from environment
            googleapi = os.getenv('GOOGLE_API_KEY')
            weatherapi = os.getenv('WEATHER_API_KEY')
            
            if not googleapi or not weatherapi:
                await ctx.send("Weather API keys not configured.")
                return

            async with aiohttp.ClientSession() as session:
                search = search.replace(' ', '+')
                # get our latitude and longitude
                georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)

                geodata = json.loads(await georesp.text())
                if not geodata.get('results'):
                    await ctx.send('Location not found.')
                    return
                    
                geolat = str(geodata['results'][0]['geometry']['location']['lat'])
                geolon = str(geodata['results'][0]['geometry']['location']['lng'])
                
                # pass the lat and lon to the weather api
                weatheresp = await session.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')

                weatherdata = json.loads(await weatheresp.text())
                
                # create the map url for the embed
                locmapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + \
                    geolat + ',' + geolon + '&zoom=11&size=600x300&key=' + googleapi

                # Create weather embed
                embed = discord.Embed(
                    title=f"Weather in {search.replace('+', ' ')}",
                    description=f"Current weather conditions",
                    color=0x00ff00
                )
                
                if 'main' in weatherdata:
                    temp = weatherdata['main'].get('temp', 'N/A')
                    humidity = weatherdata['main'].get('humidity', 'N/A')
                    pressure = weatherdata['main'].get('pressure', 'N/A')
                    
                    embed.add_field(name="Temperature", value=f"{temp}°F", inline=True)
                    embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
                    embed.add_field(name="Pressure", value=f"{pressure} hPa", inline=True)
                
                if 'weather' in weatherdata and weatherdata['weather']:
                    description = weatherdata['weather'][0].get('description', 'N/A')
                    embed.add_field(name="Conditions", value=description, inline=False)
                
                if 'wind' in weatherdata:
                    wind_speed = weatherdata['wind'].get('speed', 'N/A')
                    embed.add_field(name="Wind Speed", value=f"{wind_speed} mph", inline=True)
                
                embed.set_image(url=locmapurl)
                await ctx.send(embed=embed)

        @self.bot.command(
            name="forecast",
            help="This will query the Google Maps API to get the latitude and longitude. Using that it will query the OpenWeather API for a local forecast.",
            brief="Forecast for the location specified."
        )
        async def forecast(ctx, *, search):
            # Get API keys from environment
            googleapi = os.getenv('GOOGLE_API_KEY')
            weatherapi = os.getenv('WEATHER_API_KEY')
            
            if not googleapi or not weatherapi:
                await ctx.send("Weather API keys not configured.")
                return

            async with aiohttp.ClientSession() as session:
                search = search.replace(' ', '+')
                # Get the latitude and longitude
                georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)

                geodata = json.loads(await georesp.text())
                if not geodata.get('results'):
                    await ctx.send('Location not found.')
                    return
                    
                geolat = str(geodata['results'][0]['geometry']['location']['lat'])
                geolon = str(geodata['results'][0]['geometry']['location']['lng'])
                
                # Get the 3-day weather forecast
                forecastresp = await session.get(f'http://api.openweathermap.org/data/2.5/forecast?appid={weatherapi}&lat={geolat}&lon={geolon}&units=imperial')

                forecastdata = json.loads(await forecastresp.text())

                # Create the map URL for the embed
                locmapurl = f'https://maps.googleapis.com/maps/api/staticmap?center={geolat},{geolon}&zoom=11&size=600x300&key={googleapi}'

                # Create forecast embed
                embed = discord.Embed(
                    title=f"3-Day Forecast for {search.replace('+', ' ')}",
                    description="Weather forecast",
                    color=0x00ff00
                )
                
                if 'list' in forecastdata:
                    # Group forecasts by day
                    daily_forecasts = {}
                    for item in forecastdata['list']:
                        date = item['dt_txt'].split(' ')[0]
                        if date not in daily_forecasts:
                            daily_forecasts[date] = []
                        daily_forecasts[date].append(item)
                    
                    # Show forecast for next 3 days
                    for i, (date, forecasts) in enumerate(list(daily_forecasts.items())[:3]):
                        if forecasts:
                            # Get average temperature for the day
                            temps = [f['main']['temp'] for f in forecasts if 'main' in f]
                            avg_temp = sum(temps) / len(temps) if temps else 'N/A'
                            
                            # Get most common weather condition
                            conditions = [f['weather'][0]['description'] for f in forecasts if 'weather' in f and f['weather']]
                            most_common = max(set(conditions), key=conditions.count) if conditions else 'N/A'
                            
                            embed.add_field(
                                name=f"Day {i+1} ({date})",
                                value=f"Temp: {avg_temp:.1f}°F\nConditions: {most_common}",
                                inline=True
                            )
                
                embed.set_image(url=locmapurl)
                await ctx.send(embed=embed)
