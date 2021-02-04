import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.reactions = True

main_directory = 'src'

def get_prefix(bot, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	try:
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
	except KeyError:
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(message.guild.id)] = "~"
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
	except AttributeError:
		pass

bot = commands.Bot(command_prefix=get_prefix, status=discord.Status.online, activity=discord.Game(f'~help'), intents = intents)
bot.remove_command('help')

@bot.command(name="shutdown")
@commands.guild_only()
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await bot.logout()

@bot.event
async def on_ready():
	print("________________________________________________________________________________________________________________________\nPictionary is on standby\n________________________________________________________________________________________________________________________")

to_reload = []
for filename in os.listdir(f'./{main_directory}'):
	if filename.endswith('.py') and not filename.startswith('_'):
		bot.load_extension(f'{main_directory}.{filename[:-3]}')
	elif not filename.endswith('.py') and not filename.endswith('.json') and not filename.startswith('_'):
		to_reload.append(filename)
for file in to_reload:
	for filename in os.listdir(f'./{main_directory}/{file}'):
		if filename.endswith('.py') and not filename.startswith('_'):
			bot.load_extension(f'{main_directory}.{file}.{filename[:-3]}')

THIS_MA_TOKEN_HEHE = open('THIS_MA_TOKEN_HEHE.txt', 'r').readline()
bot.run(THIS_MA_TOKEN_HEHE)
