import discord
from discord.ext import commands
from discord import app_commands
import fnutils
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
    

@client.event
async def on_ready():
    print("Ready!")

@client.command()
async def getshop(ctx):
    shop = fnutils.getcurrentshop()
    response = ""
    for x in shop:
        response = response + x + "\n"
    await ctx.send(response)

@client.command(pass_context=True)
async def getskin(ctx, arg):
    req = requests.get('https://fortnite-api.com/v2/cosmetics/br/'+arg)
    resp = req.json()
    raritycolor = 0xffffff
    respdat = resp['data']
    rarity = respdat['rarity']
    icon = respdat['images']
    if rarity['value'] == 'common':
        raritycolor = 0x6e7073
    elif rarity['value'] == 'uncommon':
        raritycolor = 0x02a104
    elif rarity['value'] == 'rare':
        raritycolor = 0x00aaff
    elif rarity['value'] == 'epic':
        raritycolor = 0x8000ff
    elif rarity['value'] == 'legendary':
        raritycolor == 0xffd500
    else:
        raritycolor == 0xff1100
    txt = ""
    if resp['status'] != 200:
        await ctx.reply('either the id you requested does not exist or there was an error')
    else:
        embedVar = discord.Embed(title=respdat['name'], color=raritycolor)
        embedVar.set_image(url=icon['smallIcon'])
        embedVar.add_field(name="Description: ", value=respdat['description'], inline=False)
        embedVar.add_field(name="Rarity: ", value=rarity['value'], inline=False)
        await ctx.channel.send(embed=embedVar)

    

client.run('')