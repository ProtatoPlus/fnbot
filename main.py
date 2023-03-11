import discord
from discord.ext import commands
from discord import app_commands
import fnutils
import openai
import requests
import pyttsx3
from discord import FFmpegPCMAudio
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix='fn!', intents=intents)
openai.api_key = "openaihere(oldonenotwork)"
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    

@client.event
async def on_ready():
    print("Ready!")

@client.command(brief='Prints out current shop items (no cards)')
async def getshop(ctx):
    shop = fnutils.getcurrentshop()
    response = ""
    for x in shop:
        response = response + x + "\n"
    await ctx.send(response)

@client.command(brief='Prints out daily items (cards)')
async def getdaily(ctx):
    items = fnutils.getdaily()
    for x in items:
        await getskin(ctx, x)

@client.command(pass_context=True, brief='Gets requested skins card')
async def getskin(ctx, arg):
    params1 = {'name': arg}
    req = requests.get("https://fortnite-api.com/v2/cosmetics/br/search/all", params=params1)
    res = req.json()
    if res['status'] != 200:
        await ctx.reply('Either the cosmetic you requested does not exist or there was an error')
        return()
    resp = res['data']
    raritycolor = 0xffffff
    price = ""
    for x in resp:
        typebase = x['type']
        type1 = typebase['value']
        rarity = x['rarity']
        icon = x['images']
        ico = icon['featured']
        lastseen = x['shopHistory']
        isshop = True
        hasprice = False
        if lastseen == None:
            isshop = False
            ico = icon['smallIcon']
        reltime = str(x['added'])
        relun = reltime.rstrip('T00:00:00Z')
        rel = relun.split('T', 1)[0]
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
        if isshop:
            hasprice = True
            if rarity['value'] == 'uncommon':
                if type1 == 'outfit':
                    price = '800'
                elif type1 == 'pickaxe':
                    price = '500'
                elif type1 == 'glider':
                    price = '500'
                elif type1 == 'emote':
                    price = '200'
                elif type1 == 'wrap':
                    price = '300'
            elif rarity['value'] == 'rare':
                if type1 == 'outfit':
                    price = '1,200'
                elif type1 == 'backpack':
                    price == '200'
                elif type1 == 'pickaxe':
                    price = '800'
                elif type1 == 'glider':
                    price = '800'
                elif type1 == 'emote':
                    price = '500'
                elif type1 == 'wrap':
                    price = '600'
            elif rarity['value'] == 'epic':
                if type1 == 'outfit':
                    price = '1,500'
                elif type1 == 'pet':
                    price = '1,000'
                elif type1 == 'pickaxe':
                    price = '1,200/1,500'
                elif type1 == 'glider':
                    price = '1,200'
                elif type1 == 'emote':
                    price = '800'
            elif rarity['value'] == 'legendary':
                if type1 == 'outfit':
                    price = '2,000'
            else:
                price = 'unknown'
        embedVar = discord.Embed(title=x['name'], color=raritycolor)
        embedVar.set_image(url=ico)
        embedVar.add_field(name="Description: ", value=x['description'], inline=False)
        embedVar.add_field(name="Rarity: ", value=rarity['value'].capitalize(), inline=False)
        embedVar.add_field(name="Released: ", value=rel, inline=False)
        embedVar.add_field(name='Type: ', value=type1.capitalize(), inline=False)
        if lastseen != None:
            lstime = str(lastseen[-1])
            ls = lstime.rstrip('T00:00:00Z')
            embedVar.add_field(name="Last Seen: ", value=ls, inline=False)
        else:
            embedVar.add_field(name="Not Available: ", value='Cosmetic is not available for purchase.', inline=False)
        if hasprice:
            embedVar.add_field(name='Price (WIP): ', value=price, inline=False)
        await ctx.channel.send(embed=embedVar)
    
@client.command(brief='Gets an image of the current map')
async def map(ctx):
    req = requests.get('https://fortnite-api.com/v1/map')
    resp = req.json()
    dat = resp['data']
    data = dat['images']
    embedVar = discord.Embed(title='Current Map', color=0x00aaff)
    embedVar.set_image(url=data['pois'])
    await ctx.channel.send(embed=embedVar)

@client.command(pass_context=True)
async def check(ctx):
    id = 1062875057547907142
    r=requests.get("http://skinbot.pythonanywhere.com/check")
    await ctx.reply('Check '+client.get_channel(id).mention)
    print(r.json())

@client.command()
async def join(ctx):
    await ctx.reply('joining...')
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def shopvc(ctx):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")[0]
    engine.setProperty('voice', voices)
    engine.save_to_file(fnutils.getcurrentshop(), 'shop.mp3')
    engine.runAndWait()
    voice = ctx.message.guild.voice_client
    voice.play(FFmpegPCMAudio("shop.mp3"))
    os.remove('shop.mp3')


@client.command()
async def leave(ctx):
    await ctx.reply('leaving...')
    server = ctx.message.guild.voice_client
    await server.disconnect()
    

@client.command(brief='Gets requested players stats')
async def getplayer(ctx, arg):
    headers1 = {'Authorization': 'd2a808a0-61a7-4115-a7b9-09eede5d0811'}
    params1 = {'name': arg}
    reqget = requests.get('https://fortnite-api.com/v2/stats/br/v2', headers=headers1, params=params1)
    req = reqget.json()
    if req['status'] != 200:
        await ctx.reply(req['error'])
        return()
    reqdat = req['data']
    account = reqdat['account']
    bp = reqdat['battlePass']
    stats = reqdat['stats'] 
    allstat = stats['all']
    overall = allstat['overall']
    embedVar = discord.Embed(title=account['name'], color=0x00aaff)
    embedVar.add_field(name='Battle Pass Level: ', value=str(bp['level']), inline=False)
    embedVar.add_field(name='Battle Pass Progress: ', value=str(bp['progress']), inline=False)
    embedVar.add_field(name='Wins: ', value=overall['wins'], inline=False)
    embedVar.add_field(name='Kills: ', value=overall['kills'], inline=False)
    await ctx.channel.send(embed=embedVar)

@client.command(brief='thingy')
async def gpt(ctx, arg):
    max_tokens = 1024
    model_engine = "text-davinci-003"
    prompt = arg
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    await ctx.reply(completion.choices[0].text)

@client.command(brief='thingy2')
async def dalle(ctx, arg):
    response = openai.Image.create(
        prompt=arg,
        n=1,
        size="256x256",
    )
    embedVar = discord.Embed(title=arg, color=0x00aaff)
    embedVar.set_image(url=response["data"][0]["url"])
    await ctx.channel.send(embed=embedVar)



    

client.run('TOKENHERE')
