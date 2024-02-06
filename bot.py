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
        "B": 2303786
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
            # Mensagens de erro em diferentes idiomas
            if lang == 'Chinese Simplified':
                await ctx.send("找不到有关此卡的信息。")  # Mensagem em Chinês Simplificado
            elif lang == 'Chinese Traditional':
                await ctx.send("找不到有關此卡的信息。")  # Mensagem em Chinês Tradicional
            elif lang == 'French':
                await ctx.send("Impossible de trouver des informations sur cette carte.")  # Mensagem em Francês
            elif lang == 'German':
                await ctx.send("Konnte keine Informationen zu dieser Karte finden.")  # Mensagem em Alemão
            elif lang == 'Italian':
                await ctx.send("Impossibile trovare informazioni su questa carta.")  # Mensagem em Italiano
            elif lang == 'Japanese':
                await ctx.send("このカードに関する情報が見つかりませんでした。")  # Mensagem em Japonês
            elif lang == 'Korean':
                await ctx.send("이 카드에 대한 정보를 찾을 수 없습니다.")  # Mensagem em Coreano
            elif lang == 'Portuguese (Brazil)':
                await ctx.send("Não foi possível encontrar informações sobre essa carta.")  # Mensagem em Português (Brasil)
            elif lang == 'Russian':
                await ctx.send("Не удалось найти информацию об этой карте.")  # Mensagem em Russo
            elif lang == 'Spanish':
                await ctx.send("No se pudo encontrar información sobre esta carta.")  # Mensagem em Espanhol
            else:
                await ctx.send("Could not find information about this card.")  # Mensagem padrão em inglês

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
                    return
        else:
            # Mensagens de erro em diferentes idiomas
            if original_lang == 'Chinese Simplified':
                await ctx.send("找不到有关此卡的信息。")  # Mensagem em Chinês Simplificado
            elif original_lang == 'Chinese Traditional':
                await ctx.send("找不到有關此卡的信息。")  # Mensagem em Chinês Tradicional
            elif original_lang == 'French':
                await ctx.send("Impossible de trouver des informations sur cette carte.")  # Mensagem em Francês
            elif original_lang == 'German':
                await ctx.send("Konnte keine Informationen zu dieser Karte finden.")  # Mensagem em Alemão
            elif original_lang == 'Italian':
                await ctx.send("Impossibile trovare informazioni su questa carta.")  # Mensagem em Italiano
            elif original_lang == 'Japanese':
                await ctx.send("このカードに関する情報が見つかりませんでした。")  # Mensagem em Japonês
            elif original_lang == 'Korean':
                await ctx.send("이 카드에 대한 정보를 찾을 수 없습니다.")  # Mensagem em Coreano
            elif original_lang == 'Portuguese (Brazil)':
                await ctx.send("Não foi possível encontrar informações sobre essa carta.")  # Mensagem em Português (Brasil)
            elif original_lang == 'Russian':
                await ctx.send("Не удалось найти информацию об этой карте.")  # Mensagem em Russo
            elif original_lang == 'Spanish':
                await ctx.send("No se pudo encontrar información sobre esta carta.")  # Mensagem em Espanhol
            else:
                await ctx.send("Could not find information about this card.")  # Mensagem padrão em inglês
    await channel.send('Done!')
#
    
#Help
@bot.command()
async def help(ctx):
    await ctx.send("Welcome to the MTG Information Bot!\n\n"
                   "Use the following commands to interact with me:\n"
                   "`Magic info [lang] [cardName]`: Get information about MTG cards.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Translate MTG card names into other languages.\n"
                   "`Magic help [lang]`: Get help information.")

@bot.command()
async def ajuda(ctx):
    await ctx.send("Bem-vindo ao Bot de Informações sobre MTG!\n\n"
                   "Use os seguintes comandos para interagir comigo:\n"
                   "`Magic info [lang] [cardName]`: Obtenha informações sobre cartas MTG.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Traduza nomes de cartas MTG para outros idiomas.\n"
                   "`Magic ajuda [lang]`: Obtenha informações de ajuda.")

