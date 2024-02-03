#env imports
import os
from dotenv import load_dotenv
import requests
import io

#discord lib imports
import discord
from discord.ext import commands
import logging

#magic lib imports
from mtgsdk import Card, card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
from mtgsdk.restclient import json

#Instances

##Discord Lib
###Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='Magic ', intents=intents, help_command = None)

###Channel
channel = discord.channel.TextChannel

##Magic Lib

#

#Init
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
#

#Functions

def extract_color_hex(color_name):
    color_name = color_name.lower()
    # Dicionário de mapeamento de nomes de cores para códigos hexadecimais
    color_map = {
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "white": "#FFFFFF",
        "black": "#000000",
    }

    # Convertendo o nome da cor para minúsculas para corresponder ao dicionário
    color_name_lower = color_name.lower()

    # Verificando se o nome da cor está no dicionário
    if color_name_lower in color_map:
        return color_map[color_name_lower]
    else:
        return None  # Retorna None se a cor não estiver no dicionário
#

#Commands
@bot.command()
async def info(ctx, cardName):
    async with channel.typing(ctx):
        cards = Card.where(name=cardName).all()
        if cards:
            card_data = cards[0]
            
            name = card_data.name
            mana_cost = card_data.mana_cost
            #total_mana_cost = card_data.cmc
            colors = card_data.colors
            type_ = card_data.type
            rarity = card_data.rarity
            set_ = card_data.set
            text = card_data.text
            artist = card_data.artist
            power = card_data.power
            toughness = card_data.toughness
            imageURL = card_data.image_url
            
            response = requests.get(imageURL)

            embed = discord.Embed(title=name,description=text, color=extract_color_hex(colors[0]))

            embed.set_thumbnail(url="")
            embed.add_field(name="Artist", value=artist, inline=False)
            
            embed.add_field(name="Type", value=type_, inline=True)
            embed.add_field(name="Mana Cost", value=mana_cost, inline=True)
            embed.add_field(name="Power", value=power, inline=True)
            embed.add_field(name="Toughness", value=toughness, inline=True)
            embed.add_field(name="Rarity", value=rarity, inline=True)
            embed.add_field(name="Set", value=set_, inline=True)

            await ctx.send(embed=embed)            
        else:
            await ctx.send('Não foi possível encontrar informações sobre essa carta.')

    await channel.send('Done!')
#

#Run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(str(disc_api_key), log_handler=handler, log_level=logging.DEBUG)
#

