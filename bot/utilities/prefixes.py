import discord
from discord.ext import commands
import json

prefixes_directory = 'bot/resources/prefixes.json'


def get_prefix(bot, message):
    with open(prefixes_directory, 'r') as f:
        prefixes = json.load(f)
    try:
        return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
    except KeyError:
        with open(prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        prefixes[str(message.guild.id)] = "~"
        with open(prefixes_directory, 'w') as f:
            json.dump(prefixes, f, indent=4)
        return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
    except AttributeError:
        return ['~']

class Prefixes(commands.Cog):

    '''Basic class to handle custom prefixes'''

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x87ceeb
        self.prefixes_directory = prefixes_directory

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        return
        with open(self.prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "~"
        with open(self.prefixes_directory, 'w') as f:
            json.dump(prefixes, f, indent=4)
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
        with open(self.prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open(self.prefixes_directory, 'w') as f:
            json.dump(prefixes, f, indent=4)

    # Prefix finding Command
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx):
        with open(self.prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(
            title=f"Preset", description=f"CURRENT SERVER PREFIX : \n1. '`{prefixes[str(ctx.guild.id)]}`' \n2.{ctx.guild.me.mention}\nExecute `{prefixes[str(ctx.guild.id)]}prefix change <new_prefix>` command to change prefixes!", colour=self.color)
        await ctx.send(embed=embed)

    @prefix.command()
    @commands.guild_only()
    async def change(self, ctx, prefix):
        with open(self.prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = str(prefix)
        with open(self.prefixes_directory, 'w') as f:
            json.dump(prefixes, f, indent=4)
        embed = discord.Embed(
            title=f"Success!", description=f'PREFIX SUCCESSFULLY CHANGED INTO : `{prefix}`\nExecute `{prefix}prefix` command to check the local prefix anytime!', colour=self.color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Prefixes(bot))
    print('Prefixes.cog is loaded')
