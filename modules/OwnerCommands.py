import discord
from discord.ext import commands
import json
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
DBtext = bot.load_locale('OwnerCommands')

class OwnerCommands:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    @commands.check(bot.owner)
    async def change_bot_name(self, ctx, name):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        server = ctx.message.server
        member = server.get_member(self.client.user.id)
        await self.client.change_nickname(member, name)

    @commands.command(pass_context=True, aliases=['cnt'])
    @commands.check(bot.owner)
    async def content(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        
        print(ctx.message.content)

    @commands.command(pass_context=True, aliases=[])
    @commands.check(bot.owner)
    async def find_user(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)

        target = ctx.message.content.split().pop(1)
        user_id = bot.clear_user_ID(target)
        user = await self.client.get_user_info(user_id)

        embed = discord.Embed(description='id: '+user.id)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        await self.client.say(embed=embed)

    @commands.command(pass_context=True, aliases=[])
    @commands.check(bot.owner)
    async def vbucks_set(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        
        with open('users.json', 'r') as f:
            users = json.load(f)

        target, amount = ctx.message.content.split()[1:]
        user_id = bot.clear_user_ID(target)
        user = await self.client.get_user_info(user_id)
        await bot.change_vbucks_amount(self.client, users, ctx.message.server, user, int(amount))

        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'bEACH_vbucks')
        await self.client.say("{}'s {} changed to **{}**{}".format(target, emoji, amount, emoji))

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    @commands.command(pass_context=True, aliases=[])
    @commands.check(bot.owner)
    async def vbucks_change(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        
        with open('users.json', 'r') as f:
            users = json.load(f)

        target, amount = ctx.message.content.split()[1:]
        user_id = bot.clear_user_ID(target)
        user = await self.client.get_user_info(user_id)
        await bot.add_vbucks(self.client, users, ctx.message.server, user, int(amount))

        emoji = discord.utils.get(self.client.get_all_emojis(), name = 'bEACH_vbucks')
        await self.client.say("{}'s {} changed by **{}**{}".format(target, emoji, amount, emoji))

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

def setup(client):
    client.add_cog(OwnerCommands(client))