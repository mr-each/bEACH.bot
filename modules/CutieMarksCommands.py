import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'/CutieMarksCommands', encoding='utf-8')
DBtext = ['null']
DBtext.extend(f.read().splitlines())
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

        embed = await bot.cutiemark(self.client, ctx.message, '144055353934348288', DBtext[1])
        await self.client.say(embed=embed)

    async def on_message(self, message):
        if (message.author == self.client.user) or (message.channel.is_private is True):
            return
        
        words = message.content.lower().split()
        for word in words:
            if word == 'боян' or word == 'баян':
                embed = await bot.cutiemark(self.client, message, '144055353934348288', DBtext[1])
                await self.client.send_message(message.channel, embed=embed)
                return       
        
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'boyan')
        if (reaction.count < 2) and (reaction.emoji == emoji):
            embed = await bot.cutiemark(self.client, reaction.message, '144055353934348288', DBtext[1])
            await self.client.send_message(channel ,embed=embed)

    # --------------- TiTupoy mark ---------------

    @commands.command(pass_context=True, aliases=['tt'])
    async def titupoy(self, ctx):
        if await self.client.is_owner(ctx.message.author):
            if ctx.message.channel.is_private is True:
                return
            await self.client.delete_message(ctx.message)

            embed = await bot.cutiemark(self.client, ctx.message, '135140855982981121', DBtext[2])
            await self.client.say(embed=embed)

    # --------------- TupaHeyt mark ---------------

    @commands.command(pass_context=True, aliases=['th','hate'])
    async def tupaheyt(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        embed = await bot.cutiemark(self.client, ctx.message, '533991178245505024', DBtext[3])
        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(CutieMarksCommands(client))
