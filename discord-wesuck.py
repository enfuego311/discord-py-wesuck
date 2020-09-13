import os
import sys
import discord
import json
import aiohttp
import asyncio
from discord.ext import commands
import random

token = os.environ.get("DISCORD_TOKEN")
tenorapi = os.environ.get("TENOR_API_KEY")
weatherapi = os.environ.get("WEATHER_API_KEY")
googleapi = os.environ.get("GOOGLE_API_KEY")

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def sgif(ctx, *, search):
    confilter = "low"
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()
    search.replace(' ', '+')
    response = await session.get('http://api.tenor.com/v1/search?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
    data = json.loads(await response.text())
    embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])
    
    await session.close()

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def gif(ctx, *, search):
    confilter = "low"
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()
    search.replace(' ', '+')
    response = await session.get('http://api.tenor.com/v1/random?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
    data = json.loads(await response.text())
    embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])

    await session.close()

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def weather(ctx, *, search):
    session = aiohttp.ClientSession()
    search.replace(' ', '+')
    georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)
    geodata = json.loads(await georesp.text())
    geolat = geodata['results'][0]['geometry']['location']['lat']
    geolon = geodata['results'][0]['geometry']['location']['lng']
    await session.close()
    weatheresp = await session.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')
    locmapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + geolat + ',' + geolon + '&zoom=11&size=600x200&key=' + googleapi
    temp = weatheresp['main']['temp']
    city = weatheresp['name']
    country = weatheresp['sys']['country']
    cond = weatheresp['weather'][0]['description']
    feelslike = weatheresp['main']['feels_like']
    humidity = weatheresp['main']['humidity']
    await session.close()
    embed = discord.Embed(title="Weather for" + city + " " + country, colour=discord.Colour.blue())
    embed.set_image(url=locmapurl)
    embed.add_field(name="Current Temp (feelslike)", value=temp + "F" + " " + "(" + feelslike + "F)")
    embed.add_field(name="Conditions", value=cond)
    embed.add_field(name="Humidity", value=humidity + "%")

    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    namestr = "marcus"
    moviestr = "movie night"
    herzogstr = "herzog"

    if namestr.lower() in message.content.lower():
        channel = message.channel
        await channel.send(random_line(os.path.join(sys.path[0], 'name.txt')))

    if moviestr.lower() in message.content.lower():
        channel = message.channel
        await channel.send(random_line(os.path.join(sys.path[0], 'movienight.txt')))

    if herzogstr.lower() in message.content.lower():
        channel = message.channel
        await channel.send(random_line(os.path.join(sys.path[0], 'herzog.txt')))

    await bot.process_commands(message)

bot.run(token)
