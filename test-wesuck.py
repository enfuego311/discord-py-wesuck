import os
import sys
import discord
import json
import aiohttp
import asyncio
from discord.ext import commands
import random
from datetime import date

token = os.environ.get("DISCORD_TOKEN")
tenorapi = os.environ.get("TENOR_API_KEY")
weatherapi = os.environ.get("WEATHER_API_KEY")
googleapi = os.environ.get("GOOGLE_API_KEY")

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='.', description=description)


def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

try: seed
except:
    wordslines = 0
    file = open(os.path.join(sys.path[0], 'words.txt'), "r")
    for line in file:
        line = line.strip("\n")
        wordslines += 1
    file.close()
    #seed = date.today().isoformat().replace('-', '')
    seed = 12345
    random.seed(seed)
    wotdlineno = random.randrange(1, wordslines)
    f=open(os.path.join(sys.path[0], 'words.txt'))
    alllines=f.readlines()
    wotd = alllines[int(wotdlineno)]
    file.close()


# @bot.command(pass_context=True)
# async def sgif(ctx, *, search):
#     confilter = "low"
#     embed = discord.Embed(colour=discord.Colour.blue())
#     session = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     response = await session.get('http://api.tenor.com/v1/search?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
#     data = json.loads(await response.text())
#     embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])

#     await session.close()

#     await ctx.send(embed=embed)


# @bot.command(pass_context=True)
# async def gif(ctx, *, search):
#     confilter = "low"
#     embed = discord.Embed(colour=discord.Colour.blue())
#     session = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     response = await session.get('http://api.tenor.com/v1/random?key=' + tenorapi + '&q=' + search + '&contentfilter=' + confilter + '&limit=1&media_filter=minimal')
#     data = json.loads(await response.text())
#     embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])

#     await session.close()

#     await ctx.send(embed=embed)


# @bot.command(pass_context=True)
# async def weather(ctx, *, search):
#     session = aiohttp.ClientSession()
#     session2 = aiohttp.ClientSession()
#     search.replace(' ', '+')
#     georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)
#     geodata = json.loads(await georesp.text())
#     geolat = str(geodata['results'][0]['geometry']['location']['lat'])
#     geolon = str(geodata['results'][0]['geometry']['location']['lng'])
#     weatheresp = await session2.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')
#     weatherdata = json.loads(await weatheresp.text())
#     locmapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + \
#         geolat + ',' + geolon + '&zoom=11&size=600x200&key=' + googleapi
#     temp = str(weatherdata['main']['temp'])
#     city = weatherdata['name']
#     country = weatherdata['sys']['country']
#     cond = weatherdata['weather'][0]['description']
#     feelslike = str(weatherdata['main']['feels_like'])
#     humidity = str(weatherdata['main']['humidity'])
#     embed = discord.Embed(title="Weather for " + city +
#                           " " + country, colour=discord.Colour.blue())
#     embed.set_image(url=locmapurl)
#     embed.add_field(name="Current Temp (Feels Like)",
#                     value=temp + "F" + " " + "(" + feelslike + "F)")
#     embed.add_field(name="Conditions", value=cond)
#     embed.add_field(name="Humidity", value=humidity + "%")
#     await session.close()
#     await session2.close()
#     await ctx.send(embed=embed)

default_emojis = [
    "\N{GRINNING FACE}"
]

async def react(message):
    for emoji in default_emojis:
        await message.add_reaction(emoji)

@bot.event
async def on_message(message):
    
#     namestr = "marcus"
#     moviestr = "movie night"
#     herzogstr = "herzog"
#     herstr = "amanda"
#     kartstr = "kart"
#     mariostr = "mario"
#     ff2str = "ff2"
#     coolstr = "cool"
#     typongstr = "typong"
#     ffstr = "final fantasy"
#     neatostr = "neato"
#     zeldastr = "zelda"
    tellstr = "tellme"
    # if message.author.id == bot.user.id:
    #     return

    if wotd in message.content.lower():
        await react(message)
        
    if tellstr in message.content.lower():
        channel = message.channel
        await channel.send(wotd)
        await react(message)

#     if herzogstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send(random_line(os.path.join(sys.path[0], 'herzog.txt')))
    
#     if herstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("At least until operation: kill wife and kids")

#     if kartstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Mario Kart Ranking** - 8 > SNES > 64 > 7 > Wii > GBA > DS > DD")
    
#     if mariostr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Mario Ranking** - Odyssey > 64 > World 2 > 3 > World > 3D World > Galaxy > 1 > 2 > Galaxy 2 > Sunshine")
    
#     if ff2str.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("The thing about civilization is that we are all 72 hours away from pure cannibalistic anarchy. That clock gets reset everytime we eat, everytiem we sleep but all of life as know it are on a precipice. FF2 was about 48 hrs for me. Everything you know and care about means nothing. That's the reality of culture and civilzation. It's an absolute cosmic shadow held up by essentially nothing. Final fantasy 2 taught me that.")
    
#     if coolstr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("cool cool cool")
    
#     if typongstr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("Don't make fun of my typong")
    
#     if ffstr.lower() in message.content.lower():
#         channel = message.channel
#         await channel.send("**Official We Suck Final Fantasy Ranking** - FF6 > FF4 > FF7 > FF9 > FF15 > FF10 > FF12 > FF1 > FF5 > FF8 > FF3 > FF13 > FF2")

#     if neatostr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("neato burrito")

#     if zeldastr.lower() in message.content.lower():
#        channel = message.channel
#        await channel.send("**Official We Suck Zelda Ranking** - BotW > LttP > LBW > OoT > WW > LoZ > LA > TP > MM > AoL > SS")

    await bot.process_commands(message)

bot.run(token)
