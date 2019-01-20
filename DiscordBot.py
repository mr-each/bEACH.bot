import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

localesign = 'RU'

# Reading TOKEN from file
f = open('DBtoken.txt')
DBtoken = f.read()
f.close()
f = open('linklist.txt', encoding='utf-8')
linklist = f.read().splitlines()
f.close()
# Getting locale text for replies
f = open('locale/DBtext'+localesign+'.txt', encoding='utf-8')
DBtext = f.read().splitlines()
f.close()
# Getting help command content
helplist = {}
with open('locale/help'+localesign+'.txt', encoding='utf-8') as file:
    for line in file:
        key, value = line.split('+++')
        value = value.replace('\n', '')
        helplist[key] = value

# constants
rainbow_flag = True
rrole = 'RAINBOW'

client = commands.Bot(command_prefix = 'sr.')  # Command prefix
client.remove_command('help')  # Removing default HELP command

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='sr.help'))  # Giving custom status
    print('Connected!')
    print('Username: ' + client.user.name + 'ID: ' + client.user.id)
    print('------')

# --------------- Help command ---------------

@client.command(pass_context=True)
async def help(ctx):
    await client.delete_message(ctx.message)
    helpembed = discord.Embed(
        title = helplist['title'],
        description = helplist['prefix'],
        color = discord.Color.green()
    )

    helpembed.set_thumbnail(url=client.user.avatar_url)
    helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                        value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>'])

    helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                        value=helplist['ut-bly'] + '\n' + helplist['ut-ab'] + '\n' + helplist['ut-ggl'] + '\n' +
                              helplist['ut-rq'] + '\n' + helplist['ut-mgm'])

    helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                        value = helplist['cm-nb'] + '\n' + helplist['cm-tt'])

    helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                        value = helplist['rlc-ca'])

    helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                        value = helplist['rc-mkr'] + '\n' + helplist['rc-gvr'] + '\n' +
                                helplist['rc-stt'] + '\n' + helplist['rc-stp'])

    await client.say(embed=helpembed)

# --------------- Command for clearing chat ---------------

@client.command(pass_context=True, aliases=['clr'])
async def clear(ctx, amount='1'):
    await client.delete_message(ctx.message)
    try:
        int(amount)
    except ValueError:
        msg = await client.say(DBtext[1])
        await clear_last_selfmessage(msg, msg.channel)
        return
    amount = int(amount)
    if ctx.message.author.server_permissions.manage_messages is True:
        if 0 < amount < 100:
            channel = ctx.message.channel
            messages = []
            async for message in client.logs_from(channel, limit=int(amount)):
                messages.append(message)
            try:
                await client.delete_messages(messages)
            except discord.HTTPException:
                msg = await client.say(DBtext[20])
                await clear_last_selfmessage(msg, msg.channel)
                return
            msg = await client.say('**' + str(amount) + DBtext[2])
            await clear_last_selfmessage(msg, msg.channel)
        else:
            msg = await client.say(DBtext[3])
            await clear_last_selfmessage(msg, msg.channel)
    else:
        msg = await client.say(DBtext[4])
        await clear_last_selfmessage(msg, msg.channel)

# --------------- Command for creating an achievement role ---------------

@client.command(pass_context=True)
async def crach(ctx):
    await client.delete_message(ctx.message)
    if ctx.message.author.server_permissions.manage_roles is True:
        if ctx.message.content[9:] == '':
            msg = await client.say(DBtext[5])
            await clear_last_selfmessage(msg, msg.channel)
        else:
            cr_role = ctx.message.content[9:]
            server_name = ctx.message.server
            await client.create_role(server_name, name='⭐' + str(cr_role) + '⭐', permissions=discord.Permissions.none(), color=discord.Color(0xddc90d))
            discord.utils.get(ctx.message.server.roles, name=cr_role)
            new_role_name = cr_role
            await client.say(DBtext[6] + new_role_name + DBtext[7])
    else:
        msg = await client.say(DBtext[8])
        await clear_last_selfmessage(msg, msg.channel)

# --------------- Command for quoting messages ---------------

@client.command(pass_context=True, aliases=['qt','move','mv'])
async def quote(ctx):
    await client.delete_message(ctx.message)
    if len(ctx.message.content) > 44:
        cmd, chnlID, msgID = ctx.message.content.split()  # Getting channel and message ID of source message
        chnlID = clrCHID(chnlID)  # Clearing channel ID from mention
        chnl_from = client.get_channel(chnlID)
        if chnl_from is None:
            msg = await client.say(DBtext[22])
            await clear_last_selfmessage(msg, msg.channel)
            return
        try:
            msg = await client.get_message(chnl_from, msgID)
        except discord.NotFound:
            msg = await client.say(DBtext[23])
            await clear_last_selfmessage(msg, msg.channel)
            return
        mvembed = discord.Embed(
            description = msg.content,
            timestamp = msg.timestamp,
            color = discord.Color.blue()
        )
        mvembed.set_footer(text='#'+chnl_from.name)
        mvembed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
        # Getting attachment url if exist
        if msg.attachments != []:
            attch = msg.attachments.pop().get('url')
            mvembed.set_image(url=attch)

        await client.say(embed=mvembed)
    else:
        msg = await client.say(DBtext[21])
        await clear_last_selfmessage(msg, msg.channel)

