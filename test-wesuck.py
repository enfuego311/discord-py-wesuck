import os
import sys
import discord
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

# cloudflare scraper function
async def cs_page(url):
    async with CloudflareScraper() as session:
        async with session.get(url) as resp:
            return await resp.text()

# function that does what it says - also works for times spanning midnight
async def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

@bot.event
async def on_message(message):
    if message.author.id != 340495492377083905:
            return

   # s = ''.join(filter(str.isalnum, s))

    spell = SpellChecker()
    msgwords = message.content.split()
    channel = message.channel
    for word in msgwords:
        word = ''.join(filter(str.isalpha, word))
        test = spell.correction(word)
        if test != word:
            await channel.send(word + " is misspelled. i think it is spelled " + test)

    await bot.process_commands(message)

bot.run(token)
