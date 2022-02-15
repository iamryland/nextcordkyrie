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
        super().__init__(style=button_styles[value], label=label, row=0)
        self.key = key
        self.value = value

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.guild:
            if not interaction.permissions.manage_guild:
                await interaction.response.send_message('You must have `Manage Server` permissions to interact!', ephemeral=True)
                return
            view: UpdateView = self.view
            self.value = 1 if self.value == 0 else 0
            view.values[self.key] = self.value
            self.style = button_styles[self.value]
            await interaction.response.edit_message(view=view)


class UpdateView(nextcord.ui.View):
    def __init__(self, values: dict, legend: dict):
        self.values = values
        self.legend = legend
        self.end = False
        super().__init__()
        for k, v in self.values.items():
            self.add_item(ConfigButton(self.legend[k], k, v))

    @nextcord.ui.button(label='Save', style=nextcord.ButtonStyle.blurple)
    async def confirm_config(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        button.label = 'Saved!'
        await interaction.response.edit_message(view=self)
        self.stop()


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx, *, sub_command=None):
        """Enables or disables bot features for the server"""
        cg: cGuild
        item: Sector
        await ctx.message.delete()
        cg = self.bot.get_cguild(int(ctx.guild.id))

        keys = []
        for item in cg.sectors:
            keys.append(item.key)

        if sub_command is None:
            pre_select = {}
            top_config = {}
            description = ''
            for item in cg.sectors:
                top_config[item.key] = str(item)
                pre_select[item.key] = item.stat
                description += f"** - {item}:** {item.__doc__}\n"
            description += f"\nClick or Tap on the buttons to Enable (Green) or Disable (Grey) features."\
                           f"\nOnce finished, press ` Save ` to save the configuration."
            view = UpdateView(pre_select, top_config)
            embed = nextcord.Embed(title='Bot Configuration', description=description, color=nextcord.Color.dark_red())
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            message = ''
            for item in cg.sectors:
                item.stat = view.values[item.key]
                message += f" - {item}: {'Enabled' if view.values[item.key] == 0 else 'Disabled'}\n"
            config = await ctx.send(f"```Config Saved!\n{message}```")
            await msg.delete(delay=1)
            await config.delete(delay=5)
        if sub_command in keys:
            sector = None
            string = ''
            options = {}
            # sub_values = {}
            # sub_legend = {}
            for item in cg.sectors:
                if item.key == sub_command:
                    sector = item
                    for val in dir(sector):
                        if not val.startswith('_') and val not in ['key', 'gid', 'stat', 'docs', 'values']:
                            options[val] = sector.values[val].doc
                            # sub_values[val] = sector.values[val].value
                    break
                else:
                    continue
            for k, v in options.items():
                # sub_legend[k] = k
                string += f'\n - **{k}:** {v}'
            # view = UpdateView(sub_values, sub_legend)
            await ctx.send(embed=nextcord.Embed(title=f'{sector} Configuration',
                                                description=string,
                                                color=nextcord.Color.dark_red()))

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
