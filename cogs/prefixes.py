import discord
from discord.ext import commands
import json

class Prefixes(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(guild.id)] = "~"
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		async for entry in guild.audit_logs(action= discord.AuditLogAction.bot_add):
				if entry.target == self.client.user:
					color = 0x9494FF
					embed = discord.Embed(title = "__# Notice__", description= "Hey there buddy! I've noticed that you invited me into your server, here are some commands you can do to start-up!",color = color)
					embed.add_field(name= '\nBrief Guide:', value = f'`~help`', inline = True)
					embed.add_field(name= '\nIn-depth Guide:', value = f'`~help guide`', inline = True)
					embed.add_field(name= '\nVisual tutorial:', value = f'`~help tutorial`', inline = True)
					embed.add_field(name= '\nPrefix Commands:', value = f'`~prefix` (Shows Current Prefix)\n`~prefix change <new_prefix>`(Changes Current Prefix)', inline = False)
					embed.set_footer(text='Have a wonderful time playing pictionary!')
					inviter = entry.user
					await inviter.send(embed=embed)
					return

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes.pop(str(guild.id))
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		
	# Prefix finding Command
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def prefix(self, ctx):
		color = 0x9494FF
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		embed=discord.Embed(title=f"Preset", description=f"CURRENT SERVER PREFIX : \n1. '`{prefixes[str(ctx.guild.id)]}`' \n2.{ctx.guild.me.mention}\nExecute `{prefixes[str(ctx.guild.id)]}prefix change <new_prefix>` command to change prefixes!", colour=color)
		await ctx.send(embed=embed)
	
	@prefix.command()
	@commands.guild_only()
	async def change(self, ctx, prefix):
		color = 0x9494FF
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = str(prefix)
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		embed=discord.Embed(title=f"Success!", description=f'PREFIX SUCCESSFULLY CHANGED INTO : `{prefix}`\nExecute `{prefix}prefix` command to check the local prefix anytime!', colour=color)
		await ctx.send(embed=embed)
		
def setup(client):
	client.add_cog(Prefixes(client))
	print('Prefixes.cog is loaded')
