# listen.py - code by Rye

# This file will contain the discord event listeners
# and the response the bot will have to them
from nextcord.ext import commands
from runtime import SnowBot
from warehouse.classes import cGuild
import nextcord


class Execution(commands.Cog):
    def __init__(self, bot: SnowBot):
        self.bot: SnowBot = bot
        self.dba = self.bot.dba
        self.__status = 'and Listening'
        self.guild_join_msg = '***HEWWO?!? :sparkles:***\nI am Kyrie... yeah that\'s it. :D\n\n' \
                              'Oh yeah! I enabled some default settings, and I also set this channel' \
                              ' to be my channel to send important messages! You can check the "sectors"' \
                              ' enabled by default by doing `.guild_feat`.'

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot: SnowBot
        print(f'Logged in as [{self.bot.user}] successfully.')
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching,
                                                                  name=str(self.__status)),
                                       status=nextcord.Status.online)
        for guild in self.bot.guilds:
            self.bot.cguilds.append(cGuild(guild.id, guild.name, self.dba))

    @commands.command()
    @commands.is_owner()
    async def features(self, ctx):
        cg = self.bot.get_cguild(ctx.guild.id)
        await ctx.send(cg.get_feat())
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Execution(bot))
