from os import getenv
from dotenv import load_dotenv
from discord import Intents, Status, Game
from discord.ext import commands

from bot.constants import PREFIX
from bot.utils.extensions import EXTENSIONS

intents = Intents.default()
intents.reactions = True
intents.members = True

# Bot constructor
bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   status=Status.do_not_disturb, activity=Game("~help"))

# On ready event
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"{bot.user.name} is on standby")

for ext in EXTENSIONS:
    bot.load_extension(ext)

load_dotenv()
TOKEN = getenv('TOKEN')
bot.run(TOKEN)
