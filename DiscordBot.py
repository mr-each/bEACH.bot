import discord
from discord.ext import commands

localesign = 'RU'

# Reading TOKEN from file
f = open('DBtoken.txt')
DBtoken = f.read()
f.close()

# Getting help command content
helplist = {}
with open('locale/help'+localesign+'.txt', encoding='utf-8') as file:
    for line in file:
        key, value = line.split('+++')
        value = value.replace('\n', '')
        helplist[key] = value

client = commands.Bot(command_prefix = 'sr.')  # Command prefix
client.remove_command('help')  # Removing default HELP command

extensions = [
    'modules.ChatCommands',
    'modules.UtilityCommands',
    'modules.CutieMarksCommands',
    'modules.RoleCommands',
    'modules.RainbowCommands'
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
        helpembed = discord.Embed(
            title = helplist['title'],
            description = helplist['prefix'],
            color = discord.Color.green()
        )

        helpembed.set_thumbnail(url=client.user.avatar_url)
        helpembed.add_field(inline=False, name=helplist['chatcmd'],  # Chat commands
                            value = helplist['cc-clr'] + '\n' + helplist['cc-qt'] + '\n' + helplist['cc->>'])

        helpembed.add_field(inline=False, name=helplist['utilcmd'],  # Util commands
                            value=helplist['ut-bly'] + '\n' + helplist['ut-ab'] + '\n' + helplist['ut-ggl'] + '\n' +
                                  helplist['ut-rq'] + '\n' + helplist['ut-mgm'])

        helpembed.add_field(inline=False, name=helplist['cutiemarkcmd'],  # Cutie mark commands
                            value = helplist['cm-nb'] + '\n' + helplist['cm-tt'])

        helpembed.add_field(inline=False, name=helplist['rolecmd'],  # Role commands
                            value = helplist['rlc-ca'])

        helpembed.add_field(name=helplist['rainbowcmd'], inline=False,  # RAINBOW commands
                            value = helplist['rc-mkr'] + '\n' + helplist['rc-gvr'] + '\n' +
                                    helplist['rc-stt'] + '\n' + helplist['rc-stp'])

        await client.say(embed=helpembed)

    client.run(DBtoken)
