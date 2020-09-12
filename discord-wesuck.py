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
