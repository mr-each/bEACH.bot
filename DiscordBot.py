import discord
import asyncio
import logging
from discord.utils import get

client = discord.Client()
rainbow_flag = True

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('------')


@client.event
async def on_message(message):

    global rainbow_flag

    if message.author == client.user:
        return

    if message.content.startswith('!makerole'):
        msg = await client.send_message(message.channel, 'Making rainbow role...')
        role_name = 'Rainbow'
        server_name = message.server
        existance_check = discord.utils.get(message.server.roles, name=role_name)
        if existance_check is None:
            raibow_role = await client.create_role(server_name, name=role_name, permissions=discord.Permissions.none())
            await client.move_role(server_name, raibow_role, (len(server_name.roles)-1))
        else:
            msg = await client.send_message(message.channel, 'The role is already existing...')
        msg = await client.send_message(message.channel, 'Done...')


    if message.content.startswith('!rstart'):
        msg = await client.send_message(message.channel, 'RAINBOOMING...')
        sName = message.server
        rName = get(message.server.roles, name='Rainbow')
        cd = 0.1
        a = 0
        if rainbow_flag == False:
            rainbow_flag = True

        #colorlist = [red > purple]
        colorlist = [16711680, 16737536, 16776448, 4718337, 54015, 32255, 6750463, 0x2e3136]
        #colorlist = [0x00FF00, 0x00FF1A, 0x00FF35, 0x00FF50, 0x00FF6B, 0x00FF86, 0x00FFA1, 0x00FFBB, 0x00FFD6, 0x00FFF1, 0x00F1FF, 0x00D6FF, 0x00BBFF, 0x00A1FF, 0x0086FF, 0x006BFF, 0x0050FF, 0x0035FF, 0x001AFF, 0x0000FF, 0x0000FF, 0x1A00FF, 0x3500FF, 0x5000FF, 0x6B00FF, 0x8600FF, 0xA100FF, 0xBB00FF, 0xD600FF, 0xF100FF, 0xFF00F1, 0xFF00D6, 0xFF00BB, 0xFF00A1, 0xFF0086, 0xFF006B, 0xFF0050, 0xFF0035, 0xFF001A, 0xFF0000, 0xFF0000, 0xFF1A00, 0xFF3500, 0xFF5000, 0xFF6B00, 0xFF8600, 0xFFA100, 0xFFBB00, 0xFFD600, 0xFFF100, 0xF1FF00, 0xD6FF00, 0xBBFF00, 0xA1FF00, 0x86FF00, 0x6BFF00, 0x50FF00, 0x35FF00, 0x1AFF00,]

        while rainbow_flag:
            if rainbow_flag == True:
                a = a+1
                print('cycle # '+ str(a) + ': ' + str(rainbow_flag))
                for i in range(len(colorlist)):
                    await client.edit_role(sName, rName, color=discord.Color(colorlist[i]))
                    await asyncio.sleep(cd)
            else:
                return

    if message.content.startswith('!rstop'):
        msg = await client.send_message(message.channel, 'RAINBOOMING ended...')
        rainbow_flag = False
        print('rstop: ' + str(rainbow_flag))

    if message.content.startswith('!rch'):
        msg = await client.send_message(message.channel, '123')
        print('rcheck: ' + str(rainbow_flag) + '-----')

    if message.content.startswith('!cr'):
        if message.content[4:].lower() == '':
            msg = await client.send_message(message.channel, 'wrong name')
        else:
            cr_role = message.content[4:]
            server_name = message.server
            print(cr_role)
            await client.create_role(server_name, name='⭐'+str(cr_role)+'⭐', permissions=discord.Permissions.none(), color=discord.Color(0xddc90d))
            cr_chk = discord.utils.get(message.server.roles, name=cr_role)
            print(cr_chk)
            new_role_name = cr_chk.name
            msg = await client.send_message(message.channel, 'The role "' + new_role_name + '" was created!')

