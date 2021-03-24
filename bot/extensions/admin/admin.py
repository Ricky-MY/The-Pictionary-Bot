import asyncio
import aiohttp
import discord
import json

from discord.ext import commands

from bot.utils.checks import is_admin
from bot.constants import Colour


class Admin(commands.Cog):

    '''Administration and maintenance based commands and functions

    - Reload / load / unload
    - Pushing updates and threads to guild owners
    - Restarting / Shutting down the bot'''

    def __init__(self, bot):
        self.bot = bot
        self.color = Colour.BABY_PINK

    '''Prototypes ; Ignore the following code'''

    @commands.command(name="web", aliases=['wbt'])
    @commands.guild_only()
    @commands.check(is_admin)
    async def web_server_test(self, ctx):
        base = "http://127.0.0.1:5000/text"
        link = f"{ctx.channel.id}/{ctx.author.id}"
        await ctx.send("Please go to this website: "+base+link)
        await asyncio.sleep(10)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{base}/api/get/{ctx.channel.id}/{ctx.author.id}') as resp:
                if resp.status == 200:
                    if resp:
                        await ctx.send(await resp.text())
                    else:
                        print(resp)

    @commands.command(name="web2", aliases=['wbt2'])
    @commands.guild_only()
    @commands.check(is_admin)
    async def web_server_test2(self, ctx):
        base = "http://127.0.0.1:5000/draw"
        link = f"{ctx.channel.id}/{ctx.author.id}"
        await ctx.send("Please go to this website: "+base+link)
        await asyncio.sleep(10)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{base}/api/get/{ctx.channel.id}/{ctx.author.id}') as resp:
                if resp.status == 200:
                    if resp:
                        await ctx.send(await resp.text())
                    else:
                        print(resp)

    @commands.command(name="import_prefixes", aliases=['impre'])
    @commands.guild_only()
    @commands.check(is_admin)
    async def import_prefixes(self, ctx):
        with open("toimport.json", "r") as f:
            prefixes = json.load(f)

        for guild_id in prefixes.keys():
            async with PrefixHandler("bot/assets/minor.db") as cont:
                await cont.update_value("prefixes", {guild_id: prefixes[guild_id]})
        await ctx.send("Prefixes imported")

    '''Utility commands to provide administrator access on the bot'''

    @commands.command(name="guilds")
    @commands.guild_only()
    @commands.check(is_admin)
    async def guilds(self, ctx):
        guilds = [i.name for i in self.bot.guilds]
        text = '\n'.join(guilds)
        embed = discord.Embed(title="Guilds Joined",
                              description=f"{text}", colour=self.color)
        embed.set_footer(text=f'Total of {len(guilds)} guild(s) joined')
        await ctx.send(embed=embed)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.bot.guilds)} guilds'))

    @commands.command(name="members")
    @commands.guild_only()
    @commands.check(is_admin)
    async def members(self, ctx):
        count = 0
        for guild in self.bot.guilds:
            count += len(guild.members)
        await ctx.send(embed=discord.Embed(title="Amount of members play pictionary:", description=f"**{count}**", color=self.color))
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'with {count} members | ~help '))

    @commands.command(name='alter status', aliases=['as', 'changeStatus', 'chs', 'changestatus', 'change_status'])
    @commands.check(is_admin)
    async def alter_status(self, ctx, *, status):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'{status}'))
        await ctx.send(f"Status successfully changed into |{status}|")

    '''This is purely preferential, this piece of code or loop is used
	to update the bot status on how many servers it is currently invited into.'''

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.bot.guilds)} guilds'))
        except:
            pass


def setup(bot):
    bot.add_cog(Admin(bot))
    print('Admin.cog is loaded')
