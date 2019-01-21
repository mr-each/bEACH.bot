import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'.txt', encoding='utf-8')
DBtext = f.read().splitlines()
f.close()

class ChatCommands:
    def __init__(self, client):
        self.client = client

    # --------------- Command for clearing chat ---------------

    @commands.command(pass_context=True, aliases=['clr'])
    async def clear(self, ctx, amount='1'):
        if ctx.message.channel.is_private is True:
            return
        try:
            int(amount)
        except ValueError:
            msg = await self.client.say(DBtext[1])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        amount = int(amount)
        if ctx.message.author.server_permissions.manage_messages is True:
            if 0 < amount < 100:
                channel = ctx.message.channel
                messages = []
                async for message in self.client.logs_from(channel, limit=amount+1):
                    messages.append(message)
                print(messages)
                try:
                    await self.client.delete_messages(messages)
                except Exception as error:
                    msg = await self.client.say(DBtext[20] + ' ' + str(error))
                    await bot.clear_last_selfmessage(self.client, msg, msg.channel)
                    return
                msg = await self.client.say('**' + str(len(messages)-1) + DBtext[2])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            else:
                msg = await self.client.say(DBtext[3])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            msg = await self.client.say(DBtext[4])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)

    # --------------- Command for quoting messages ---------------

    @commands.command(pass_context=True, aliases=['qt','move','mv'])
    async def quote(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if len(ctx.message.content) > 44:
            cmd, chnlID, msgID = ctx.message.content.split()  # Getting channel and message ID of source message
            chnlID = bot.clrCHID(chnlID)  # Clearing channel ID from mention
            chnl_from = self.client.get_channel(chnlID)
            if chnl_from is None:
                msg = await self.client.say(DBtext[22])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
                return
            try:
                msg = await self.client.get_message(chnl_from, msgID)
            except discord.NotFound:
                msg = await self.client.say(DBtext[23])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
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

            await self.client.say(embed=mvembed)
        else:
            msg = await self.client.say(DBtext[21])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)

    # --------------- Command for making embedded messages ---------------

    async def on_message(self, message):
        if message.channel.is_private is True:
            return
            #await self.client.send_message(message.author, "If you want to continue send me your Discord login, password, your credit card number and it's CVV/CVC code")


        if message.author == self.client.user:
            return

        if message.content.startswith('>>'):
            await self.client.delete_message(message)
            if message.author.color == discord.Color(0x000000):
                clr = discord.Color.light_grey()
            else:
                clr = message.author.color
            embed = await bot.newembed(self.client, user_id=message.author.id, content=message.content[2:], color=clr)
            await self.client.send_message(message.channel, embed=embed)

def setup(client):
    client.add_cog(ChatCommands(client))