# --------------- Command for bullying someone ---------------

@client.command(pass_context=True, aliases=['bly','bul'])
async def bully(ctx, targetID=''):
    await client.delete_message(ctx.message)

    #cmd, cnt = ctx.message.content.split(' ', 1)

    # Getting phrases for bullying
    f = open('locale/bullying' + localesign + '.txt', encoding='utf-8')
    bullying = f.read().splitlines()
    f.close()

    if targetID == '':
        msg = await client.say(DBtext[9])
        await clear_last_selfmessage(msg, msg.channel)
    else:
        bullyembed = discord.Embed(
            description = random.choice(bullying),
            color = discord.Color.red()
        )
        bullyembed.set_thumbnail(url=linklist[1])
        bullyembed.set_footer(text = DBtext[10])

        await client.say(DBtext[11] + targetID + '!', embed=bullyembed)

# --------------- Command for adding new bullying line ---------------

@client.command(pass_context=True)
async def addbull(ctx):
    if ctx.message.content[11:] == '':
        msg = await client.say(DBtext[12])
        await clear_last_selfmessage(msg, msg.channel)
    else:
        f = open('lacale/bullying' + localesign + '.txt', 'a', encoding='utf-8')
        f.write('\n'+ctx.message.content[11:])
        f.close()
        await client.say(DBtext[24])

# --------------- Neboyan mark ---------------

@client.command(pass_context=True, aliases=['nebayan','nebajan','nebojan','nb'])
async def neboyan(ctx):
    await client.delete_message(ctx.message)
    memid = '144055353934348288'
    member = ctx.message.server.get_member(memid)
    if member is None:
        clr = discord.Color.darker_grey()
    else:
        if member.color == discord.Color(0x000000):
            clr = discord.Color.light_grey()
        else:
            clr = member.color
    embed = await newembed(user_id=memid, content=DBtext[19], color=clr)
    await client.say(embed=embed)

# --------------- RageQuitting command  ---------------

@client.command(pass_context=True, aliases=['rq'])
async def ragequit(ctx):
    await client.delete_message(ctx.message)
    megumin_img(ctx.message.author.avatar_url)
    rqch = await client.create_channel(ctx.message.server, 'rq', type=discord.ChannelType.voice)
    await client.move_member(ctx.message.author, rqch)
    await client.delete_channel(rqch)
    await client.send_file(ctx.message.channel, 'out.png', content=DBtext[25] + ctx.message.author.mention + '!')

# --------------- Command for getting personal Megumin image  ---------------

@client.command(pass_context=True, aliases=['mgm'])
async def megumin(ctx, targetID=''):
    await client.delete_message(ctx.message)
    if targetID == '':
        target = ctx.message.author
    else:
        targetID = clrUID(targetID)
        try:
            target = await client.get_user_info(targetID)
        except discord.NotFound:
            msg = await client.say(DBtext[27])
            await clear_last_selfmessage(msg, msg.channel)
            return
    megumin_img(target.avatar_url)
    await client.send_file(ctx.message.author, 'out.png', content=DBtext[25] + target.name + '!')


@client.command(pass_context=True, aliases=['ggl'])
async def google(ctx):
    await client.delete_message(ctx.message)
    cmd, cnt = ctx.message.content.split(' ', 1)
    if len(cnt) < 22:
        msg = await client.say(DBtext[36])
        await clear_last_selfmessage(msg, msg.channel)
    else:
        targetID, search = cnt.split(' ', 1)
        try:
            await client.get_user_info(clrUID(targetID))
        except discord.NotFound:
            msg = await client.say(DBtext[27])
            await clear_last_selfmessage(msg, msg.channel)
            return
        if search == '':
            msg = await client.say(DBtext[31])
            await clear_last_selfmessage(msg, msg.channel)
            return
        else:
            gglembed = discord.Embed(
                description='**' + ctx.message.author.name + '**' + DBtext[32] + '\n' + DBtext[33] + '\n' + DBtext[34] + search.replace(' ', '+') + DBtext[35],
                color=discord.Color.teal()
            )
            gglembed.set_thumbnail(url=linklist[2])
            await client.say(DBtext[11] + targetID + '!', embed=gglembed)

