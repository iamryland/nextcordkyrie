# games.py - code by Rye
# This file contains fun commands and games :D
import time
from typing import List

import nextcord
from nextcord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rytime(self, ctx, time_period='12h'):
        """What time is it in Rytime?!?!"""
        await ctx.message.delete()
        curr = time.gmtime(time.time())
        day = curr[2]
        if curr[8] == 1:
            pre_hour = curr[3] - 5
            if pre_hour < 0:
                hour = 24 + pre_hour
            else:
                hour = pre_hour
            if hour >= 18:
                day = curr[2] - 1
        elif curr[8] == 0:
            pre_hour = curr[3] - 4
            if pre_hour < 0:
                hour = 24 + pre_hour
            else:
                hour = pre_hour
            if hour >= 19:
                day = curr[2] - 1
        else:
            hour = '(?)' + str(curr[3])

        if day == 0:
            month = 'EOM'
            day = ''
        else:
            month = curr[1]

        formatted = ''
        if time_period == '24h':
            formatted = f'{hour}:{curr[4]}'
        elif time_period == '12h':
            if hour >= 12:
                formatted = f'{hour - 12}:{curr[4]} SP'
            elif hour < 12:
                formatted = f'{hour}:{curr[4]} FP'
        else:
            await ctx.send('Please send a valid time period :point_right::point_left::pleading_face:'
                           '\n(either `12h` or `24h`)')
            return

        embed = nextcord.Embed(title=f'RyTime: {formatted}',
                               description=f'It is day {day} of month {month}\n'
                                           f'It is month {month} of the year {curr[0]}.',
                               color=nextcord.Color.blurple())
        embed.set_footer(text='RyTime Info', icon_url=self.bot.user.avatar.url)
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=15)

    @commands.command()
    async def tictactoe(self, ctx):
        """Yo you wanna play TicTacToe on discord"""
        await ctx.message.delete()
        await ctx.send('Play TicTacToe! `X` goes first!', view=TicTacToe())


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
        if state in (view.playerX, view.playerO):
            return

        if view.current_player == view.playerX:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.playerX
            view.current_player = view.playerO
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.playerO
            view.current_player = view.playerX
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.playerX:
                content = 'X won!'
            elif winner == view.playerO:
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
    playerX = -1
    playerO = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.playerX
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
                return self.playerO
            elif value == -3:
                return self.playerX

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.playerO
            elif value == -3:
                return self.playerX

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.playerO
        elif diag == -3:
            return self.playerX

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.playerO
        elif diag == -3:
            return self.playerX

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


def setup(bot):
    bot.add_cog(Games(bot))
