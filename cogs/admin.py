import discord
import os
import json
from discord.ext import commands, tasks

class Admin(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.color = 0x9494FF

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

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
		embed = discord.Embed(title = "__# Notice__", description= "Hey there, recently we've recieved a lot of feedbacks on the poor lobbying system and we've worked on it now to work a tad lot better!",color = self.color)
		embed.add_field(name= '\nWhats new?:', value = f"```- Better ready up process\nYou can now ready up for lobbies by reacting to the message with the reaction it says.\n- Game per channel\nPictionary games are now restricted per channel to avoid blockage, although it's allowed and possible to play multiple games on different channels.```", inline = False)
		embed.add_field(name= '\nTip:', value = f'`To unsubscribe from this mailing list as a guild owner, please react to this with 🙅‍♂️`', inline = True)
		embed.add_field(name= '\nPictionary code base:', value = f'https://github.com/Ricky-MY/The-Pictionary-Bot', inline = True)
		embed.add_field(name= '\nPrefix Commands:', value = f'`~prefix` (Shows Current Prefix)\n`~prefix change <new_prefix>`(Changes Current Prefix)', inline = False)
		embed.add_field(name= '\u200b',value= f'[Join our support server and have a say in what we do next!](https://discord.gg/UmnzdPgn6g)', inline = False)
		embed.set_footer(text='Have a wonderful time playing pictionary!')
		for key in people_subscribed.keys():
			if int(key) in [i.id for i in guilds]:
				if people_subscribed[key] not in sent:
					sent.append(people_subscribed[key])
					member = self.client.get_guild(int(key)).get_member(people_subscribed[key])
					message = await member.send(embed = embed)
					message.add_reaction('🙅‍♂️')
			elif int(key) not in [i.id for i in guilds]:
				people_subscribed.pop(key)
		with open('cogs/subscriptions.json', 'w') as f:
			json.dump(people_subscribed, f)

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

	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cogs(self, ctx, extension):
		
		self.client.unload_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is unloaded.',
								color=self.color)
		await ctx.send(embed=embed)

	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cogs(self, ctx, extension):
		self.client.reload_extension(f'cogs.{extension}')
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
									color=self.color)
		await ctx.send(embed=embed)
			
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.client.unload_extension(f'cogs.{filename[:-3]}')
				self.client.load_extension(f'cogs.{filename[:-3]}')
		await ctx.send(embed=discord.Embed(title='Success!', description=f'Bot has restarted', color=self.color))

	@tasks.loop(hours = 2)
	async def change_status(self):
		try:
			await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.client.guilds)} guilds'))
		except:
			pass

def setup(client):
	client.add_cog(Admin(client))
	print('Admin.cog is loaded')