@client.command(pass_context=True, aliases=['tt'])
async def titupoy(ctx):
    await client.delete_message(ctx.message)
    memid = '135140855982981121'
    member = ctx.message.server.get_member(memid)
    if member is None:
        clr = discord.Color.darker_grey()
    else:
        if member.color == discord.Color(0x000000):
            clr = discord.Color.light_grey()
        else:
            clr = member.color
    embed = await newembed(user_id=memid, content=DBtext[37], color=clr)
    await client.say(embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>>'):
        await client.delete_message(message)
        if message.author.color == discord.Color(0x000000):
            clr = discord.Color.light_grey()
        else:
            clr = message.author.color
        embed = await newembed(user_id=message.author.id, content=message.content[2:], color=clr)
        await client.send_message(message.channel, embed=embed)
    await client.process_commands(message)


# ------------------------------ Functions ------------------------------


async def newembed(user_id, content, color):
    user = await client.get_user_info(user_id)

    newembed = discord.Embed(
        description=content,
        color=color
    )
    newembed.set_author(name=user.name, icon_url=user.avatar_url)
    return newembed

async def clear_last_selfmessage(message,channel):
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


########################################################################################################################
# ------------------------------ RAINBOW SECTION  ------------------------------
# --------------- Command for making RAINBOW role  ---------------

@client.command(pass_context=True, aliases=['r_mkrl'])
async def r_makerole(ctx):
    await client.delete_message(ctx.message)
    if ctx.message.author.server_permissions.manage_roles is True:
        existence_check = discord.utils.get(ctx.message.server.roles, name=rrole)
        rolepos = discord.utils.get(ctx.message.server.roles, name=client.user.name).position
        if existence_check is None:
            rainbow_role = await client.create_role(ctx.message.server, name=rrole, permissions=discord.Permissions.none())
            await client.move_role(ctx.message.server, rainbow_role, rolepos)
            await client.say(DBtext[14])
        else:
            msg = await client.say(DBtext[13])
            await clear_last_selfmessage(msg, msg.channel)
    else:
        await client.sat(DBtext[0])

# --------------- Command for giving RAINBOW role  ---------------

@client.command(pass_context=True, aliases=['r_gvrl'])
async def r_giverole(ctx, targetID=''):
    await client.delete_message(ctx.message)
    if ctx.message.author.server_permissions.manage_roles is True:
        if targetID == '':
            member = ctx.message.author
        else:
            user = await client.get_user_info(clrUID(targetID))
            member = discord.utils.find(lambda m: m.name == user.name, ctx.message.server.members)
        await client.add_roles(member, discord.utils.get(ctx.message.server.roles, name=rrole))
    else:
        await client.sat(DBtext[0])

# --------------- Command to start RAINBOOMING  ---------------

@client.command(pass_context=True)
async def r_start(ctx):
    await client.delete_message(ctx.message)
    if ctx.message.author.server_permissions.ban_members is True:
        await client.say(DBtext[29])
        msg = await client.wait_for_message(timeout=5,author=ctx.message.author)
        if msg is not None:
            if msg.content == 'Yes' or msg.content == 'Y' or msg.content == 'yes' or msg.content == 'y':
                await client.say(ctx.message.author.mention + DBtext[15])
                sName = ctx.message.server
                rName = get(ctx.message.server.roles, name=rrole)
                cd = 0.1
                a = 0
                global rainbow_flag
                if rainbow_flag is False:
                    rainbow_flag = True

                # colorlist = [red > purple]
                colorlist1 = [16711680, 16737536, 16776448, 4718337, 54015, 32255, 6750463, 0x2e3136]
                colorlist2 = [0x00FF00, 0x00FF1A, 0x00FF35, 0x00FF50, 0x00FF6B, 0x00FF86, 0x00FFA1, 0x00FFBB, 0x00FFD6,
                              0x00FFF1, 0x00F1FF, 0x00D6FF, 0x00BBFF, 0x00A1FF, 0x0086FF, 0x006BFF, 0x0050FF, 0x0035FF,
                              0x001AFF, 0x0000FF, 0x0000FF, 0x1A00FF, 0x3500FF, 0x5000FF, 0x6B00FF, 0x8600FF, 0xA100FF,
                              0xBB00FF, 0xD600FF, 0xF100FF, 0xFF00F1, 0xFF00D6, 0xFF00BB, 0xFF00A1, 0xFF0086, 0xFF006B,
                              0xFF0050, 0xFF0035, 0xFF001A, 0xFF0000, 0xFF0000, 0xFF1A00, 0xFF3500, 0xFF5000, 0xFF6B00,
                              0xFF8600, 0xFFA100, 0xFFBB00, 0xFFD600, 0xFFF100, 0xF1FF00, 0xD6FF00, 0xBBFF00, 0xA1FF00,
                              0x86FF00, 0x6BFF00, 0x50FF00, 0x35FF00, 0x1AFF00, ]

                while rainbow_flag:
                    if rainbow_flag is True:
                        a = a + 1
                        for i in range(len(colorlist1)):
                            await client.edit_role(sName, rName, color=discord.Color(colorlist1[i]))
                            await asyncio.sleep(cd)
                    else:
                        return
            else:
                msg = await client.say(DBtext[30])
                await clear_last_selfmessage(msg, msg.channel)
        else:
            msg = await client.say(DBtext[28])
            await clear_last_selfmessage(msg, msg.channel)
    else:
        msg = await client.say(DBtext[18])
        await clear_last_selfmessage(msg, msg.channel)

# --------------- Command to stop RAINBOOMING  ---------------

@client.command(pass_context=True, aliases=['stop'])
async def r_stop(ctx):
    await client.delete_message(ctx.message)
    global rainbow_flag
    rainbow_flag = False
    await client.say(DBtext[16])

########################################################################################################################

client.run(DBtoken)