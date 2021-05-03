from discord.ext import commands

# Command to DM a user
# await bot.send_message(message.author, "#The message")


class DefaultKaomoji(commands.Cog):
    """
    This cog encodes popular kaomoji for immediate use. All commands print the kaomoji requested to the channel that the
    command was used in.
    """

    # Information about the general commands of the bot (in the dictionary format required by embeds)
    general_cmds = [{'inline': False, 'name': 'd!lenny', 'value': '( ͡° ͜ʖ ͡°)'},
                    {'inline': False, 'name': 'd!flowergirl', 'value': '(✿◕‿◕)'}]

    admin_cmds = []

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

    # @commands.command()
    # async def lenny(self, ctx):
    #     """
    #     ( ͡° ͜ʖ ͡°)
    #
    #     Parameters:
    #         ctx (commands.Context): The required context for commands
    #     """
    #     await ctx.send('( ͡° ͜ʖ ͡°)')
    #
    # @commands.command()
    # async def flowergirl(self, ctx):
    #     """
    #     (✿◕‿◕)
    #
    #     Parameters:
    #         ctx (commands.Context): The required context for commands
    #     """
    #     await ctx.send('(✿◕‿◕)')

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listen for a message containing a kaomoji command from above. Allows a user to use commands in the middle of a
        message.

        Parameters:
            ctx (commands.Context): The required context for commands
            message (Message): The message that was sent
        """

        # Prevent the bot from responding to itself
        if message.author != self.bot.user:
            if 'd!lenny' in message.content:
                await message.channel.send('( ͡° ͜ʖ ͡°)')

                # Send a DM to the user containing the kaomoji
                await message.author.send('( ͡° ͜ʖ ͡°)')
            if 'd!flowergirl' in message.content:
                await message.channel.send('(✿◕‿◕)')


def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(DefaultKaomoji(bot))
