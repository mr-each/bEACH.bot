import discord
from discord.ext import commands
import json
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
DBtext = bot.load_locale('VBucksSystem')

class VBucksSystem:
    def __init__(self, client):
        self.client = client

    # --------------- Daily vbusck giveaway ---------------
    
    @commands.command(pass_context=True, aliases=[])
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def v_daily(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
    
        with open('users.json', 'r') as f:
            users = json.load(f)

        amount = 5
        await bot.add_vbucks(self.client, users, ctx.message.server, ctx.message.author, amount)

        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'bEACH_vbucks')
        msg = await self.client.say(DBtext[1].format(amount, emoji))
        await bot.clear_last_selfmessage(self.client, msg, msg.channel)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    @v_daily.error
    async def v_daily_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.message.channel.is_private is True:
                return
            await self.client.delete_message(ctx.message)

            time = bot.secconds_to_time(error.retry_after)
            if int(time['hours']) < 1:
                after = DBtext[2].format(int(time['minutes'])+1)
            else:
                after = DBtext[3].format(time['hours'], time['minutes'])

            msg = await self.client.say(DBtext[4].format(after))
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
        else:
            print(str(error))

    @commands.command(pass_context=True, aliases=[])
    async def v_give(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        server = ctx.message.server
        author = ctx.message.author
        # Checking command's arguments
        try:
            target, amount = ctx.message.content.split()[1:]
        except Exception:
            msg = await self.client.say(DBtext[5])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        user_id = bot.clear_user_ID(target)
        # Checking for user existence
        try:
            user = await self.client.get_user_info(user_id)
        except Exception:
            msg = await self.client.say(DBtext[6])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        # Checking if target is message author
        if user == author:
            msg = await self.client.say(DBtext[7])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        # Checking for integer amount value
        try:
            int(amount)
        except Exception:
            msg = await self.client.say(DBtext[8])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        with open('users.json', 'r') as f:
            users = json.load(f)
        # Checking author's currency status
        if int(amount) > users[server.id][ctx.message.author.id]['vbucks']:
            msg = await self.client.say(DBtext[9])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        # Checking if ammount is positive number
        if int(amount) < 1:
            msg = await self.client.say(DBtext[10])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return
        # Checking target existence in DB
        if not user.id in users:
            msg = await self.client.say(DBtext[11])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            return

        await bot.add_vbucks(self.client, users, server, author, int(amount)*(-1))
        await bot.add_vbucks(self.client, users, server, user, int(amount))
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'bEACH_vbucks')
        msg = await self.client.say(DBtext[12].format(author.mention, int(amount), emoji, target))
        if user != self.client.user:
            await self.client.send_message(user, DBtext[13].format(author.mention, int(amount), emoji, server.name))
        await bot.clear_last_selfmessage(self.client, msg, msg.channel)

    # --------------- NAME ---------------
    
    @commands.command(pass_context=True, aliases=[])
    async def v_info(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        server = ctx.message.server
        user = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        #Database update in case the user is not there
        if (not server.id in users) or (not user.id in users[server.id]):
            await bot.update_data(users, ctx.message.server, ctx.message.author)

        #Embed
        exp_needed = (((users[server.id][user.id]['level']+1)**4)//5 + 1) * 5
        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'bEACH_vbucks')
        infoembed = discord.Embed(
            description=
            DBtext[14].format(users[server.id][user.id]['level']) + '\n' +
            DBtext[15].format(users[server.id][user.id]['experience'],exp_needed) + '\n' +
            DBtext[16].format(users[server.id][user.id]['vbucks'],emoji)
            ,
            color=discord.Color.dark_orange()
        )
        infoembed.set_author(name = user.display_name)
        infoembed.set_thumbnail(url = user.avatar_url)
        if ctx.message.server.icon is None:
            icon = discord.Embed.Empty
        else:
            icon = DBtext[17].format(server.id,server.icon)
        infoembed.set_footer(text = DBtext[18].format(server.name), icon_url = icon)
        
        await self.client.say(embed = infoembed)
    
    # --------------- LEVEL ---------------
    # --------------- Add new member to users database ---------------
    
    async def on_member_join(self, member):
        if member.bot is True:
            return
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await bot.update_data(users, member.server, member)
            
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4, sort_keys=True)

    # --------------- Giving EXP and LVL to user on message ---------------

    async def on_message(self, message):
        if (message.author == self.client.user) or (message.channel.is_private is True):
            return

        if message.author.bot is True:
            return

        if message.content.startswith('sr.') or message.content.startswith('Sr.'):
            pass
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await bot.update_data(users, message.server, message.author)
            await bot.spam_cooldown(self.client, users, message)
            await bot.add_experience(users, message.server, message.author, 5)
            await bot.level_up(self.client, users, message.server, message.channel, message.author)
            
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4, sort_keys=True)
    
def setup(client):
    client.add_cog(VBucksSystem(client))