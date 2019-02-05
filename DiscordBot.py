import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Reading TOKEN from file
DBtoken = bot.load_token()

# Getting locale text for replies
DBtext = bot.load_locale('DiscordBot')

prefix = ['sr.', 'Sr.']

client = commands.Bot(command_prefix = prefix)  # Command prefixes
client.remove_command('help')  # Removing default HELP command

last_help_message = None

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

        helplist = bot.load_help_list()
        
        global last_help_message

        try:
            await client.delete_message(last_help_message)
        except Exception as error:
            print(str(error))

        value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>']
        helpembed = bot.create_help(client, f1=value)
        
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
        vb_emoji = discord.utils.get(client.get_all_emojis(), name = 'bEACH_vbucks')

        helplist = bot.load_help_list()
        
        if reaction.message.id == last_help_message.id:
            await client.remove_reaction(reaction.message, reaction.emoji, user)
            # Chat commands
            if reaction.emoji == '💬':
                value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>']
                helpembed = bot.create_help(client, f1=value)
                await client.edit_message(last_help_message, embed=helpembed)
            # Util commands
            elif reaction.emoji == '🇺':
                value = helplist['ut-bly'] + '\n' + helplist['ut-ab'] + '\n' + helplist['ut-ggl'] + '\n' + helplist['ut-rq'] + '\n' + helplist['ut-mgm']
                helpembed = bot.create_help(client, f2=value)
                await client.edit_message(last_help_message, embed=helpembed)
            # Role commands
            elif reaction.emoji == '⭐':
                value = helplist['rlc-ca']
                helpembed = bot.create_help(client, f3=value)
                await client.edit_message(last_help_message, embed=helpembed)
            # V-bucks commands
            elif reaction.emoji == vb_emoji:
                value = helplist['vb-inf'] + '\n' + helplist['vb-day'] + '\n' + helplist['vb-gv']
                helpembed = bot.create_help(client, f4=value)
                await client.edit_message(last_help_message, embed=helpembed)
            # Cutie mark commands
            elif reaction.emoji == '🦄':
                value = helplist['cm-nb'] + '\n' + helplist['cm-tt']+ '\n' + helplist['cm-th']
                helpembed = bot.create_help(client, f5=value)
                await client.edit_message(last_help_message, embed=helpembed)
            # RAINBOW commands
            elif reaction.emoji == '🏳️‍🌈': 
                value = helplist['rc-mkr'] + '\n' + helplist['rc-gvr'] + '\n' + helplist['rc-stt'] + '\n' + helplist['rc-stp']
                helpembed = bot.create_help(client, f6=value)
                await client.edit_message(last_help_message, embed=helpembed)
            else:
                return

    # --------------- Private message handler ---------------

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.channel.is_private is True:
            await client.send_message(message.channel, DBtext[1])
            return
        
        await client.process_commands(message)

    client.run(DBtoken)