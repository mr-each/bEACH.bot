import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'/RainbowCommands', encoding='utf-8')
DBtext = ['null']
DBtext.extend(f.read().splitlines())
f.close()

rainbow_flag = True
rrole = 'RAINBOW'


class RainbowCommands:
    def __init__(self, client):
        self.client = client

    # --------------- Command for making RAINBOW role  ---------------

    @commands.command(pass_context=True, aliases=['r_mkrl'])
    async def r_makerole(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if ctx.message.author.server_permissions.manage_roles is True:
            existence_check = discord.utils.get(ctx.message.server.roles, name=rrole)
            rolepos = discord.utils.get(ctx.message.server.roles, name=self.client.user.name).position
            if existence_check is None:
                rainbow_role = await self.client.create_role(ctx.message.server, name=rrole, permissions=discord.Permissions.none())
                await self.client.move_role(ctx.message.server, rainbow_role, rolepos)
                await self.client.say(DBtext[1])
            else:
                msg = await self.client.say(DBtext[2])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            await self.client.sat(DBtext[3])

    # --------------- Command for giving RAINBOW role  ---------------

    @commands.command(pass_context=True, aliases=['r_gvrl'])
    async def r_giverole(self, ctx, targetID=''):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if ctx.message.author.server_permissions.manage_roles is True:
            if targetID == '':
                member = ctx.message.author
            else:
                user = await self.client.get_user_info(bot.clear_user_ID(targetID))
                member = discord.utils.find(lambda m: m.name == user.name, ctx.message.server.members)
            await self.client.add_roles(member, discord.utils.get(ctx.message.server.roles, name=rrole))
        else:
            await self.client.sat(DBtext[3])

    # --------------- Command to start RAINBOOMING  ---------------

    @commands.command(pass_context=True)
    async def r_start(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if ctx.message.author.server_permissions.ban_members is True:
            await self.client.say(DBtext[4])
            msg = await self.client.wait_for_message(timeout=5, author=ctx.message.author)
            if msg is not None:
                if msg.content == 'Yes' or msg.content == 'Y' or msg.content == 'yes' or msg.content == 'y':
                    await self.client.say(DBtext[5].format(ctx.message.author.mention))
                    sName = ctx.message.server
                    rName = get(ctx.message.server.roles, name=rrole)
                    cd = 0.1
                    a = 0
                    global rainbow_flag
                    if rainbow_flag is False:
                        rainbow_flag = True

                    # colorlist = [red > purple]
                    colorlist = [16711680, 16737536, 16776448, 4718337, 54015, 32255, 6750463, 0x2e3136]
                    '''
                    colorlist2 = [0x00FF00, 0x00FF1A, 0x00FF35, 0x00FF50, 0x00FF6B, 0x00FF86, 0x00FFA1, 0x00FFBB, 0x00FFD6,
                                  0x00FFF1, 0x00F1FF, 0x00D6FF, 0x00BBFF, 0x00A1FF, 0x0086FF, 0x006BFF, 0x0050FF, 0x0035FF,
                                  0x001AFF, 0x0000FF, 0x0000FF, 0x1A00FF, 0x3500FF, 0x5000FF, 0x6B00FF, 0x8600FF, 0xA100FF,
                                  0xBB00FF, 0xD600FF, 0xF100FF, 0xFF00F1, 0xFF00D6, 0xFF00BB, 0xFF00A1, 0xFF0086, 0xFF006B,
                                  0xFF0050, 0xFF0035, 0xFF001A, 0xFF0000, 0xFF0000, 0xFF1A00, 0xFF3500, 0xFF5000, 0xFF6B00,
                                  0xFF8600, 0xFFA100, 0xFFBB00, 0xFFD600, 0xFFF100, 0xF1FF00, 0xD6FF00, 0xBBFF00, 0xA1FF00,
                                  0x86FF00, 0x6BFF00, 0x50FF00, 0x35FF00, 0x1AFF00, ]
                    '''
                    while rainbow_flag:
                        if rainbow_flag is True:
                            a = a + 1
                            for i in range(len(colorlist)):
                                await self.client.edit_role(sName, rName, color=discord.Color(colorlist[i]))
                                await asyncio.sleep(cd)
                        else:
                            return
                else:
                    msg = await self.client.say(DBtext[6])
                    await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            else:
                msg = await self.client.say(DBtext[7])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            msg = await self.client.say(DBtext[8])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)

    # --------------- Command to stop RAINBOOMING  ---------------

    @commands.command(pass_context=True, aliases=['stop'])
    async def r_stop(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        global rainbow_flag
        rainbow_flag = False
        await self.client.say(DBtext[9])

def setup(client):
    client.add_cog(RainbowCommands(client))
