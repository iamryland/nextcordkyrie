# runtime.py - code by Rye

# This file will do the following:
# - Connect the bot to discord
# - Access the configured guild prefix
# - Load and unload other bot functionality
# - Allow Dev Access to be authorized through discord
import functools
import json
import asyncio
from os import path

import nextcord.ext.commands
from nextcord.ext import commands


class SnowBot(commands.Bot):
    def __init__(self):
        self.retrieve_prefix = functools.partial(self.get_bot_prefix)
        super().__init__(command_prefix=self.retrieve_prefix)
        self.__status: str = 'and Listening'
        self.wh = 'warehouse'
        self.support: Support = Support()
        self.preload = self.support.preload()
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        # self.dba
        # self.cguilds

    def startup(self):
        self.add_cog(DevLoader(self))
        for item in self.preload:
            try:
                self.load_extension(item)
            except nextcord.ext.commands.ExtensionNotFound:
                pass

        self.loop = asyncio.new_event_loop()

        async def runner(self_):
            try:
                await self.start(self_.support.get_token())
            finally:
                if not self.is_closed():
                    await self.close()

        def stop_loop_on_completion(stop_loop):
            self.loop.stop()
        future = asyncio.ensure_future(runner(self), loop=self.loop)
        future.add_done_callback(stop_loop_on_completion)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Exiting Event Loop")

    def get_bot_prefix(self, bot, message):
        if not message.guild:
            return '.'
        else:
            with open(f'{self.wh}/database/master.json') as f:
                data = json.load(f)
                if str(message.guild.id) in data.keys():
                    record = data[f'{message.guild.id}']
                else:
                    record = '.'
            pre = [record, f'{record} ']
            return commands.when_mentioned_or(pre[0], pre[1])(bot, message)


class Support:
    @staticmethod
    # Stack Overflow provided this code, I did not create it, I did tweak it though
    def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} <|{bar}|> {percent}% {suffix}', end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()

    @staticmethod
    def preload():
        with open('warehouse/config.json') as f:
            data = json.load(f)
        check = data['config']['check']
        final = []
        item: str
        for item in check['yes']:
            if path.isfile(f'{item.replace(".", "/")}.py'):
                final.append(item)
            else:
                print(f'ERROR - {item}: ' + data['errors'][item])
                choice = input('Continue? (Y/N): ')
                print(choice)
                if choice.startswith('y'):
                    continue
                elif choice.startswith('n'):
                    exit()
        for item in check['no']:
            if path.isfile(f'{item.replace(".", "/")}.py'):
                final.append(item)
            else:
                continue
        return final

    @staticmethod
    def get_token():
        with open('warehouse/config.json') as f:
            data = json.load(f)
            token = data['key']
        return token


class DevLoader(commands.Cog, command_attrs=dict(hidden=True)):
    """Hidden"""
    def __init__(self, bot):
        self.bot = bot
        self.location = 'driver.dev'
        self.toggle = False

    @commands.command()
    @commands.is_owner()
    async def debug(self, ctx):
        """The Dev Tools :eyes:"""
        if self.toggle is True:
            self.bot.unload_extension(self.location)
            msg = await ctx.send('`Successfully Disabled the Developer Tools.`')
            self.toggle = False
        else:
            self.bot.load_extension(self.location)
            msg = await ctx.send('`Successfully Enabled the Developer Tools.`')
            self.toggle = True
        await ctx.message.delete()
        await asyncio.sleep(3)
        await msg.delete()

    @commands.command()
    @commands.is_owner()
    async def debugs(self, ctx):
        """Show's whether the Dev module is loaded"""
        await ctx.message.delete()
        msg = await ctx.send('`Current Dev status: {}`'.format('Enabled' if self.toggle else 'Disabled'))
        await asyncio.sleep(3)
        await msg.delete()

    @commands.command()
    @commands.is_owner()
    async def debuggers(self, ctx):
        """Reloads the Dev module"""
        self.bot.reload_extension('driver.elevate')
        await ctx.message.delete()
        msg = await ctx.send('`Reloaded the Dev Tools module`')
        await asyncio.sleep(5)
        await msg.delete()


# Starts the bot :D
discordBot = SnowBot()
discordBot.startup()
