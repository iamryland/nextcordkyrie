# dev.py - code by Rye
# This contains Dev tools accessible through discord
import time
import runtime
import asyncio
import datetime
import nextcord
from typing import List
from nextcord.ext import commands
from http.client import HTTPException


class Dev(commands.Cog, command_attrs=dict(hidden=True, )):
    """This driver elevates the Owner's abilities to allow dev work on the bot"""
    def __init__(self, bot: runtime.SnowBot):
        self.bot = bot
        self.session_start: datetime.datetime
        self.session_start = datetime.datetime.utcnow()

    @commands.command()
    @commands.is_owner()
    async def server_list(self, ctx):
        """Lists the servers the bot is currently in"""
        currently_in = {}
        async for guild in self.bot.fetch_guilds():
            currently_in[f'{guild.id}'] = guild.name
        msg = '```*Currently I am in these servers:*\n'
        for guild_id, name in currently_in.items():
            msg += f' - {guild_id} = {name}\n'
        msg += '```'
        await ctx.send(msg)

    @commands.command()
    @commands.is_owner()
    async def cguilds(self, ctx):
        """Guilds in memory, and their prefix"""
        to_send = f'```Guilds Stored: {len(self.bot.cguilds)}\n\n'
        for cg in self.bot.cguilds:
            to_send += f'{cg.gid} - {cg.name} - prefix=[ {cg.prefix} ]\n'
        to_send += '\n```'
        await ctx.message.delete()
        await ctx.send(to_send)

    @commands.command()
    @commands.is_owner()
    async def loaded(self, ctx):
        """Shows which cogs are loaded"""
        cogs = self.bot.cogs
        msg = '```Currently loaded Sectors/Drivers\n\n'
        for item in cogs:
            current = self.bot.get_cog(item)
            if current.description == 'Hidden':
                continue
            msg += f' - {current.qualified_name} : {current.description}\n'
        msg += '```'
        await ctx.send(msg)

    @commands.command()
    @commands.is_owner()
    async def cleanup(self, ctx):
        """Cleans up the messages the bot and owner send during a Dev session"""
        to_delete = []
        async for message in ctx.channel.history(limit=250, after=self.session_start):
            if message.author == self.bot.user or message.author.id == self.bot.owner_id:
                to_delete.append(message)
            else:
                continue

        def in_msg(m):
            return m in to_delete

        deleted = await ctx.channel.purge(limit=250, check=in_msg)
        tm = self.session_start
        await ctx.send(f'`Cleaned up [{len(deleted)}] messages from session'
                       f' starting at [{tm.month}/{tm.day}] [{str(tm.time())[:5]}](UTC)`')

    @commands.command()
    @commands.is_owner()
    async def leave_guild(self, ctx, guild_id):
        """Leaves the guild based on a given ID"""
        guild = self.bot.get_guild(int(guild_id))
        if guild is None:
            fail = await ctx.send(f'`Failed to find guild with ID of: {guild_id}`')
            await asyncio.sleep(3)
            await fail.delete()
        else:
            try:
                await guild.leave()
                msg = await ctx.send(f'`Successfully left the guild [{guild.name}]({guild.id})`')
            except HTTPException:
                msg = await ctx.send(f'`Failed to leave [{guild.name}]({guild.id})`')
            await asyncio.sleep(3)
            await msg.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def get_invite(self, ctx, server_id):
        """Gets an invitation to a server the bot resides in given the ID"""
        guild = self.bot.get_guild(int(server_id))
        invite = None
        for channel in guild.text_channels:
            invite = await channel.create_invite(max_uses=1, reason='RY HAS POWERSSSS')
            break
        await ctx.message.delete()
        if invite:
            await ctx.send(f'{invite.url}')

    @commands.command()
    @commands.is_owner()
    async def dev_shutdown(self, ctx):
        """Gracefully shuts down the bot; processes involved printed below.

        - Notifies bot owner that shutdown was initiated
        - Saves all persistent data about guilds and the bot to
          files or a database per data requirements.
        - Sends a good bye, then logs out the bot"""

        await self.bot.change_presence(status=nextcord.Status.invisible)
        self.bot.dba.cleanup()

        await ctx.message.delete()
        print('Logged out, closing program.', end='\r')
        await asyncio.sleep(1)
        print('Logged out, closing program..', end='\r')
        await asyncio.sleep(1)
        print('Logged out, closing program...', end='\n')
        if self.bot.is_closed():
            return
        try:
            await self.bot.close()
        except RuntimeError:
            pass

    @commands.command()
    async def tictactoe(self, ctx):
        await ctx.send('TicTacToe', view=TicTacToe())


class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0], ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


def setup(bot):
    bot.add_cog(Dev(bot))
