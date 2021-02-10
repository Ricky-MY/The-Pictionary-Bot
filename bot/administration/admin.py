import discord
from os import listdir
import json
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded

class Admin(commands.Cog):
	
	'''Administration and maintenance based commands and functions
	
	- Reload / load / unload
	- Pushing updates and threads to guild owners
	- Restarting / Shutting down the bot'''

	def __init__(self, bot):
		self.bot = bot
		self.color = 0x87ceeb
		self.main_directory = 'bot'

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

	'''Pushing and publishing updates and threads to 
	guild owners, this part can be mostly ignored'''

	@commands.command(name = "restart subslist", aliases=['rstl'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def restart_subscriptions(self, ctx):
		guilds = self.bot.guilds
		with open(f'{self.main_directory}/subscriptions.json', 'r') as f:
			data = json.load(f)
		for guild in guilds:
			data[str(guild.id)] = guild.owner_id
		with open(f'{self.main_directory}/subscriptions.json', 'w') as f:
			json.dump(data, f)
		
	@commands.command(name = "push update", aliases = ['upt'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def push_updates(self, ctx):
		guilds = self.bot.guilds
		with open(f'{self.main_directory}/subscriptions.json', 'r') as f:
			people_subscribed = json.load(f)
		sent = []
		embed = discord.Embed(title = "__# Notice__", description= "description")
		for key in people_subscribed.keys():
			if int(key) in [i.id for i in guilds]:
				if people_subscribed[key] not in sent:
					sent.append(people_subscribed[key])
					member = self.bot.get_guild(int(key)).get_member(people_subscribed[key])
					message = await member.send(embed = embed)
					await message.add_reaction('🙅‍♂️')
			elif int(key) not in [i.id for i in guilds]:
				people_subscribed.pop(key)
		with open(f'{self.main_directory}/subscriptions.json', 'w') as f:
			json.dump(people_subscribed, f)

	'''Utility commands to provide administrator access on the bot'''

	# Guilds Checker
	@commands.command(name="guilds")
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		guilds = [i.name for i in self.bot.guilds]
		text = '\n'.join(guilds)
		embed = discord.Embed(title="Guilds Joined", description = f"{text}", colour=self.color)
		embed.set_footer(text=f'Total of {len(guilds)} guild(s) joined')
		await ctx.send(embed=embed)
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.bot.guilds)} guilds'))

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cog(self, ctx, extension):
		self.bot.load_extension(f'{self.main_directory}.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
							   color=self.color)
		await ctx.send(embed=embed)

	# Unload command
	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cog(self, ctx, extension):
		
		self.bot.unload_extension(f'{self.main_directory}.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is unloaded.',
								color=self.color)
		await ctx.send(embed=embed)

	# Reload command
	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cog(self, ctx, extension):
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
										color=self.color)
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.reload_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.send(embed=embed)
				return
		raise ExtensionNotFound(extension)

	# Load and reload all {self.main_directory}
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		for subdir in listdir(f'./{self.main_directory}/'):
			for files in listdir(f'./{self.main_directory}/{subdir}/'):
				if files.endswith('.py') and not files.startswith('_'):
					self.bot.reload_extension(f'{self.main_directory}.{subdir}.{files[:-3]}')
		await ctx.send(embed=discord.Embed(title='Success!', description=f'Bot has restarted', color=self.color))

	@commands.command(name='alter status', aliases = ['as', 'changeStatus', 'chs', 'changestatus', 'change_status'])
	@commands.check(botAdminCheck)
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
