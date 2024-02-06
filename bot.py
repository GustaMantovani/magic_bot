#env imports
import os
from dotenv import load_dotenv

#discord lib imports
import discord
from discord.ext import commands
import logging

#magic lib imports
from mtgsdk import Card 

#Instances

##Discord Lib
###Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='Magic ', intents=intents, help_command = None)

###Channel
channel = discord.channel.TextChannel
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

def gen_magic_api_lang_by_user_input(lang):
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
        'es': 'Spanish',
        'en': None
    }

    return lista_linguagens[lang]

#

#Commands
@bot.command()
async def info(ctx, lang,cardName):
    async with channel.typing(ctx):
        lang = gen_magic_api_lang_by_user_input(lang)
        if lang:
            cards = Card.where(language=lang,name=cardName).all()
        else:
            cards = Card.where(name=cardName).all()

        if cards:
            card_data = cards[0]
            
            mana_cost = card_data.mana_cost
            colors = card_data.color_identity
            rarity = card_data.rarity
            artist = card_data.artist
            power = card_data.power
            toughness = card_data.toughness
            imageURL = card_data.image_url

            if lang:
                for card_in_lang in card_data.foreign_names:
                    if lang == card_in_lang['language']:
                        name = card_in_lang['name']
                        text = card_in_lang['text']
                        type_ = card_in_lang['type']
            else:
                name = card_data.name
                text = card_data.text
                type_ = card_data.type

            embed = discord.Embed(title=name,description=text, color=extract_color_hex(colors[0]))
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
async def tr(ctx, original_lang,cardName,target_lang):
    async with channel.typing(ctx):

        original_lang = gen_magic_api_lang_by_user_input(original_lang)
        target_lang = gen_magic_api_lang_by_user_input(target_lang)

        cards = Card.where(language=original_lang,name=cardName).all()
        if cards:
            names = cards[0].foreign_names

            for name in names:
                if target_lang == name['language']:
                    await ctx.send(name['name'])
    await channel.send('Done!')
#

#Run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(str(disc_api_key), log_handler=handler, log_level=logging.DEBUG)
#