import discord
import json
import os
import asyncio
from discord.ext import commands, tasks, menus

class HelpMenu(menus.Menu):
	async def send_initial_message(self, ctx, channel):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		f.close()
		color = 0x9494FF
		page1= discord.Embed(title = '__# Visual Tutorial__', color = color )
		page1.add_field(name= '\nStep 1:', value = f'Initiate a lobby using the command \n`{prefixes[str(ctx.guild.id)]}start_game <rounds> <participants>`\nMake sure to reply with ready when your name is called for activity! :P', inline = False)
		page1.set_image(url='https://i.gyazo.com/b2720f6103f25cd59dbcc8153dd59d7e.png')
		page1.set_thumbnail(url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
		page1.set_footer(text = 'Use the buttons below to browse through the guide')

		page2= discord.Embed(title = '__# Visual Tutorial__', color = color )
		page2.add_field(name= '\nStep 2:', value = f'If its your turn to draw, draw the theme given to you with whatever you want to draw with! MS Paint is being used in this picture', inline = False)
		page2.set_image(url='https://i.gyazo.com/bc5544cb7f6053e7fb42ea1b0a906191.png')
		page2.set_thumbnail(url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
		page2.set_footer(text = 'Use the buttons below to browse through the guide')

		page3=discord.Embed(title = '__# Visual Tutorial__', color = color )
		page3.add_field(name= '\nStep 3:', value = f'Is it not your turn to draw?!, son, its still your turn to guess, wake yourself up!', inline = False)
		page3.set_image(url='https://i.gyazo.com/3e863c8d18c2f5b315a33c0477e30d37.png')
		page3.set_thumbnail(url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
		page3.set_footer(text = 'Use the buttons below to browse through the guide')
		
		page4 = discord.Embed(title = '__# Visual Tutorial__', color = color )
		page4.add_field(name= " \nThat's about it!", value = f'Have a slipping fun playing!', inline = False)
		page4.add_field(name= "You've reached the end! wasn't so hard was it.",value= f'[Join our support server for further support!](https://discord.gg/dkgfBktj)', inline = False)
		page4.set_thumbnail(url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
		self.pages = [page1, page2, page3, page4]
		self.count = 0
		return await channel.send(embed = self.pages[self.count])
	
	@menus.button('⬅️')
	async def on_thumbs_up(self, payload):
		if self.count > 0:
			self.count -= 1
			await self.message.edit(embed = self.pages[self.count])

	@menus.button('➡️')
	async def on_thumbs_down(self, payload):
		if self.count < 3:
			self.count += 1
			await self.message.edit(embed = self.pages[self.count])

	@menus.button('🗑️')
	async def on_stop(self, payload):
		await self.message.delete()

class Help(commands.Cog):

	def __init__(self, client):
		self.client = client

	# Guilds Checker
	@commands.group(name="help", aliases = ['manual', 'YOOO', 'info'], invoke_without_command = True)
	@commands.guild_only()
	async def help(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		f.close()
		color = 0x9494FF
		embed = discord.Embed(title = "__# Information and Manual__", description= f'Command : `{prefixes[str(ctx.guild.id)]}start normal <rounds> <participants>`\n\n**1. A lobby can consists of up to 30 people but no less than 2.**\n- All participants must be active when the lobby is initiated.\n\n**2. When the game starts each participant in the game will have a chance to draw and guess.**\n- For drawing purposes you can use MS paint or any other simple paint application(hell, even a piece of pen and paper) to draw the given theme. Make sure to dm the picture to the bot within 60 seconds!\n\n**3. Each person gets 60 seconds to draw and 70 seconds to guess.**\n- This may also very well vary upon future updates\n\n**4. You get up to 10 points per successful guesses.**\n- Note that the scores are built for every game session.', color = color)
		embed.add_field(name= '\nIn-depth Guide:', value = f'`{prefixes[str(ctx.guild.id)]}help guide`', inline = True)
		embed.add_field(name= '\nVisual tutorial:', value = f'`{prefixes[str(ctx.guild.id)]}help tutorial`', inline = True)
		embed.add_field(name= '\nPrefix Commands:', value = f'`{prefixes[str(ctx.guild.id)]}prefix` (Shows Current Prefix)\n`{prefixes[str(ctx.guild.id)]}prefix change <new_prefix>`(Changes Current Prefix)', inline = False)
		embed.add_field(name = '\nCustomizable Mode:', value = f'Use `{prefixes[str(ctx.guild.id)]}start custom <rounds> <draw_time> <guess_time> <participants>` (Same command with just more parameters)', inline = False)
		embed.add_field(name= '\u200b',value= f'[Join our support server for further support!](https://discord.gg/xunWcUs9Rr)', inline = False)
		embed.set_thumbnail(url = 'https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
		embed2 = discord.Embed(title = 'Credits', description = 'Image by OpenIcons from Pixabay')
		await ctx.send(embed = embed)

	@help.command()
	@commands.guild_only()
	async def support(self, ctx):
		message = ctx.message
		member = ctx.author
		await message.add_reaction('<:blue_check_mark:768785950947409972>')
		await ctx.send('> Check your dms!')
		await member.send("> Here's the link to the support server!\nhttps://discord.gg/xunWcUs9Rr")

	@help.command()
	@commands.guild_only()
	async def guide(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		f.close()
		color = 0x9494FF
		channel = ctx.channel
		embed = discord.Embed(title = '__# In-depth Guide__ (normal mode)', description ="\n**=** When a lobby is initiated**(start_game command used)**, every participant is required to **prove** their **activity**. This, as of the latest update, is recoginized as replying `ready`. If any of the participants **fail** to prove activity within `30` seconds, the game will consequently fail to start. \n\n **=** After **every** participant have proven their activity, the game will begin after 5 seconds. Chat will be **disabled** until the first drawing is submitted. \n\n **=** A member is then chosen to submit a drawing of a random theme. You can draw the theme on literally anything, you candraw it on a piece of paper, take a picture and DM the bot, you can draw the picture on MS paint and send the bot, literally anything!. If they **fail** to submit the picture within a time frame of `60 seconds`, they will recieve a deduction and the game will continue onto another person in queue. \n\n **=** If however the member **successfully** submitted the drawing, the other participants will have a timeframe of `70 seconds` to guess.\n\n**=** The first person to correctly answer will recieve a few points.\n\n**=** This process is repeated through every member and every rounds.", color = color)
		embed.add_field(name= '\nVisual tutorial:', value = f'`{prefixes[str(ctx.guild.id)]}help tutorial`', inline = True)
		embed.add_field(name= '\n__# Guide for Customs__', value = f'Every game functionality will stay the same except several options such as the guessing time, drawing time and themes(coming soon).', inline = False)
		embed.add_field(name= '\u200b',value= f'[Join our support server for further support!](https://discord.gg/xunWcUs9Rr)', inline = False)
		embed.set_thumbnail(url = 'https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
		await channel.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def tutorial(self, ctx):
		menu = HelpMenu()
		await menu.start(ctx)

def setup(client):
	client.add_cog(Help(client))
	print('Help.cog is loaded')
