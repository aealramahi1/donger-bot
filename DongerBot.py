import discord
from discord.ext import commands
from Token import TOKEN

# All command are called using the format d!cmdname
bot = commands.Bot(command_prefix='d!')

# List of all the cogs that this bot will run by default
all_cogs = ['DefaultKaomoji']

# Contains all the loaded cogs (which will be all the cogs unless some are unloaded)
current_cogs = ['DefaultKaomoji']

# Remove the default help command since we will rewrite it
bot.remove_command('help')


@bot.event
async def on_ready():
    """
    Called when the bot runs.
    """
    print('Bot successfully connected!')


@bot.command(aliases=['load', 'loadcog'])
@commands.has_permissions(manage_messages=True)
async def load_cog(ctx, ext):
    """
    Load the cog from within the Discord guild. This makes it easier to add new features to the bot

    Parameters:
        ctx (commands.Context): The required context for commands
        ext (str): The name of the cog (without the .py)
    """
    try:

        # Check to make sure we actually need to load this cog
        if ext not in current_cogs:

            # All cogs are in the cogs folder
            bot.load_extension('cogs.%s' % ext)
            current_cogs.append(ext)

            if ext not in all_cogs:
                all_cogs.append(ext)
            await ctx.send('Cog loaded successfully!')
        elif ext in current_cogs:
            await ctx.send('This cog is already loaded')
    except IOError:

        # If the cog doesn't exist and throws an error then we can deal with it
        await ctx.send('This cog does not exist.')


@bot.command(aliases=['unload', 'unloadcog'])
@commands.has_permissions(manage_messages=True)
async def unload_cog(ctx, ext):
    """
    Unload a cog from within the Discord guild. This will disable any features that the bot may have been using from
    this cog

    Parameters:
        ctx (commands.Context): The required context for commands
        ext (str): The name of the cog (without the .py)
    """

    # Check to make sure this cog is loaded so we can unload it
    if ext in current_cogs:
        bot.unload_extension('cogs.%s' % ext)
        current_cogs.remove(ext)
        await ctx.send('Cog unloaded successfully!')
    elif ext not in current_cogs:
        await ctx.send('This cog is not loaded or doesn\'t exist.')


@bot.command(aliases=['reload', 'reloadcog'])
@commands.has_permissions(manage_messages=True)
async def reload_cog(ctx, ext):
    """
    Unload and the load a cog. Useful when the code of a cog is updated

    Parameters:
        ctx (commands.Context): The required context
        ext (str): The name of the cog (without the .py)
    """
    bot.reload_extension('cogs.%s' % ext)
    await ctx.send('Cog successfully reloaded!')


@bot.command(aliases=['viewloadedcogs', 'viewloaded', 'vlc'])
async def view_loaded_cogs(ctx):
    """
    Show a list of all the currently loaded cogs.

    Parameters:
        ctx (commands.Context): The required context for commands
    """
    await ctx.send('Currently loaded cogs:')
    for the_cog in current_cogs:
        await ctx.send('-%s\n' % the_cog)


@bot.command(aliases=['viewavailablecogs', 'viewavailable', 'vac'])
async def view_available_cogs(ctx):
    """
    Show a list of all the available, unloaded cogs.

    Parameters:
        ctx (commands.Context): The required context for commands
    """
    await ctx.send('Available cogs:')
    for the_cog in all_cogs:
        if the_cog not in current_cogs:
            await ctx.send('-%s' % the_cog)


@bot.command(aliases=['stop', 'end'])
@commands.has_permissions(manage_messages=True)
async def halt(ctx):
    """
    Halt the execution of the bot from within the Discord guild.

    Parameters:
        ctx (commands.Context): The required context for commands
    """
    await ctx.send('DongerBot out (⌐■_■)')
    await bot.logout()


@bot.command()
async def help(ctx):
    """
    Send an embed with the commands and descriptions for all the loaded cogs.

    Parameters:
        ctx (commands.Context): The required context for commands
    """

    help_embed_dict = {'fields': [{'inline': False, 'name': '\u200b', 'value': '\u200b'}],
                       'type': 'rich',
                       'description': 'Command list for all loaded cogs',
                       'title': 'Nito Commands'}

    admin_commands = [{'inline': True, 'name': 'ADMIN COMMANDS:', 'value': '\u200b'},
                      {'inline': False, 'name': 'd!load_cog\td!loadcog\td!load',
                       'value': 'Loads the cog passed in, if it exists.'},
                      {'inline': False, 'name': 'd!unload_cog\td!unloadcog\td!unload',
                       'value': 'Unloads the cog passed in, if it is loaded.'},
                      {'inline': False, 'name': 'd!reload_cog\td!reloadcog\td!reload',
                       'value': 'Unloads and reloads a loaded cog.'},
                      {'inline': False, 'name': 'd!halt', 'value': 'Stops execution of the bot.'}]

    general_commands = [{'inline': True, 'name': 'GENERAL COMMANDS:', 'value': '\u200b'},
                        {'inline': False, 'name': 'd!view_loaded_cogs\td!viewloadedcogs\td!viewloaded\td!vlc',
                         'value': 'Shows a list of all the currently loaded cogs.'}]

    # Add the admin commands from all the other loaded cogs
    for each_cog in current_cogs:
        admin_cmds = bot.get_cog(each_cog).admin_cmds
        admin_commands.extend(admin_cmds)

    # Add the general commands from all the other loaded cogs
    for each_cog in current_cogs:
        general_cmds = bot.get_cog(each_cog).general_cmds
        general_commands.extend(general_cmds)

    # Add a blank line in between the admin commands and general commands
    admin_commands.append({'inline': False, 'name': '\u200b', 'value': '\u200b'})

    # Construct the dictionary for the help embed from the general and admin commands, then make an embed from the
    # newly constructed dictionary
    help_embed_dict['fields'].extend(admin_commands)
    help_embed_dict['fields'].extend(general_commands)
    help_embed = discord.Embed.from_dict(help_embed_dict)

    await ctx.send(embed=help_embed)


# Each cog in the list is loaded in automatically whenever we run the program
for cog in all_cogs:
    bot.load_extension('cogs.%s' % cog)

bot.run(TOKEN)
