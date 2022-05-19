import os
import sys
import discord
import re
import json
import aiohttp
import asyncio
from discord.ext import commands
import random
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from aiocfscrape import CloudflareScraper
from spellchecker import SpellChecker

# discord and API tokens need to be environment variables named as below
token = os.environ.get("DISCORD_TOKEN")
tenorapi = os.environ.get("TENOR_API_KEY")
weatherapi = os.environ.get("WEATHER_API_KEY")
googleapi = os.environ.get("GOOGLE_API_KEY")

description = '''To seek and annoy'''

# set command prefix
bot = commands.Bot(command_prefix='.', description=description)

# random line function for word matching
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)



# if we see this the bot is alive
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# check if seed is set
# if not that means word of the day (wotd) isn't set so run the exception code
try: seed
except:
    wordslines = 0
    # open the words file and count the lines
    file = open(os.path.join(sys.path[0], 'words.txt'), "r")
    for line in file:
        line = line.strip("\n")
        wordslines += 1
    file.close()
    # set seed to today's date for consistency
    seed = date.today().isoformat().replace('-', '')
    # set yesterday's seed to to yesterday's date
    ydayseed = (date.today() - timedelta(days=1)).isoformat().replace('-', '')
    # set today's seed and get today's line number
    random.seed(seed)
    wotdlineno = random.randrange(1, wordslines)
    # set yesterday's seed and get yesterday's line number
    random.seed(ydayseed)
    ydwotdlineno = random.randrange(1, wordslines)
    # open the file and get the 2 words
    f=open(os.path.join(sys.path[0], 'words.txt'))
    alllines=f.readlines()
    swotd = str.strip(alllines[int(wotdlineno)])
    sywotd = str.strip(alllines[int(ydwotdlineno)])
    # after wotd and ywotd are defined reset the seed and close the file
    random.seed()
    file.close()

# set reactions to word of the day
async def wotdreact(message):
    wotd_emojis = [
    "👌",
    "😂",
    "🔥",
    "😱"
    ]
    for emoji in wotd_emojis:
        await message.add_reaction(emoji)

# set reactions to nice
async def nicereact(message):
    nice_emoji = "<:69:844757057437302856>"
    await message.add_reaction(nice_emoji)



# function that does what it says - also works for times spanning midnight
async def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# clap!👏
@bot.command(
    pass_context=True,
    help="Put a clap emoji between every word.",
    brief="I will clap for you."
)
async def clap(ctx, *, claptext):
    clapemoji = '👏'
    clapupper = str(claptext).upper().split()
    clapjoin = clapemoji.join(clapupper)
    await ctx.send(str(clapjoin) + clapemoji)

