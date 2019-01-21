import discord
from discord.ext import commands
import random
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'.txt', encoding='utf-8')
DBtext = f.read().splitlines()
f.close()
# Getting links
f = open('linklist.txt', encoding='utf-8')
linklist = f.read().splitlines()
f.close()

class UtilityCommands:
    def __init__(self, client):
        self.client = client

    # --------------- Command for bullying someone ---------------

    @commands.command(pass_context=True, aliases=['bly','bul'])
    async def bully(self, ctx, targetID=''):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        # Getting phrases for bullying
        bullying = {}
        with open('locale/bullying'+localesign+'.txt', encoding='utf-8') as file:
            for line in file:
                key, value = line.split('+++')
                value = value.replace('\n', '')
                bullying[key] = value

        if targetID == '':
            msg = await self.client.say(DBtext[9])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            cmd, cnt = ctx.message.content.split(' ', 1)
            num = random.randint(1,(len(bullying)//2))
            bullyline = 'bly' + str(num)
            bullyauth = 'auth' + str(num)
            bullyembed = discord.Embed(
                description = bullying[bullyline],
                color = discord.Color.red()
            )
            bullyembed.set_thumbnail(url=linklist[1])
            bullyembed.set_footer(text = '— ' + bullying[bullyauth])

            await self.client.say(DBtext[11] + cnt + '!', embed=bullyembed)

    # --------------- Command for adding new bullying line ---------------

    @commands.command(pass_context=True)
    async def addbull(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        try:
            cmd, cnt = ctx.message.content.split(' ', 1)
        except ValueError:
            msg = await self.client.say(DBtext[12])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        if cnt == '':
            msg = await self.client.say(DBtext[12])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            bullying = {}
            with open('locale/bullying'+localesign+'.txt', encoding='utf-8') as file:
                for line in file:
                    key, value = line.split('+++')
                    value = value.replace('\n', '')
                    bullying[key] = value
            f = open('locale/bullying' + localesign + '.txt', 'a', encoding='utf-8')
            f.write('\nbly'+str((len(bullying)//2))+'+++'+cnt)
            f.write('\nauth'+str((len(bullying)//2))+'+++'+ctx.message.author.name)
            f.close()
            await self.client.say(DBtext[24])

    # --------------- Command for ragequitting  ---------------

    @commands.command(pass_context=True, aliases=['rq'])
    async def ragequit(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        bot.megumin_img(ctx.message.author.avatar_url)
        rqch = await self.client.create_channel(ctx.message.server, 'rq', type=discord.ChannelType.voice)
        await self.client.move_member(ctx.message.author, rqch)
        await self.client.delete_channel(rqch)
        await self.client.send_file(ctx.message.channel, 'out.png', content=DBtext[25] + ctx.message.author.mention + '!')

    # --------------- Command for getting personal Megumin image  ---------------

    @commands.command(pass_context=True, aliases=['mgm'])
    async def megumin(self, ctx, targetID=''):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if targetID == '':
            target = ctx.message.author
        else:
            targetID = bot.clrUID(targetID)
            try:
                target = await self.client.get_user_info(targetID)
            except discord.NotFound:
                msg = await self.client.say(DBtext[27])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
                return
        bot.megumin_img(target.avatar_url)
        await self.client.send_file(ctx.message.author, 'out.png', content=DBtext[25] + target.name + '!')

    # --------------- LMGTFY command ---------------

    @commands.command(pass_context=True, aliases=['ggl'])
    async def google(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        cmd, cnt = ctx.message.content.split(' ', 1)
        if len(cnt) < 22:
            msg = await self.client.say(DBtext[36])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            targetID, search = cnt.split(' ', 1)
            try:
                await self.client.get_user_info(bot.clrUID(targetID))
            except discord.NotFound:
                msg = await self.client.say(DBtext[27])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
                return
            if search == '':
                msg = await self.client.say(DBtext[31])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
                return
            else:
                gglembed = discord.Embed(
                    description='**' + ctx.message.author.name + '**' + DBtext[32] + '\n' + DBtext[33] + '\n' + DBtext[34] + search.replace(' ', '+') + DBtext[35],
                    color=discord.Color.teal()
                )
                gglembed.set_thumbnail(url=linklist[2])
                await self.client.say(DBtext[11] + targetID + '!', embed=gglembed)

def setup(client):
    client.add_cog(UtilityCommands(client))
