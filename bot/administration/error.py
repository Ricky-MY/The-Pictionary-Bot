import traceback
import sys

from discord import Embed
from discord import Color
from discord import errors
from discord.ext import commands
from discord import HTTPException

class ExceptionHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xC0C0C0
        self.error_color = Color.dark_red()

    '''Basic discord exception handler'''
    
    async def raise_norm(self, ctx, error):
        print(f'Ignoring exception in command {ctx.command}:')
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_usage(self, ctx):
        return f'{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}'

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'⚠️ {ctx.command} has been disabled.')

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'⚠️ {str(ctx.command).upper()} cannot be used in Private Messages.')
            except HTTPException:
                pass
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(title='⚠️ Unable to proceed...', description=f"{error.param} is a required parameter.", color=self.error_color)
            embed.set_footer(text=self.get_usage(ctx))
            await ctx.send(embed=embed)
        
        if isinstance(error, commands.BadArgument):
            embed = Embed(title='⚠️ Unable to proceed...', description=f"Incorrect details passed in.", color=self.error_color)
            embed.set_footer(text=self.get_usage(ctx))
            await ctx.send(embed=embed)

        else:
            if cog.qualified_name == 'Admin':
                if isinstance(error, commands.ExtensionNotFound):
                    await ctx.send("⚠️ Extension is not found.")
                elif isinstance(error, commands.ExtensionNotLoaded):
                    await ctx.send("⚠️ Extension is not loaded.")
                elif isinstance(error, commands.ExtensionAlreadyLoaded):
                    await ctx.send("⚠️ Extension has been already loaded.")
                else:
                    await self.raise_norm(ctx, error)

            elif cog.qualified_name == 'Pictionary':
                if isinstance(error, commands.BotMissingPermissions):
                    embed = Embed(title='⚠️ Permission needed!', description=f"Due to the latest update on the new multi-answering system. The bot now requires the `manage_messages` permission. Find out more [here](https://github.com/Ricky-MY/The-Pictionary-Bot/blob/main/src/game_files/pictionary.py).", color=self.error_color )
                    embed.add_field(name="Why?", value="The new rewarding system allows multiple people to score points according to how fast they answer. The bot is required to delete valid answers so that when one person gets the correct theme. It remains unexposed.")
                    embed.add_field(name="How?", value=f"• Create a new role named `Pictionary`\n• Give the role access to the `manage_messages` permission\n• Give {self.bot.user.mention} the role!",inline= True)
                    embed.set_image(url = 'https://i.gyazo.com/98f79a36e4145705917434c6942f7a99.png')
                    embed.set_footer(text=f'{ctx.prefix}updates | to find out about latest updates')
                    await ctx.send(embed=embed)
                else:
                    await self.raise_norm(ctx, error)
            else:
                await self.raise_norm(ctx, error)

        if isinstance(error, errors.Forbidden):
            embed = Embed(title='⚠️ Unable to proceed...', description=f"Required permission is missing.", color=self.error_color)
            embed.set_footer(text=self.get_usage(ctx))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ExceptionHandler(bot))
    print('Exception handler is loaded')

