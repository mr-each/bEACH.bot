import discord
from discord.ext import commands

localesign = 'RU'

# Reading TOKEN from file
f = open('DBtoken.txt')
DBtoken = f.read()
f.close()

# Getting locale text for replies
f = open('locale/DBtext'+localesign+'/DiscordBot', encoding='utf-8')
DBtext = ['null']
DBtext.extend(f.read().splitlines())
f.close()

prefix = ['sr.', 'Sr.']

client = commands.Bot(command_prefix = prefix)  # Command prefixes
client.remove_command('help')  # Removing default HELP command

helplist = {}
last_help_message = None
last_reaction = '💬'

extensions = [
    'modules.ChatCommands',
    'modules.UtilityCommands',
    'modules.CutieMarksCommands',
    'modules.RoleCommands',
    'modules.RainbowCommands',
    'modules.VBucksSystem',
    'modules.OwnerCommands'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    @client.event
    async def on_ready():
        await client.change_presence(game=discord.Game(name='sr.help'))  # Giving custom status
        print('Connected!')
        print('Username: ' + client.user.name + ' ID: ' + client.user.id)
        print('------')

    # --------------- Help command ---------------

    @client.command(pass_context=True)
    async def help(ctx):
        if ctx.message.channel.is_private is True:
            return
        await client.delete_message(ctx.message)

        with open('locale/help'+localesign+'.txt', encoding='utf-8') as file:
            for line in file:
                key, value = line.split('+++')
                value = value.replace('\n', '')
                helplist[key] = value
        
        global last_help_message

        try:
            await client.delete_message(last_help_message)
        except Exception as error:
            print(str(error))

        helpembed = discord.Embed(
            description = helplist['prefix'],
            color = discord.Color.green()
        )
        helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
        helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                            value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>'])
        helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                            value = DBtext[2])
        helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                            value = DBtext[3])
        helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                            value = DBtext[4])
        helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                            value = DBtext[5])
        helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                            value = DBtext[6])
        
        last_help_message = await client.say(embed=helpembed)

        vb_emoji= discord.utils.get(client.get_all_emojis(), name = 'bEACH_vbucks')
        emojis = ['💬','🇺','⭐', vb_emoji, '🦄', '🏳️‍🌈']
        for emoji in emojis:
            await client.add_reaction(last_help_message, emoji)

    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user:
            return
        
        global last_help_message
        global last_reaction
        vb_emoji = discord.utils.get(client.get_all_emojis(), name = 'bEACH_vbucks')
        with open('locale/help'+localesign+'.txt', encoding='utf-8') as file:
            for line in file:
                key, value = line.split('+++')
                value = value.replace('\n', '')
                helplist[key] = value
        
        if reaction.message.id == last_help_message.id:
            await client.remove_reaction(reaction.message, reaction.emoji, user)
            if reaction.emoji == '💬':
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>'])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = DBtext[2])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = DBtext[3])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = DBtext[4])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = DBtext[5])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                                    value = DBtext[6])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            elif reaction.emoji == '🇺':
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = DBtext[1])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = helplist['ut-bly'] + '\n' + helplist['ut-ab'] + '\n' + helplist['ut-ggl'] + '\n' + 
                                            helplist['ut-rq'] + '\n' + helplist['ut-mgm'])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = DBtext[3])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = DBtext[4])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = DBtext[5])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                                    value = DBtext[6])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            elif reaction.emoji == '⭐':
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = DBtext[1])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = DBtext[2])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = helplist['rlc-ca'])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = DBtext[4])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = DBtext[5])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                                    value = DBtext[6])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            elif reaction.emoji == vb_emoji:
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = DBtext[1])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = DBtext[2])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = DBtext[3])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = helplist['vb-inf'] + '\n' + helplist['vb-day'] + '\n' + helplist['vb-gv'])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = DBtext[5])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                                    value = DBtext[6])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            elif reaction.emoji == '🦄':
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = DBtext[1])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = DBtext[2])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = DBtext[3])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = DBtext[4])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = helplist['cm-nb'] + '\n' + helplist['cm-tt']+ '\n' + helplist['cm-th'])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                                    value = DBtext[6])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            elif reaction.emoji == '🏳️‍🌈':
                helpembed = discord.Embed(
                    description = helplist['prefix'],
                    color = discord.Color.green()
                )
                helpembed.set_author(name = helplist['title'], icon_url = client.user.avatar_url)
                helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                                    value = DBtext[1])
                helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                                    value = DBtext[2])
                helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                                    value = DBtext[3])
                helpembed.add_field(inline=False, name=helplist['vbuckscmd'],  # V-bucks commands
                                    value = DBtext[4])
                helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                                    value = DBtext[5])
                helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                        value = helplist['rc-mkr'] + '\n' + helplist['rc-gvr'] + '\n' + helplist['rc-stt'] + '\n' + 
                                helplist['rc-stp'])

                last_reaction = reaction.emoji
                await client.edit_message(last_help_message, embed=helpembed)
            else:
                return

    # --------------- Private message handler ---------------

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.channel.is_private is True:
            await client.send_message(message.channel, DBtext[7])
            return
        
        await client.process_commands(message)

    client.run(DBtoken)