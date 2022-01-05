# error.py - code by Rye

# This file will contain the error event handler
# and will handle all errors based on type
import asyncio
import nextcord
from nextcord.ext import commands


async def handle(ctx, error, bot):
    if ctx.message.content.startswith('..'):
        pass
    else:
        embed = nextcord.Embed(title='Error Message', description='', color=nextcord.Color.blurple())
        if isinstance(error, commands.CommandError):
            if isinstance(error, commands.UserInputError):
                if isinstance(error, commands.MissingRequiredArgument):
                    embed.add_field(name='**Missing required argument!**',
                                    value=f'Argument: {error.param}\n'
                                          f'Please provide the required argument.')
                if isinstance(error, commands.TooManyArguments):
                    embed.add_field(name='**Too Many Arguments!**',
                                    value='Please send less arguments.')
                if isinstance(error, commands.BadArgument):
                    if isinstance(error, commands.MessageNotFound):
                        embed.add_field(name='**Message Not Found**',
                                        value=f'Message that was not found:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.MemberNotFound):
                        embed.add_field(name='**Member Not Found**',
                                        value=f'Member that was not found:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.UserNotFound):
                        embed.add_field(name='**User Not Found**',
                                        value=f'User that was not found:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.ChannelNotFound):
                        embed.add_field(name='**Channel Not Found**',
                                        value=f'Channel that was not found:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.ChannelNotReadable):
                        embed.add_field(name='**Channel Not Readable**',
                                        value=f'Channel: {error.argument.mention}')
                    if isinstance(error, commands.BadColourArgument):
                        embed.add_field(name='**Bad Color Argument**',
                                        value=f'Argument: {error.argument}')
                    if isinstance(error, commands.RoleNotFound):
                        embed.add_field(name='**Role Not Found**',
                                        value=f'Role that was not found:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.BadInviteArgument):
                        embed.add_field(name='**Bad Invite Argument**',
                                        value='Man, that was not nice.')
                    if isinstance(error, commands.EmojiNotFound):
                        embed.add_field(name='**Emoji Not Found**',
                                        value=f'Failed to find emoji:\n'
                                              f'{error.argument}')
                    if isinstance(error, commands.PartialEmojiConversionFailure):
                        embed.add_field(name='**Partial Emoji Conversion Failure**',
                                        value='Imma be straight up I don\'t know what this is')
                    if isinstance(error, commands.BadBoolArgument):
                        embed.add_field(name='**Bad Boolean Argument**',
                                        value=f'{error.argument}')
            if isinstance(error, commands.CommandNotFound):
                final = ctx.message.content.split(' ')
                embed.add_field(name='**Command Not Found!**',
                                value=f'**Command:** {final[0][1:]}')
            if isinstance(error, commands.CheckFailure):
                if isinstance(error, commands.CheckAnyFailure):
                    pass
                elif isinstance(error, commands.PrivateMessageOnly):
                    embed.add_field(name='**Private Message Only!**',
                                    value=f'{ctx.author.mention}, that can only be used in a Private Message!')
                elif isinstance(error, commands.NoPrivateMessage):
                    embed.add_field(name='**Guild Only Command!**',
                                    value=f'{ctx.author.mention}, you can only use that in a Guild!')
                elif isinstance(error, commands.NotOwner):
                    embed.add_field(name='**You arent the owner of this bot!**',
                                    value=f'L O L! {ctx.author.mention} thought they were my owner :rofl:\n'
                                          f'You can\'t use that\nYou do be funny tho')
                elif isinstance(error, commands.MissingPermissions):
                    embed.add_field(name=f'**Missing Permissions**',
                                    value=f'**User:** [{ctx.author.mention}]\n'
                                          f'**Missing Permissions:** {error.missing_permissions}')
                elif isinstance(error, commands.MissingRole):
                    embed.add_field(name='**Missing Role**',
                                    value=f'**User:** [{ctx.author.mention}]\n'
                                          f'**Missing Role:** {error.missing_role}')
                elif isinstance(error, commands.BotMissingRole):
                    embed.add_field(name='**Bot Missing Role**',
                                    value=f'The bot is missing a required role.\n'
                                          f'**Missing Role:** {error.missing_role}')
                elif isinstance(error, commands.MissingAnyRole):
                    embed.add_field(name='**Missing Role(s)**',
                                    value=f'**User:** [{ctx.author.mention}]\n'
                                          f'**Missing Role(s):** {error.missing_roles}')
                elif isinstance(error, commands.BotMissingAnyRole):
                    embed.add_field(name='**Bot Missing Roles**',
                                    value=f'The bot is missing some roles.\n'
                                          f'**Missing Role(s):** {error.missing_roles}')
                elif isinstance(error, commands.NSFWChannelRequired):
                    embed.add_field(name='**NSFW Channel Required**',
                                    value=f'Please use this in an NSFW channel.\n'
                                          f'Can\'t let the 12 year olds see.')
                else:
                    embed.add_field(name='**A check failed!**',
                                    value='Please ensure that the module is enabled,\n'
                                          'and that you have proper permissions to run that!')
            # if isinstance(error, commands.CommandInvokeError):
            #     pass
            if isinstance(error, commands.DisabledCommand):
                pass
            if isinstance(error, commands.CommandOnCooldown):
                pass
        if isinstance(error, commands.ExtensionError):
            ext_err = 'Extension Error!'
            if isinstance(error, commands.ExtensionAlreadyLoaded):
                embed.add_field(name=ext_err, value=f'The extension (** {error.name} **) is **ALREADY** loaded!')
            if isinstance(error, commands.ExtensionNotLoaded):
                embed.add_field(name=ext_err, value=f'The extension (** {error.name} **) is **NOT** loaded!')
            if isinstance(error, commands.NoEntryPointError):
                embed.add_field(name=ext_err, value=f'The extension (** {error.name} **) has no entry point!\n'
                                                    f'(Add the setup function)')
            if isinstance(error, commands.ExtensionFailed):
                embed.add_field(name=ext_err, value=f'The extension (** {error.name} **) failed :(')
                embed.add_field(name='Original Error:', value=error.original)
            if isinstance(error, commands.ExtensionNotFound):
                embed.add_field(name=ext_err, value=f'The extension (** {error.name} **) **was NOT found!**')
        msg = await ctx.send(embed=embed)
        if 'Dev' in bot.cogs.keys():
            print(error.args)
            print(error)
            print(error.__cause__)
            print(error.with_traceback(error.__traceback__))
        # await ctx.send(error)
        await ctx.message.delete(delay=1)
        await msg.delete(delay=10)


class ErrorHandler(commands.Cog):
    """This is the Error Handler that catches all your dumb mistakes"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await handle(ctx, error.original, self.bot)
        else:
            await handle(ctx, error, self.bot)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
