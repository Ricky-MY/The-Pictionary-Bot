import discord
from discord.ext import commands, tasks
import asyncio
import random

class Pictionary(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.group(invoke_without_command = True)
	@commands.guild_only()
	async def start(self, ctx):
		await ctx.send('Please choose `normal/custom`!')

	@start.command()
	@commands.guild_only()
	async def normal(self, ctx, rounds : int = 1 , members : commands.Greedy[discord.Member] = None):
		if len(members) is None:
			await ctx.send("You didn't specify any participants, please try again.")
			return
		if len(members) < 2:
			await ctx.send("You need more than 2 members to start a game.")
			return
		elif len(members) > 30:
			await ctx.send("You have way too many members to start a game!")
			return

		themes = ['Mom', 'Donald Trump', 'Joe Biden', 'apple', 'orange', 'merman', 'superman', 'thor', 'Timer', 'Paper', 'Pencils', 'Index cards', 'Dice', 'Angry', 'Fireworks', 'Pumpkin', 'Baby', 'Flower', 'Rainbow', 'Beard', 'Flying saucer', 'Recycle', 'Bible', 'Giraffe', 'Sand castle', 'Glasses', 'Snowflake', 'Book', 'High heel', 'Stairs', 'Bucket', 'Ice cream cone', 'Starfish', 'Bumble bee', 'Igloo', 'Strawberry', 'Butterfly', 'Lady bug', 'Sun', 'Camera', 'Lamp', 'Tire', 'Cat', 'Lion', 'Toast', 'Church', 'Mailbox', 'Toothbrush', 'Crayon', 'Night', 'Toothpaste', 'Dolphin', 'Nose', 'Truck', 'Egg', 'Olympics', 'Volleyball', 'Eiffel Tower', 'Peanut', 'Abraham Lincoln', 'Kiss', 'Pigtails', 'Brain', 'Kitten', 'Playground', 'Bubble bath', 'Kiwi', 'Pumpkin pie', 'Buckle', 'Lipstick', 'Raindrop', 'Bus', 'Lobster', 'Robot', 'Car accident', 'Lollipop', 'Sand castle', 'Castle', 'Magnet', 'Slipper', 'Chain saw', 'Megaphone', 'Snowball', 'Circus tent', 'Mermaid', 'Sprinkler', 'Computer', 'Minivan', 'Statue of Liberty', 'Crib', 'Mount Rushmore', 'Tadpole', 'Dragon', 'Music', 'Teepee', 'Dumbbell', 'North pole', 'Telescope', 'Eel', 'Nurse', 'Train', 'Ferris wheel', 'Owl', 'Tricycle', 'Flag', 'Pacifier', 'Tuk Tuk', 'Junk mail', 'Piano']
		channel = ctx.channel
		color = 0x9494FF
		DRAWING_TIME = 60
		GUESSING_TIME = 70
		STARTING_SCORE = 0
		BASIC_SCORE = 10
		scores = {}
		lobby_init = await ctx.send(embed=discord.Embed(title='__**# Lobby**__', description = f'> Starting in 3 seconds...\n> \n> Guess Time = 70 seconds\n> \n> Drawing Time = 60 seconds\n> \n> No of Participants = {len(members)}', color = color))
		await asyncio.sleep(3)

		for member in members:
			scores[member.mention] = STARTING_SCORE
			try: 
				await lobby_init.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'> {member.mention} Please reply ready.\n> \n> Guess Time = 70 seconds\n> \n> Drawing Time = 60 seconds\n> \n> No of Participants = {len(members)}', color = color))
				msg = await self.client.wait_for('message', check=lambda message : message.content.lower() == 'ready' and message.channel == channel and message.author == member, timeout = 30)
			except asyncio.TimeoutError:
				await lobby_init.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'{member.mention} is inactive - Lobby failed to start.', color = discord.Color.dark_red()))
				return

		main_embed = await channel.send(embed=discord.Embed(title = "All players ready.", color = color))
		await asyncio.sleep(0.5)
		to_be_deleted = await channel.send('> Game is starting in `5` seconds....')
		await asyncio.sleep(5)
		await to_be_deleted.delete()
		await main_embed.edit(embed = discord.Embed(title = "GAME HAS STARTED", description = 'Round : 1', color= color))

		for i in range(0, rounds):
			if i > 0:
				await channel.send(embed = discord.Embed(title = "Game Update", description = f'Round : {i+1}', color= color))
			for member in members:
				theme = random.choice(themes)
				words_of_theme = list(theme)
				blank_list = []
				for i in words_of_theme:
					if i == ' ':
						blank_list.append('  ')
					else:
						blank_list.append(' _ ')
				blank = ''.join(blank_list)
				
				await channel.send(f"> Its {member.mention}'s turn, lets wait for them to submit their drawing!")
				await member.send(embed = discord.Embed(title=f'Eyo, please draw "{theme}" in MS paint and send me a picture of it.', description='You only have 60 seconds so get it together son.', color = color))
				try:
					msg = await self.client.wait_for('message', check=lambda message : len(message.attachments)> 0 and message.guild is None and message.author == member, timeout = DRAWING_TIME)
				except asyncio.TimeoutError:
					await member.send(f'60 seconds has elapsed and still no drawings, what a shame son.')
					await channel.send(f"Son's lackin, too slow and couldn't submit in time, -{BASIC_SCORE} from your points {member.mention}")
					scores[member.mention] -= BASIC_SCORE
				else:
					embed = discord.Embed(title=f'Drawn by {member.display_name}', description = f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`', color = color)
					embed.set_image(url=msg.attachments[0].url)
					await channel.send(embed=embed)
					try: 
						msg = await self.client.wait_for('message', check=lambda message : message.content.lower() == theme.lower() and message.channel == channel and message.author in members and message.author != member, timeout = GUESSING_TIME  )
					except asyncio.TimeoutError:
						await ctx.send(f"You all couldn't answer in time, WHICH, surprised absolutely no one. The theme was `{theme}`.")
					else:
						await ctx.send(f'{msg.author.mention} guessed it correctly. Not bad considering the brain cells count.')
						scores[msg.author.mention] += BASIC_SCORE

		scores = sorted(scores.items(), key=lambda x: x[1], reverse = True)
		embed = discord.Embed(title= '__**# Scoreboard**__', color = color )
		places = ['🥇','🥈','🥉', ':four:', ':five:',':six:', ':seven:', ':eight:', ':nine:', '🔟']
		if len(members) >= 10:
			count = 0
			for i in range(0,10):
				embed.add_field(name ='\u200b', value = f'{places[count]} : {scores[count][0]} : {scores[count][1]} pts', inline = False)
				count += 1
		elif len(members) < 10:
			count = 0
			for i in range(0,len(members)):
				embed.add_field(name = '\u200b', value = f'{places[count]} : {scores[count][0]} : {scores[count][1]} pts',inline = False)
				count += 1
		await channel.send(embed=embed)

	@start.command()
	@commands.guild_only()
	async def custom(self, ctx, rounds:int = 1, draw_time:int = 60, guess_time:int = 70, members:commands.Greedy[discord.Member]= None):
		if len(members) is None:
			await ctx.send("You didn't specify any participants, please try again.")
			return
		if len(members) < 2:
			await ctx.send("You need more than 2 members to start a game.")
			return
		if len(members) > 30:
			await ctx.send("You have way too many members to start a game!")
			return
		themes = ['mom', 'stepsister', 'donald trump', 'nano tech', 'apple', 'orange', 'joe mama', 'pimp', 'superman', 'thor', 'Timer', 'Paper', 'Pencils', 'Index cards', 'Dice', 'Angry', 'Fireworks', 'Pumpkin', 'Baby', 'Flower', 'Rainbow', 'Beard', 'Flying saucer', 'Recycle', 'Bible', 'Giraffe', 'Sand castle', 'Bikini', 'Glasses', 'Snowflake', 'Book', 'High heel', 'Stairs', 'Bucket', 'Ice cream cone', 'Starfish', 'Bumble bee', 'Igloo', 'Strawberry', 'Butterfly', 'Lady bug', 'Sun', 'Camera', 'Lamp', 'Tire', 'Cat', 'Lion', 'Toast', 'Church', 'Mailbox', 'Toothbrush', 'Crayon', 'Night', 'Toothpaste', 'Dolphin', 'Nose', 'Truck', 'Egg', 'Olympics', 'Volleyball', 'Eiffel Tower', 'Peanut', 'Abraham Lincoln', 'Kiss', 'Pigtails', 'Brain', 'Kitten', 'Playground', 'Bubble bath', 'Kiwi', 'Pumpkin pie', 'Buckle', 'Lipstick', 'Raindrop', 'Bus', 'Lobster', 'Robot', 'Car accident', 'Lollipop', 'Sand castle', 'Castle', 'Magnet', 'Slipper', 'Chain saw', 'Megaphone', 'Snowball', 'Circus tent', 'Mermaid', 'Sprinkler', 'Computer', 'Minivan', 'Statue of Liberty', 'Crib', 'Mount Rushmore', 'Tadpole', 'Dragon', 'Music', 'Teepee', 'Dumbbell', 'North pole', 'Telescope', 'Eel', 'Nurse', 'Train', 'Ferris wheel', 'Owl', 'Tricycle', 'Flag', 'Pacifier', 'Tuk Tuk', 'Junk mail', 'Piano']
		guild = ctx.guild
		channel = ctx.channel
		color = 0x9494FF
		scores = {}
		lobby_init = await ctx.send(embed=discord.Embed(title='__**# Lobby**__', description = f'> Starting in 3 seconds...\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color = color))
		await asyncio.sleep(3)
		for member in members:
			scores[member.mention] = 0
			try: 
				await lobby_init.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'> {member.mention} Please reply ready.\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color = color))
				msg = await self.client.wait_for('message', check=lambda message : message.content.lower() == 'ready' and message.channel == channel and message.author == member, timeout = 30)
			except asyncio.TimeoutError:
				await lobby_init.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'{member.mention} is inactive - Lobby failed to start.', color = discord.Color.dark_red()))
				return
		main_embed = await ctx.send(embed=discord.Embed(title = "All players ready.", color = color))
		await asyncio.sleep(0.5)
		to_be_edited = await ctx.send('> Game is starting in `5` seconds....')
		await asyncio.sleep(5)
		await to_be_edited.delete()
		await main_embed.edit(embed = discord.Embed(title = "GAME HAS STARTED", description = 'Round : 1', color= color))
		for i in range(0 , rounds):
			if i > 0:
				await channel.send(embed = discord.Embed(title = "Game Update", description = f'Round : {i+1}', color= color))
			for member in members:
				theme = random.choice(themes)
				words = list(theme)
				blank_list = []
				for i in words:
					if i == ' ':
						blank_list.append('  ')
					else:
						blank_list.append(' _ ')
				blank = ''.join(blank_list)
				await channel.send(f"> Its {member.mention}'s turn, lets wait for them to submit their drawing!")
				await member.send(embed = discord.Embed(title=f'Eyo, please draw "{theme}" in MS paint and send me a picture of it.', description=f'You only have {draw_time} seconds so get it together son.', color = color))
				try:
					msg = await self.client.wait_for('message', check=lambda message : len(message.attachments)> 0 and message.guild is None and message.author == member, timeout = draw_time)
				except asyncio.TimeoutError:
					await member.send(f'{draw_time} seconds has elapsed and still no drawings, what a shame son.')
					await channel.send(f"> Son's lackin, too slow and couldn't submit in time, -🔟 from your points {member.mention}")
					scores[member.mention] -= 10
				else:
					embed = discord.Embed(title=f'Drawn by {member.display_name}', description = f'Start pushing in THEM guesses, just say it out load, no fancy commands needed!\n Word : `{blank}`', color = color)
					embed.set_image(url=msg.attachments[0].url)
					await channel.send(embed=embed)
					try: 
						msg = await self.client.wait_for('message', check=lambda message : message.content.lower() == theme.lower() and message.channel == channel and message.author in members and message.author != member, timeout = guess_time)
					except asyncio.TimeoutError:
						await ctx.send(f"Yall couldn't answer in time, WHICH, surprised absolutely no one. The theme was `{theme}`.")
					else:
						await ctx.send(f"{msg.author.mention} guessed it correctly. Fair play peanut! Here's 🔟 pts")
						scores[msg.author.mention] += 10
		scores = sorted(scores.items(), key=lambda x: x[1], reverse = True)
		embed = discord.Embed(title= '__**# Scoreboard**__', color = color )
		places = ['🥇','🥈','🥉', ':four:', ':five:',':six:', ':seven:', ':eight:', ':nine:', '🔟']
		if len(members) >= 10:
			count = 0
			for i in range(0,10):
				embed.add_field(name ='\u200b', value = f'{places[count]} : {scores[count][0]} : {scores[count][1]} pts', inline = False)
				count += 1
		elif len(members) < 10:
			count = 0
			for i in range(0,len(members)):
				embed.add_field(name = '\u200b', value = f'{places[count]} : {scores[count][0]} : {scores[count][1]} pts',inline = False)
				count += 1
		await channel.send(embed=embed)


def setup(client):
	client.add_cog(Pictionary(client))
	print('Pictionary.cog is loaded')
