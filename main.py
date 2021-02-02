import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.reactions = True

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	try:
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
	except KeyError:
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(message.guild.id)] = "~"
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
	except AttributeError:
		pass

client = commands.Bot(command_prefix=get_prefix, intents = intents)
client.remove_command('help')

# Shut Down Command
@client.command(name="shutdown")
@commands.guild_only()
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await client.logout()

@client.event
async def on_ready():
	print("________________________________________________________________________________________________________________________\nPictionary is on standby\n________________________________________________________________________________________________________________________")
	await client.change_presence(status=discord.Status.online, activity=discord.Game(f'Pictionary : {len(client.guilds)} guilds'))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

THIS_MA_TOKEN_HEHE = open('THIS_MA_TOKEN_HEHE.txt', 'r').readline()
client.run(THIS_MA_TOKEN_HEHE)
