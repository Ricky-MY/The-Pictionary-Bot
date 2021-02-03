import discord
import os
import json
from discord.ext import commands, tasks

class Admin(commands.Cog):
	
	'''Administration and maintenance based commands and functions
	
	- Reload / load / unload
	- Pushing updates and threads to guild owners
	- Restarting / Shutting down the bot'''

	def __init__(self, client):
		self.client = client
		self.color = 0x9494FF
		self.change_status.start()

	'''This is a custom ID check designed to disapprove any 
	alien acceses'''

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

	'''Pushing and publishing updates and threads to 
	guild owners, this part can be mostly ignored'''

	@commands.command(name = "restart subslist", aliases=['rstl'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def restart_subscriptions(self, ctx):
		guilds = self.client.guilds
		with open('cogs/subscriptions.json', 'r') as f:
			data = json.load(f)
		for guild in guilds:
			data[str(guild.id)] = guild.owner_id
		with open('cogs/subscriptions.json', 'w') as f:
			json.dump(data, f)
		
	@commands.command(name = "push update", aliases = ['upt'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def push_updates(self, ctx):
		guilds = self.client.guilds
		with open('cogs/subscriptions.json', 'r') as f:
			people_subscribed = json.load(f)
		sent = []
		embed = discord.Embed(title = "__# Notice__", description= "description")
		for key in people_subscribed.keys():
			if int(key) in [i.id for i in guilds]:
				if people_subscribed[key] not in sent:
					sent.append(people_subscribed[key])
					member = self.client.get_guild(int(key)).get_member(people_subscribed[key])
					message = await member.send(embed = embed)
					await message.add_reaction('🙅‍♂️')
			elif int(key) not in [i.id for i in guilds]:
				people_subscribed.pop(key)
		with open('cogs/subscriptions.json', 'w') as f:
			json.dump(people_subscribed, f)

	'''Utility commands to provide administrator access on the bot'''

	# Guilds Checker
	@commands.command(name="guilds")
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		count = 0
		guilds = [i.name for i in self.client.guilds]
		text = '\n'.join(guilds)
		embed = discord.Embed(title="Guilds Joined", description = f"{text}", colour=self.color)
		embed.set_footer(text=f'Total of {len(guilds)} guild(s) joined')
		await ctx.send(embed=embed)

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cogs(self, ctx, extension):
		self.client.load_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
							   color=self.color)
		await ctx.send(embed=embed)

	# Unload command
	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cogs(self, ctx, extension):
		
		self.client.unload_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is unloaded.',
								color=self.color)
		await ctx.send(embed=embed)

	# Reload command
	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cogs(self, ctx, extension):
		self.client.reload_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
									color=self.color)
		await ctx.send(embed=embed)
	
	# Load and reload all cogs
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.client.unload_extension(f'cogs.{filename[:-3]}')
				self.client.load_extension(f'cogs.{filename[:-3]}')
		await ctx.send(embed=discord.Embed(title='Success!', description=f'Bot has restarted', color=self.color))

	'''This is purely preferential, this piece of code or loop is used 
	to update the bot status on how many servers it is currently invited into.'''
	
	@tasks.loop(hours = 2)
	async def change_status(self):
		try:
			await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.client.guilds)} guilds'))
		except:
			pass

def setup(client):
	client.add_cog(Admin(client))
	print('Admin.cog is loaded')
