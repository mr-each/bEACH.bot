import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'.txt', encoding='utf-8')
DBtext = f.read().splitlines()
f.close()

class CutieMarksCommands:
    def __init__(self, client):
        self.client = client

    # --------------- Neboyan mark ---------------

    @commands.command(pass_context=True, aliases=['nebayan','nebajan','nebojan','nb'])
    async def neboyan(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        memid = '144055353934348288'
        member = ctx.message.server.get_member(memid)
        if member is None:
            clr = discord.Color.darker_grey()
        else:
            if member.color == discord.Color(0x000000):
                clr = discord.Color.light_grey()
            else:
                clr = member.color
        embed = await bot.newembed(self.client, user_id=memid, content=DBtext[19], color=clr)
        await self.client.say(embed=embed)

    # --------------- TiTupoy mark ---------------

    @commands.command(pass_context=True, aliases=['tt'])
    async def titupoy(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        memid = '135140855982981121'
        member = ctx.message.server.get_member(memid)
        if member is None:
            clr = discord.Color.darker_grey()
        else:
            if member.color == discord.Color(0x000000):
                clr = discord.Color.light_grey()
            else:
                clr = member.color
        embed = await bot.newembed(self.client, user_id=memid, content=DBtext[37], color=clr)
        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(CutieMarksCommands(client))
