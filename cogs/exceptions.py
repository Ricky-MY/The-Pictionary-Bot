import discord
import traceback
import sys
from discord.ext import commands
from discord import errors

async def raise_norm(ctx, error):
    print(f'Ignoring exception in command {ctx.command}:')
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def get_usage(ctx):
    return f'{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}'

class ExceptionHandler(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.color = 0xC0C0C0
        self.error_color = discord.Color.dark_red()

    '''Basic discord exception handler'''

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
            except discord.HTTPException:
                pass
        
        else:
            if cog.qualified_name == 'Admin':
                if isinstance(error, commands.ExtensionNotFound):
                    await ctx.send("⚠️ Extension is not found.")
                elif isinstance(error, commands.ExtensionNotLoaded):
                    await ctx.send("⚠️ Extension is not loaded.")
                elif isinstance(error, commands.ExtensionAlreadyLoaded):
                    await ctx.send("⚠️ Extension has been already loaded.")
                else:
                    await raise_norm(ctx, error)

            elif cog.qualified_name == 'Pictionary':
                if isinstance(error, commands.BadArgument):
                    embed = discord.Embed(title='⚠️ Unable to proceed...', description=f"Incorrect details passed in. Make sure to include the rounds and mode.", color=self.error_color)
                    embed.set_footer(text=get_usage(ctx))
                    await ctx.send(embed=embed)
                elif isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(title='⚠️ Unable to proceed...', description=f"Mandatory arguments are missing, make sure to add them.", color=self.error_color)
                    embed.set_footer(text=get_usage(ctx))
                    await ctx.send(embed=embed)
                else:
                    await raise_norm(ctx, error)
            else:
                await raise_norm(ctx, error)

        if isinstance(error, errors.Forbidden):
            embed = discord.Embed(title='⚠️ Unable to proceed...', description=f"Required permission is missing.", color=self.error_color)
            embed.set_footer(text=get_usage(ctx))
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(ExceptionHandler(client))
    print('Exception handler is loaded')

