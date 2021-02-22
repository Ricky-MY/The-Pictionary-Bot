import discord
import yaml

from discord.ext import commands

from bot.utilities._frameworks.databases import PrefixHandler, sync_handle_prefixes

def get_prefix(bot, message):
    if message.guild is None:
        return "~"
    elif message.guild is not None:
        with sync_handle_prefixes("bot/resources/minor.db") as cont:
            return commands.when_mentioned_or(cont.get_value("prefixes", message.guild.id))(bot, message)

async def get_real_prefix(guild_id):
    directory = "bot/resources/minor.db"
    async with PrefixHandler(directory) as cont:
        return await cont.get_value("prefixes", guild_id)

class Prefixes(commands.Cog):
    '''Basic class to handle custom prefixes'''

    def __init__(self, bot):
        self.bot = bot

        with open("config.yml", "r") as file:
            configs = yaml.load(file, Loader=yaml.SafeLoader)
        self.color = configs["asthetics"]["blushColor"]

        self.minor_dir = configs["moderation"]["minor"]
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with PrefixHandler(self.directory) as cont:
            await cont.update_value("prefixes", {guild.id: "~"})
        return
        async for entry in guild.audit_logs(action=discord.AuditLogAction.bot_add):
            if entry.target == self.bot.user:
                embed = discord.Embed(
                    title="__# Notice__", description="Hey there buddy! I've noticed that you invited me into your server, here are some commands you can do to start-up!", color=self.color)
                fields = (('\nBrief Guide:', f'`~help`', True),
                          ('\nIn-depth Guide:', f'`~help guide`', True),
                          ('\nVisual tutorial:', f'`~help tutorial`', True),
                          ('\nPrefix Commands:', f'`~prefix` (Shows Current Prefix)\n`~prefix change <new_prefix>`(Changes Current Prefix)', False))
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                embed.set_footer(
                    text='Have a wonderful time playing pictionary!')
                inviter = entry.user
                await inviter.send(embed=embed)
                return

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with PrefixHandler(self.minor_dir) as ctx:
            await ctx.delete_value("prefixes", guild.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if '<@!769198596339269643>' == message.content:
            await self.prefix(message)

    # Prefix finding Command
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx):
        prefix = await get_real_prefix(ctx.guild.id)
        embed = discord.Embed(
            title=f"Preset", description=f"CURRENT SERVER PREFIX : \n1. '`{prefix}`' \n2.{ctx.guild.me.mention}\nExecute `{prefix}prefix change <new_prefix>` command to change prefixes!", colour=self.color)
        await ctx.channel.send(embed=embed)

    @prefix.command()
    @commands.guild_only()
    async def change(self, ctx, prefix):
        async with PrefixHandler(self.minor_dir) as cont:
            await cont.update_value("prefixes", {ctx.guild.id: prefix})
        embed = discord.Embed(
            title=f"Success!", description=f'PREFIX SUCCESSFULLY CHANGED INTO : `{prefix}`\nExecute `{prefix}prefix` command to check the local prefix anytime!', colour=self.color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Prefixes(bot))
    print('Prefixes.cog is loaded')
