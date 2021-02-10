from discord import Intents
from discord import Status
from discord import Game
from discord.ext import commands

from dotenv import load_dotenv
from bot.utilities.prefixes import get_prefix
from os import listdir
from os import getenv

intents = Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=get_prefix, status=Status.online, activity= Game(f'~help'), intents = intents)
bot.remove_command('help')

@bot.command(name="shutdown")
@commands.guild_only()
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await bot.logout()

@bot.event
async def on_ready():
	print("+------------------------+\n|Pictionary is on standby|\n+------------------------+")

parentdir = 'bot'
for filename in listdir(f'./{parentdir}'):
	if not filename.endswith('.py') and not filename.startswith('_') and not filename.startswith('.'):
		for subdir in listdir(f'./{parentdir}/{filename}/'):
			if subdir.endswith('.py') and not subdir.startswith('_') and not subdir.startswith('.'):
				bot.load_extension(f'{parentdir}.{filename}.{subdir[:-3]}')

load_dotenv()
token = getenv('TOKEN')
bot.run(token)