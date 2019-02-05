import discord
import asyncio
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

#import random
#from discord.ext import commands
#from discord.utils import get

localesign = 'RU'

# --------------- File loading ---------------
def load_token():
    f = open('DBtoken.txt')
    token = f.read()
    f.close()
    return token

def load_locale(module_name):
    f = open('locale/DBtext'+localesign+'/'+module_name, encoding='utf-8')
    bot_locale = ['null']
    bot_locale.extend(f.read().splitlines())
    f.close()
    return bot_locale

DBtext = load_locale('Functions')

def load_help_list():
    help_list = {}
    with open('locale/help'+localesign+'.txt', encoding='utf-8') as file:
        for line in file:
            key, value = line.split('+++')
            value = value.replace('\n', '')
            help_list[key] = value
    return help_list

def load_bullying_phrases():
    bullying_phrases = {}
    with open('locale/bullying'+localesign+'.txt', encoding='utf-8') as file:
        for line in file:
            key, value = line.split('+++')
            value = value.replace('\n', '')
            bullying_phrases[key] = value
    return bullying_phrases

# --------------- Ownber chek ---------------

def owner(ctx):
    return ctx.message.author.id == '135140855982981121'

# --------------- Clearing Channel and User IDs ---------------

def clear_channel_ID(channel_id):
    channel_id = channel_id.replace('<', '').replace('#', '').replace('>', '')
    return channel_id

def clear_user_ID(user_id):
    user_id = user_id.replace('<', '').replace('@', '').replace('!', '').replace('>', '')
    return user_id

# --------------- New embed generation ---------------

async def newembed(client, user_id, content, color):
    user = await client.get_user_info(user_id)

    newembed = discord.Embed(
        description=content,
        color=color
    )
    newembed.set_author(name=user.name, icon_url=user.avatar_url)
    return newembed

# --------------- New embed generation for cutiemark ---------------

async def cutiemark(client, message, memberid, text):
    memid = memberid
    member = message.server.get_member(memid)
    if member is None:
        clr = discord.Color.darker_grey()
    else:
        if member.color == discord.Color(0x000000):
            clr = discord.Color.light_grey()
        else:
            clr = member.color
    embed = await newembed(client, user_id=memid, content=text, color = clr)
    return embed

# --------------- Short help generation ---------------

def create_help(client, f1=DBtext[1], f2=DBtext[2], f3=DBtext[3], f4=DBtext[4], f5=DBtext[5], f6=DBtext[6]):
        helplist = load_help_list()
        embed = discord.Embed(
            description = helplist['prefix'],
            color = discord.Color.green()
        )
        embed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
        embed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                            value = f1)
        embed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                            value = f2)
        embed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                            value = f3)
        embed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                            value = f4)
        embed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                            value = f5)
        embed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                            value = f6)
        return embed

# --------------- Deleting bot messages after short delay ---------------

async def clear_last_selfmessage(client, message, channel, seconds=2):
    await asyncio.sleep(seconds)
    async for msg in client.logs_from(channel, limit=1):
        dellog = msg
    if message.id == dellog.id:
        await client.delete_message(message)
    else:
        return

# --------------- Ragequit image ---------------

def megumin_img(url):
    # IMAGE generation
    size = 250, 250
    response = requests.get(url)
    avt = Image.open(BytesIO(response.content))
    avt = avt.resize(size, Image.ANTIALIAS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0)+size, fill = 255)
    output = ImageOps.fit(avt, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    offset = (250, 285)
    mgm = Image.open('img/megu.png', 'r')
    mgm.paste(output, offset, output)
    mgm.save('img/out.png')

# --------------- Database update ---------------

async def update_data(users_list, server, user):
    if not server.id in users_list:
        users_list[server.id] = {}
    if not user.id in users_list[server.id]:
        users_list[server.id][user.id] = {}
        users_list[server.id][user.id]['experience'] = 0
        users_list[server.id][user.id]['level'] = 1
        users_list[server.id][user.id]['vbucks'] = 0

# --------------- Level ---------------

async def add_experience(users_list, server, user, exp):
    users_list[server.id][user.id]['experience'] += exp

async def level_up(client, users_list, server, channel, user):
    experience = users_list[server.id][user.id]['experience']
    lvl_start = users_list[server.id][user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, DBtext[7].format(user.mention, lvl_end))
        users_list[server.id][user.id]['level'] = lvl_end
        users_list[server.id][user.id]['experience'] = 0
        vbucks_coef = (lvl_end//5) + 1
        users_list[server.id][user.id]['vbucks'] += vbucks_coef*5
        
# --------------- V-Bucks ---------------

async def add_vbucks(client, users_list, server, user, vbucks):
    users_list[server.id][user.id]['vbucks'] += vbucks

async def change_vbucks_amount(client, users_list, server, user, vbucks):
    users_list[server.id][user.id]['vbucks'] = vbucks

# --------------- Time ---------------

def secconds_to_time(timer):
    time = {}
    time['hours'] = str(int(timer)//3600)
    time['minutes'] = (int(timer)//60)%60
    time['seconds'] = int(timer)%60
    if time['minutes'] < 10:
        time['minutes'] = '0' + str(time['minutes'])
    else:
        time['minutes'] = str(time['minutes'])
    if time['seconds'] < 10:
        time['seconds'] = '0' + str(time['seconds'])
    else:
        time['seconds'] = str(time['seconds'])
    return time