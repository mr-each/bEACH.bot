import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'/RoleCommands', encoding='utf-8')
DBtext = ['null']
DBtext.extend(f.read().splitlines())
f.close()

class RoleCommands:
    def __init__(self, client):
        self.client = client

    # --------------- Command for creating an achievement role ---------------

    @commands.command(pass_context=True)
    async def crach(self, ctx):
        if ctx.message.channel.is_private is True:
            return
        await self.client.delete_message(ctx.message)
        if ctx.message.author.server_permissions.manage_roles is True:
            if ctx.message.content[9:] == '':
                msg = await self.client.say(DBtext[1])
                await bot.clear_last_selfmessage(self.client, msg, msg.channel)
            else:
                cr_role = ctx.message.content[9:]
                server_name = ctx.message.server
                await self.client.create_role(server_name, name='⭐' + str(cr_role) + '⭐', permissions=discord.Permissions.none(), color=discord.Color(0xddc90d))
                discord.utils.get(ctx.message.server.roles, name=cr_role)
                new_role_name = cr_role
                await self.client.say(DBtext[2].format(new_role_name))
        else:
            msg = await self.client.say(DBtext[3])
            await bot.clear_last_selfmessage(self.client, msg, msg.channel)

def setup(client):
    client.add_cog(RoleCommands(client))