# spongebob text into alternating case SaRcAsM
@bot.command(
    pass_context=True,
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

# why not both?
@bot.command(
    pass_context=True,
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

# top result tenor match command
@bot.command(
    pass_context=True, 
    help="Sends a query to Tenor to get the top match based on your search terms.", 
    brief="Tenor top gif."
)
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


async def cs_page(url):
    async with CloudflareScraper() as session:
        async with session.get(url) as resp:
            return await resp.text()

# inspire me
@bot.command(
    pass_context=True,
    help="Generates an image from inspirobot.",
    brief="Inpsire me."
)
async def inspire(ctx):
    embed = discord.Embed(colour=discord.Colour.blue())
    response = await cs_page('https://inspirobot.me/api?generate=true')
    embed.set_image(url=response)
    await ctx.send(embed=embed)

# random result tenor match command
@bot.command(
    pass_context=True, 
    help="Sends a query to Tenor to get a random match based on your search terms.", 
    brief="Tenor random gif."
)
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

# get today's word
@bot.command(
    pass_context=True,
    help="This will return today's word of the day between 8pm and 12pm eastern.",
    brief="Get today's word."
)
async def wotd(ctx):
    if await is_time_between(time(20, 00), time(23, 59)):
        await ctx.send("The word of the day today was: **" + swotd + "**")
    else:
        await ctx.send("We don't talk about the word of the day until after 8pm eastern.")

# get yesterday's word
@bot.command(
    pass_context=True,
    help="This will return yesterday's word of the day.",
    brief="Get yesterday's word."
)
async def ywotd(ctx):
    await ctx.send("Yesterday's word of the day was: **" + sywotd + "**")

# the WTF command
# gets the last message from mentioned user in the current channel and spell corrects it
@bot.command(
    pass_context="True",
    help="If a user is mentioned using an @, it will get the last msg by them and spellcheck it.",
    brief="Spellcheck a mentioned user's last msg."
)
async def wtf(ctx, user: discord.User):
    # init lastMessage
    lastMessage = None
    # identify what channel this was asked in
    channel = ctx.channel
    # check history for the latest message
    fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)

    # loop to find the newest message by comparing creation times
    if lastMessage is None:
        lastMessage = fetchMessage
    else:
        if fetchMessage.created_at > lastMessage.created_at:
            lastMessage = fetchMessage

    # if a message is found, run the spell check sequence
    if (lastMessage is not None):
        spell = SpellChecker()
        # init the working message as a copy of the actual message
        workmsg = lastMessage.content
        # split the message into words
        msgwords = lastMessage.content.split()
        # spell check every word
        for word in msgwords:
            # sanity check for alpha characters
            word = ''.join(filter(str.isalpha, word))
            # this tests if there is a correction for the word
            test = spell.correction(word)
            # if the word has changed, it has been corrected
            if test != word:
                # replace this word in the working message
                workmsg = workmsg.replace(word, test)
            else: 
                pass
            
        await ctx.send('"' + workmsg + '"')

# weather command
@bot.command(
    pass_context=True, 
    help="This will query the google maps api to get the latitude and longitude. Using that it will query the OpenWeather API for local conditions.", 
    brief="Weather for the location specified."
)
async def weather(ctx, *, search):
    session = aiohttp.ClientSession()
    session2 = aiohttp.ClientSession()
    search.replace(' ', '+')
    # get our latitude and longitude
    georesp = await session.get('https://maps.googleapis.com/maps/api/geocode/json?key=' + googleapi + '&address=' + search, ssl=False)
    geodata = json.loads(await georesp.text())
    geolat = str(geodata['results'][0]['geometry']['location']['lat'])
    geolon = str(geodata['results'][0]['geometry']['location']['lng'])
    # pass the lat and lon to the weather api
    weatheresp = await session2.get('http://api.openweathermap.org/data/2.5/weather?appid=' + weatherapi + '&lat=' + geolat + '&lon=' + geolon + '&units=imperial')
    weatherdata = json.loads(await weatheresp.text())
    # create the map url for the embed
    locmapurl = 'https://maps.googleapis.com/maps/api/staticmap?center=' + \
        geolat + ',' + geolon + '&zoom=11&size=600x300&key=' + googleapi
    temp = str(weatherdata['main']['temp'])
    city = weatherdata['name']
    country = weatherdata['sys']['country']
    cond = weatherdata['weather'][0]['description']
    feelslike = str(weatherdata['main']['feels_like'])
    humidity = str(weatherdata['main']['humidity'])
    # populate the embed with returned values
    embed = discord.Embed(title="Weather for " + city +
                          " " + country, colour=discord.Colour.blue())
    embed.set_image(url=locmapurl)
    embed.add_field(name="Current Temp (Feels Like)",
                    value=temp + "F" + " " + "(" + feelslike + "F)")
    embed.add_field(name="Conditions", value=cond)
    embed.add_field(name="Humidity", value=humidity + "%")
    await session.close()
    await session2.close()
    await ctx.send(embed=embed)

# match various patterns including word of the day and respond with
# either random lines or react to wotd with emoji
@bot.event
async def on_message(message):
#    nicepattern = r".*\bnice\b\W*"
    namestr = "marcus"
    moviestr = "movie night"
    herzogstr = "herzog"
    herstr = "amanda"
    kartstr = "kart game"
    mariostr = "mario game"
    ff2str = "ff2"
    typongstr = "typong"
    ffstr = "final fantasy"
    neatostr = "neato"
    zeldastr = "zelda"
    titwstr = "this is the way"
    bofhpattern = r".*\berror\b\W*"
    # this is the *real* bot username - not the nickname
    botstr = bot.user.name

    # what channel is this? needed for channel.send
    channel = message.channel
    
    # bot ignores botself
    if message.author.id == bot.user.id:
            return

    # reacts to namestr if not botstr
    if (namestr.lower() in message.content.lower()) and (botstr.lower() not in message.content.lower()):
        await channel.send(random_line(os.path.join(sys.path[0], 'name.txt')))
    elif botstr.lower() in message.content.lower():
        line = random_line(os.path.join(sys.path[0], 'botmention.txt'))
        response = line.replace("BOT", botstr)
        await channel.send(response)
    
    # wotd reaction
    if swotd.lower() in message.content.lower():
        await wotdreact(message)

    # nice reaction
    #sequence = message.content.lower()
    #if re.match(nicepattern, sequence):
        #await nicereact(message)

    # bofh regex
    if re.match(bofhpattern, sequence):
        await channel.send(random_line(os.path.join(sys.path[0], 'bofh.txt')))

    # other word matches with static and random line responses below
    if moviestr.lower() in message.content.lower():
        await channel.send(random_line(os.path.join(sys.path[0], 'movienight.txt')))

    if herzogstr.lower() in message.content.lower():
        await channel.send(random_line(os.path.join(sys.path[0], 'herzog.txt')))

    if herstr.lower() in message.content.lower():
        await channel.send("At least until operation: kill wife and kids")

    if kartstr.lower() in message.content.lower():
        await channel.send("**Official We Suck Mario Kart Ranking** - 8 > SNES > 64 > 7 > Wii > GBA > DS > DD")
    
    if mariostr.lower() in message.content.lower():
        await channel.send("**Official We Suck Mario Ranking** - Odyssey > 64 > World 2 > 3 > World > 3D World > Galaxy > 1 > 2 > Galaxy 2 > Sunshine")
    
    if ff2str.lower() in message.content.lower():
        await channel.send("The thing about civilization is that we are all 72 hours away from pure cannibalistic anarchy. That clock gets reset everytime we eat, everytiem we sleep but all of life as know it are on a precipice. FF2 was about 48 hrs for me. Everything you know and care about means nothing. That's the reality of culture and civilzation. It's an absolute cosmic shadow held up by essentially nothing. Final fantasy 2 taught me that.")
    
    if typongstr.lower() in message.content.lower():
       await channel.send("Don't make fun of my typong")
    
    if ffstr.lower() in message.content.lower():
        await channel.send("**Official We Suck Final Fantasy Ranking** - FF6 > FF4 > FF7 > FF9 > FF15 > FF10 > FF12 > FF1 > FF5 > FF8 > FF3 > FF13 > FF2")

    if neatostr.lower() in message.content.lower():
       await channel.send("neato burrito")

    if zeldastr.lower() in message.content.lower():
       await channel.send("**Official We Suck Zelda Ranking** - BotW > LttP > LBW > OoT > WW > LoZ > LA > TP > MM > AoL > SS")
    
    if titwstr.lower() in message.content.lower():
        await channel.send("This is the way.")
        
    # this keeps us from getting stuck in this function
    await bot.process_commands(message)

bot.run(token)
