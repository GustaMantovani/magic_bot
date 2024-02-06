#env imports
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import tempfile

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
    # Dicionário de mapeamento de nomes de cores para inteiros da api do discord
    color_map = {
        "R": 15548997,
        "G": 5763719,
        "U": 3447003,
        "W": 16777215,
        "B": 2303786,
    }

    # Verificando se o nome da cor está no dicionário
    if color_name in color_map:
        return color_map[color_name]
    else:
        return None  # Retorna None se a cor não estiver no dicionário

def gen_magic_api_len_by_user_input(len):
    lista_linguagens = {
        'zh-cn': 'Chinese Simplified',
        'zh-tw': 'Chinese Traditional',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'pt-br': 'Portuguese (Brazil)',
        'ru': 'Russian',
        'es': 'Spanish'
    }

    return lista_linguagens[len]

#

#Commands
@bot.command()
async def info(ctx, len,cardName):
    async with channel.typing(ctx):
        len = gen_magic_api_len_by_user_input(len)
        cards = Card.where(language=len,name=cardName).all()
        if cards:
            card_data = cards[0]
            
            #name = card_data.name
            mana_cost = card_data.mana_cost
            #total_mana_cost = card_data.cmc
            colors = card_data.color_identity
            type_ = card_data.type
            rarity = card_data.rarity
            #text = card_data.text
            artist = card_data.artist
            power = card_data.power
            toughness = card_data.toughness
            imageURL = card_data.image_url
            

            for card_in_lang in card_data.foreign_names:
                if len == card_in_lang['language']:
                    name = card_in_lang['name']
                    text = card_in_lang['text']
                    
            '''r = requests.get(imageURL)
            print(r.content)
            imagem = Image.open(BytesIO(r.content))

            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                # Salvar a imagem no arquivo temporário
                imagem.save(temp_file.name)

            # Obter o caminho do arquivo temporário
            temp_file_path = temp_file.name
            file = discord.File(temp_file_path, filename="image.png")'''

            embed = discord.Embed(title=name,description=text, color=extract_color_hex(colors[0]))
            #embed.set_thumbnail(url="attachment://image.png")
            embed.add_field(name="Type", value=type_, inline=True)
            embed.add_field(name="Mana Cost", value=mana_cost, inline=True)
            embed.add_field(name="Power/Toughness", value=power+"/"+toughness, inline=True)
            embed.add_field(name="Rarity", value=rarity, inline=True)
            embed.add_field(name="Artist", value=artist, inline=False)

            await ctx.send(embed=embed)            
        else:
            await ctx.send('Não foi possível encontrar informações sobre essa carta.')

    await channel.send('Done!')

@bot.command()
async def tr(ctx, original_len,cardName,target_len):
    async with channel.typing(ctx):

        original_len = gen_magic_api_len_by_user_input(original_len)
        target_len = gen_magic_api_len_by_user_input(target_len)

        cards = Card.where(language=original_len,name=cardName).all()
        if cards:
            names = cards[0].foreign_names

            for name in names:
                if target_len == name['language']:
                    await ctx.send(name['name'])
    await channel.send('Done!')
#

#Run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(str(disc_api_key), log_handler=handler, log_level=logging.DEBUG)
#

