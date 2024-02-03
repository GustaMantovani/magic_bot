#env imports
import os
from dotenv import load_dotenv

#discord lib imports
import discord
from discord.ext import commands
import logging

#magic lib imports
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

#Instances

##Discord Lib
###Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command = None)

###Channel
channel = discord.channel.TextChannel

##Magic Lib

#

#Init
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
#

#Run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(str(disc_api_key), log_handler=handler, log_level=logging.DEBUG)
#

