# manager.py - code by Rye

# This file will contain basic bot configuration commands
# that server mods and admins can use to customize their experience
import asyncio
import nextcord
from nextcord.ext import commands
from warehouse.classes import cGuild
from warehouse.classes.sector import Sector

button_styles = [nextcord.ButtonStyle.success,
                 nextcord.ButtonStyle.secondary,
                 nextcord.ButtonStyle.danger]


class ConfigButton(nextcord.ui.Button):
    def __init__(self, label, key, value):
        super().__init__(style=button_styles[value], label=label)
        self.key = key
        self.value = value

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.guild:
            if not interaction.permissions.manage_guild:
                await interaction.response.send_message('You must have `Manage Guild` permissions to interact!', ephemeral=True)
                return
            view: UpdateView = self.view
            self.value = 1 if self.value == 0 else 0
            view.values[self.key] = self.value
            self.style = button_styles[self.value]
            await interaction.response.edit_message(view=view)


class UpdateView(nextcord.ui.View):
    def __init__(self, pre_select: dict):
        super().__init__()
        self.values = {'mod': pre_select['mod'],
                       'modone': pre_select['modone'],
                       'levels': pre_select['levels']}
        self.legend = {'mod': 'Mod Features', 'modone': 'ModOne', 'levels': 'Levels'}
        self.end = False
        for k, v in self.values.items():
            self.add_item(ConfigButton(self.legend[k], k, v))

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.blurple, row=1)
    async def confirm_config(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        button.label = 'Confirmed!'
        await interaction.response.edit_message(view=self)
        self.stop()


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def update(self, ctx):
        """Enables or disables bot features for the server"""
        cg: cGuild
        item: Sector
        await ctx.message.delete()
        cg = self.bot.get_cguild(int(ctx.guild.id))

        pre_select = {}
        for item in cg.sectors:
            pre_select[item.key] = item.stat
        view = UpdateView(pre_select)
        msg = await ctx.send(f"**Bot Configuration**\n\n"
                             f"** - Mod Features:** Allows the bot to run moderation commands\n"
                             f"** - ModOne:** The Advanced Auto-Mod features\n"
                             f"** - Levels:** The leveling system, which ranks users based on activity.", view=view)
        await view.wait()
        for item in cg.sectors:
            item.stat = view.values[item.key]
        config = await ctx.send(f"```Config Saved!\n"
                                f" - Mod Features: {'Enabled' if view.values['mod'] == 0 else 'Disabled'}\n"
                                f" - ModOne Bot: {'Enabled' if view.values['modone'] == 0 else 'Disabled'}\n"
                                f" - Levels: {'Enabled' if view.values['levels'] == 0 else 'Disabled'}```")
        await msg.delete()
        await asyncio.sleep(5)
        await config.delete()

    @commands.command()
    @commands.is_owner()
    async def features(self, ctx):
        cg = self.bot.get_cguild(ctx.guild.id)
        msg = await ctx.send(cg.get_feat())
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()


def setup(bot):
    bot.add_cog(Manager(bot))
