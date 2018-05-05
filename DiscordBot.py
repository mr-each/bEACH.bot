import discord
import asyncio
import logging
from discord.utils import get

client = discord.Client()

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('------')
#    rainbow_flag = 1

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    """
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        print('hello init')
        print(message.server.id)

    if message.content.startswith('!run'):
        msg = await client.send_message(message.channel, 'Beginning...')
        print('run init')
        server_name = message.server
        print(len(server_name.roles))

    if message.content.startswith('!go'):
        msg = await client.send_message(message.channel, 'Rainbooming...')
        sName = message.server
        print('sName: ')
        print(sName)
        rName = get(message.server.roles, name='RAINBOW')
        rN = rName.name
        rID = rName.id
        rC = rName.color
        print('name: ' + rN)
        print('rID: ' + rID)
        print('rC: ')
        print(rC)
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.red())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.orange())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.gold())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.green())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.teal())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.blue())
        await asyncio.sleep(1)
        await client.edit_role(sName, rName, color = discord.Color.purple())
        print('DONE')
    """


    if message.content.startswith('!makerole'):
        msg = await client.send_message(message.channel, 'Making rainbow role...')
        role_name = 'Rainbow'
        server_name = message.server
        existance_check = discord.utils.get(message.server.roles, name=role_name)
        if existance_check is None:
            raibow_role = await client.create_role(server_name, name=role_name, permissions=discord.Permissions(permissions=0))
            await client.move_role(server_name, raibow_role, (len(server_name.roles)-1))
        else:
            msg = await client.send_message(message.channel, 'The role is already existing...')
        msg = await client.send_message(message.channel, 'Done...')


    if message.content.startswith('!rstart'):
        msg = await client.send_message(message.channel, 'RAINBOOMING...')
        sName = message.server
        rName = get(message.server.roles, name='Rainbow')
        cd = 0.2
        while 1:
            await client.edit_role(sName, rName, color=discord.Color(16711680))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(16737536))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(16776448))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(4718337))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(54015))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(32255))
            await asyncio.sleep(cd)
            await client.edit_role(sName, rName, color=discord.Color(6750463))
            await asyncio.sleep(cd)

    """
    if message.content.startswith('!rstop'):
        msg = await client.send_message(message.channel, 'RAINBOOMING ended...')
        rainbow_flag = 0
    """

"""
role_name = 'RAINBOW'
server = discord.utils.get(client.servers, id = server.id)
current_role = discord.utils.get(client.server.roles, name = role_name)
raibow_role = client.create_role(server, name = role_name)
"""

client.run('MjMwNzIzMzYxMDA3NzMwNjg5.DcUV4g.jRhX-_9G1G42Fds7sOlHjH4rgvQ')