@bot.command()
async def ayuda(ctx):
    await ctx.send("¡Bienvenido al Bot de Información de MTG!\n\n"
                   "Utilice los siguientes comandos para interactuar conmigo:\n"
                   "`Magic info [lang] [cardName]`: Obtenga información sobre las cartas de MTG.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Traduzca nombres de cartas de MTG a otros idiomas.\n"
                   "`Magic ayuda [lang]`: Obtenga información de ayuda.")

@bot.command()
async def hilfe(ctx):
    await ctx.send("Willkommen beim MTG Information Bot!\n\n"
                   "Verwenden Sie die folgenden Befehle, um mit mir zu interagieren:\n"
                   "`Magic info [lang] [cardName]`: Informationen über MTG-Karten abrufen.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Übersetzen Sie MTG-Kartennamen in andere Sprachen.\n"
                   "`Magic hilfe [lang]`: Hilfeinformationen erhalten.")
@bot.command()
async def 帮助(ctx):
    await ctx.send("欢迎使用 MTG 信息查询机器人！\n\n"
                   "使用以下命令来与我互动：\n"
                   "`Magic info [lang] [cardName]`: 获取关于 MTG 卡片的信息。\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: 将 MTG 卡片名称翻译成其他语言。\n"
                   "`Magic 帮助 [lang]`: 获取帮助信息。")

@bot.command()
async def ヘルプ(ctx):
    await ctx.send("MTG 情報ボットへようこそ！\n\n"
                   "以下のコマンドを使用して私と対話してください：\n"
                   "`Magic info [lang] [cardName]`: MTG カードの情報を取得します。\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: MTG カード名を他の言語に翻訳します。\n"
                   "`Magic ヘルプ [lang]`: ヘルプ情報を取得します。")

@bot.command()
async def 도움말(ctx):
    await ctx.send("MTG 정보 봇에 오신 것을 환영합니다!\n\n"
                   "다음 명령을 사용하여 저와 상호 작용할 수 있습니다:\n"
                   "`Magic info [lang] [cardName]`: MTG 카드 정보를 가져옵니다.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: MTG 카드 이름을 다른 언어로 번역합니다.\n"
                   "`Magic 도움말 [lang]`: 도움말 정보를 얻습니다.")

@bot.command()
async def aiuto(ctx):
    await ctx.send("Benvenuto nel Bot di Informazioni su MTG!\n\n"
                   "Utilizza i seguenti comandi per interagire con me:\n"
                   "`Magic info [lang] [cardName]`: Ottieni informazioni sulle carte MTG.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Traduci nomi di carte MTG in altre lingue.\n"
                   "`Magic aiuto [lang]`: Ottieni informazioni di aiuto.")

@bot.command()
async def помощь(ctx):
    await ctx.send("Добро пожаловать в Бот Информации о MTG!\n\n"
                   "Используйте следующие команды для взаимодействия со мной:\n"
                   "`Magic info [lang] [cardName]`: Получить информацию о картах MTG.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Перевести названия карт MTG на другие языки.\n"
                   "`Magic помощь [lang]`: Получить информацию о помощи.")
@bot.command()
async def 도움말(ctx):
    await ctx.send("MTG 정보 봇에 오신 것을 환영합니다!\n\n"
                   "다음 명령을 사용하여 저와 상호 작용할 수 있습니다:\n"
                   "`Magic info [lang] [cardName]`: MTG 카드 정보를 가져옵니다.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: MTG 카드 이름을 다른 언어로 번역합니다.\n"
                   "`Magic 도움말 [lang]`: 도움말 정보를 얻습니다.")

@bot.command()
async def aide(ctx):
    await ctx.send("Bienvenue sur le Bot d'Information MTG !\n\n"
                   "Utilisez les commandes suivantes pour interagir avec moi :\n"
                   "`Magic info [lang] [cardName]`: Obtenez des informations sur les cartes MTG.\n"
                   "`Magic tr [original_lang] [cardName] [target_lang]`: Traduisez les noms de cartes MTG dans d'autres langues.\n"
                   "`Magic aide [lang]`: Obtenez des informations d'aide.")
#

#Run 
load_dotenv()
disc_api_key = os.getenv('DISCORD_API_KEY')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(str(disc_api_key), log_handler=handler, log_level=logging.DEBUG)
#