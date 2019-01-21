import discord
import asyncio
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

#import random
#from discord.ext import commands
#from discord.utils import get

async def newembed(client, user_id, content, color):
    user = await client.get_user_info(user_id)

    newembed = discord.Embed(
        description=content,
        color=color
    )
    newembed.set_author(name=user.name, icon_url=user.avatar_url)
    return newembed

async def clear_last_selfmessage(client, message, channel):
    await asyncio.sleep(2)
    async for msg in client.logs_from(channel, limit=1):
        dellog = msg
    if message.id == dellog.id:
        await client.delete_message(message)
    else:
        return

def clrCHID(channel_id):
    channel_id = channel_id.replace('<', '').replace('#', '').replace('>', '')
    return channel_id

def clrUID(user_id):
    user_id = user_id.replace('<', '').replace('@', '').replace('!', '').replace('>', '')
    return user_id

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
    mgm = Image.open('megu.png', 'r')
    mgm.paste(output, offset, output)
    mgm.save('out.png')

