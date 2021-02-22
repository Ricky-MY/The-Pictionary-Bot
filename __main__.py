import yaml

from discord.ext import commands
from discord import Intents, Game, Status

from dotenv import load_dotenv
from os import listdir, getenv

from bot.utilities.prefixes import get_prefix
from bot.administration.admin import Admin

intents = Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=get_prefix, status=Status.online, activity= Game(f'~help'), intents = intents)
bot.remove_command('help')

with open("config.yml", "r") as file:
    configs = yaml.load(file, Loader=yaml.SafeLoader)

parentdir = configs["dirLayout"]["d"]
for filename in listdir(f'./{parentdir}'):
	if not filename.endswith('.py') and not filename.startswith('_') and not filename.startswith('.'):
		for subdir in listdir(f'./{parentdir}/{filename}/'):
			if subdir.endswith('.py') and not subdir.startswith('_') and not subdir.startswith('.'):
				bot.load_extension(f'{parentdir}.{filename}.{subdir[:-3]}')

@bot.event
async def on_ready():
	print("+------------------------+\n|Pictionary is on standby|\n+------------------------+")
	
@commands.check(Admin.botAdminCheck)
@commands.guild_only()
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await bot.logout()

load_dotenv()
bot.run(getenv('TOKEN'))