from discord.ext import commands
from discord.ext.commands.context import Context

from bot.utils.checks import is_admin
from bot.utils.extensions import EXTENSIONS


class AdminIO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extension_state = []

    @commands.command(name="load", aliases=['ld'])
    @commands.check(is_admin)
    async def load_cog(self, ctx: Context, extension: str):
        """Loads a unloaded cog to the bot."""
        for ext in EXTENSIONS:
            if ext.split('.')[-1] == extension:
                self.bot.load_extension(ext)
                await ctx.message.add_reaction("☑️")
                return
        await ctx.message.add_reaction("❎")

    # Unload command
    @commands.command(name="unload", aliases=['ul'])
    @commands.check(is_admin)
    async def unload_cog(self, ctx: Context, extension: str):
        """Unloads an loaded cog to the bot."""
        for ext in EXTENSIONS:
            if ext.split('.')[-1] == extension:
                self.bot.unload_extension(ext)
                await ctx.message.add_reaction("☑️")
                return
        await ctx.message.add_reaction("❎")

    # Reload command
    @commands.command(name="reload", aliases=['rl'])
    @commands.check(is_admin)
    async def reload_cog(self, ctx: Context, extension: str):
        """
        Reloads a loaded cog to the bot.
        """
        for ext in EXTENSIONS:
            if ext.split('.')[-1] == extension:
                self.bot.reload_extension(ext)
                await ctx.message.add_reaction("☑️")
                return
        await ctx.message.add_reaction("❎")

    # Load and reload all {self.main_directory}

    @commands.command(name="restart", aliases=['rst', 'sync'])
    @commands.check(is_admin)
    async def restart(self, ctx: Context):
        """
        Reloads every cog connected to the bot.
        """
        for ext in EXTENSIONS:
            self.bot.reload_extension(ext)
        await ctx.message.add_reaction("☑️")


def setup(bot):
    """Loads AdminIO cog"""
    bot.add_cog(AdminIO(bot))
    print("IO.cog is loaded")
