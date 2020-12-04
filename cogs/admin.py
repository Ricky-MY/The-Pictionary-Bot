import discord
import json
import os
from discord.ext import commands, tasks


class Admin(commands.Cog):

	def __init__(self, client):
		self.client = client

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

	# Guilds Checker
	@commands.command(name="guilds")
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		color = 0x9494FF
		count = 0
		inGuilds = self.client.guilds
		embed = discord.Embed(title="Guilds Joined", colour=color)
		for guild in inGuilds:
			count = count + 1
			embed.add_field(name=count, value=f'`{guild}`', inline = False)
		embed.set_footer(text=f'Total of {count} guild(s) joined')
		await ctx.send(embed=embed)

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cogs(self, ctx, extension):
		color = 0x9494FF
		self.client.load_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
							   color=color)
		await ctx.send(embed=embed)

	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cogs(self, ctx, extension):
		color = 0x9494FF
		self.client.unload_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is unloaded.',
								color=color)
		await ctx.send(embed=embed)

	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cogs(self, ctx, extension):
		color = 0x9494FF
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
									color=color)
		try:
			self.client.reload_extension(f'cogs.{extension}')
		except:
			self.client.load_extension(f'cogs.{extension}')
		await ctx.send(embed=embed)
			
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		color = 0x9494FF
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.client.unload_extension(f'cogs.{filename[:-3]}')
				self.client.load_extension(f'cogs.{filename[:-3]}')
				embed = discord.Embed(title='Success!', description=f'{filename[:-3]} is reloaded.',color=color)
				await ctx.send(embed=embed)

	@tasks.loop(hours = 1)
	async def change_status(self):
		try:
			await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'on {len(self.client.guilds)} servers!'))
		except:
			pass
		guild = self.client.get_guild(702714944558202933)
		channel = guild.get_channel(768796445364715551)
		await channel.edit(name=f'Pictionary : {len(self.client.guilds)} guilds')

def setup(client):
	client.add_cog(Admin(client))
	print('Admin.cog is loaded')
