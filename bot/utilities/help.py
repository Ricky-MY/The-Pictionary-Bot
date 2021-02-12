import discord
import json
import datetime
from discord.ext import commands, menus
from bot.utilities.prefixes import prefixes_directory

class HelpMenu(menus.Menu):

    '''Menu system for the help menu'''

    async def send_initial_message(self, ctx, channel):
        with open(prefixes_directory, 'r') as f:
            prefixes = json.load(f)
        color = 0x87ceeb
        page1 = discord.Embed(title='__# Visual Tutorial__', color=color)
        page1.add_field(
            name='\nStep 1:', value=f'Initiate a lobby using the command \n`{prefix}start <mode> <rounds> <participants>`\nAll participants have to react to the message with the emoji given to start the game!', inline=False)
        page1.set_image(
            url='https://i.gyazo.com/f641c27eac788ebb888455ba58826a33.png')
        page1.set_thumbnail(
            url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
        page1.set_footer(
            text='Use the buttons below to browse through the guide')

        page2 = discord.Embed(title='__# Visual Tutorial__', color=color)
        page2.add_field(
            name='\nStep 2:', value=f'If its your turn to draw, the bot will DM you the details, just draw and submit by replying to the dm!', inline=False)
        page2.set_image(
            url='https://i.gyazo.com/e4be08116bdd0fedab95c70f200f5dee.png')
        page2.set_thumbnail(
            url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
        page2.set_footer(
            text='Use the buttons below to browse through the guide')

        page3 = discord.Embed(title='__# Visual Tutorial__', color=color)
        page3.add_field(
            name='\nStep 3:', value=f'Is it not your turn to draw?!, son, its still your turn to guess, wake yourself up!', inline=False)
        page3.set_image(
            url='https://i.gyazo.com/bd8c8a8b42e6da796317a87077bced4a.png')
        page3.set_thumbnail(
            url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
        page3.set_footer(
            text='Use the buttons below to browse through the guide')

        page4 = discord.Embed(title='__# Visual Tutorial__', color=color)
        page4.add_field(name=" \nThat's about it!",
                        value=f'Have a slipping fun playing!', inline=False)
        page4.add_field(name="You've reached the end! wasn't so hard was it.",
                        value=f'[Join our support server for further support!](https://discord.gg/UmnzdPgn6g)', inline=False)
        page4.set_thumbnail(
            url='https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png')
        self.pages = [page1, page2, page3, page4]
        self.count = 0
        return await channel.send(embed=self.pages[self.count])

    @menus.button('⬅️')
    async def on_thumbs_up(self, payload):
        if self.count > 0:
            self.count -= 1
            await self.message.edit(embed=self.pages[self.count])

    @menus.button('➡️')
    async def on_thumbs_down(self, payload):
        if self.count < 3:
            self.count += 1
            await self.message.edit(embed=self.pages[self.count])

    @menus.button('🗑️')
    async def on_stop(self, payload):
        await self.message.delete()

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x87ceeb

    def go_get_prefix(self, ctx):
        with open(prefixes_directory, 'r') as f:
                prefixes = json.load(f)
        try:
            prefixes[str(ctx.guild.id)]
        except AttributeError:
            return '~'
        else:
            return prefixes[str(ctx.guild.id)]

    @commands.command(name= "updates", aliases = ["changelog", "ch", "up"])
    async def updates(self, ctx):
        prefix = self.go_get_prefix(ctx)
        embed = discord.Embed(title="__# Changelog__", description=f'Command : `{prefix}start normal <rounds> <participants>`\n\n__**Update Pushed : 05/02/2021**__', color=self.color)
        embed.add_field(name='\nNew Hinting System:',
                        value=f'If players are unable to answer within the first __7 seconds__, more blanks will be revealed in the interval of __6 seconds__.', inline=False)
        embed.add_field(name='\nNew Rewarding System:',
                        value=f'The new system allows everyone who can answer the picture to be rewarded. The __faster__ a person answers the more points they get.', inline=False)
        embed.add_field(name='\nColor scheme change and three new commands',
                        value=f'All embed colors have been changed into __0x87ceeb__.\n•{prefix}updates\n•{prefix}feedback <feedback>\n•{prefix}help drawing', inline=False)
        embed.add_field(name='\nBetter generated themes:',
                        value=f'Pulling from local dictionaries for themes', inline=False)
        embed.add_field(name='\u200b\nPrefix Commands:',
                        value=f'`{prefix}prefix` (Shows Current Prefix)\n`{prefix}prefix change <new_prefix>`(Changes Current Prefix)', inline=True)
        embed.add_field(name='\u200b\nMultipurpose Help:',
                        value=f'Use `{prefix}help`', inline=True)
        embed.add_field(
            name='\u200b', value=f'[Find the open-source code here!](https://github.com/Ricky-MY/The-Pictionary-Bot)', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        embed.set_footer(text="Version 1.0.0.0")
        embed.timestamp = datetime.datetime(2021, 14, 2)
        await ctx.send(embed=embed)


    # Guilds Checker
    @commands.group(name="help", aliases=['manual', 'YOOO', 'info'], invoke_without_command=True)
    async def help(self, ctx):
        prefix = self.go_get_prefix(ctx)
        embed = discord.Embed(title="__# Information and Manual__", description=f'Command : `{prefix}start normal <rounds> <participants>`\n\n**1. A game can consist of 2 to 30 players**\n- All participants must be active when the game is started.\n\n**2. When the game starts each participant in the game will have a chance to draw and guess.**\n- To draw, you should use MS paint or any simple paint application screenshot it and submit it. For more drawing related tips do `{prefix} help drawing`. Normally, each person gets 60 seconds to draw and 70 seconds to guess\n\n**3. You get higher points the faster you get the answer.**\n- Note that the scores are built for every game session.', color=self.color)
        embed.add_field(name='\nIn-depth Guide:',
                        value=f'`{prefix}help guide`', inline=True)
        embed.add_field(name='\nVisual tutorial:',
                        value=f'`{prefix}help tutorial`', inline=True)
        embed.add_field(name='\nDrawing Guide:',
                        value=f'`{prefix}help drawing`', inline=True)
        embed.add_field(name='\nLATEST UPDATES:',
                        value=f'`{prefix}updates`', inline=True)
        embed.add_field(name='\nSubmit feedback',
                        value = f'`{prefix}feedback <feedback>`', inline=True)
        embed.add_field(name='\nPrefix Comamnds:',
                        value=f'`{prefix}prefix` (Current Prefix)\n`{prefix}prefix change <new_prefix>`(changes current prefix)', inline=False)
        embed.add_field(name='\nCustomizable Mode:',
                        value=f'Use `{prefix}start custom <rounds> <participants> <draw_time> <guess_time>`', inline=False)
        embed.add_field(
            name='\u200b', value=f'Join our support [server](https://discord.gg/UmnzdPgn6g) for more support and check out the open sourced Git-Hub repository [here](https://github.com/Ricky-MY/The-Pictionary-Bot).', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        await ctx.send(embed=embed)

    @help.command()
    async def support(self, ctx):
        message = ctx.message
        member = ctx.author
        await message.add_reaction('<:blue_check_mark:768785950947409972>')
        await ctx.send('> Check your dms!')
        await member.send("> Here's the link to the support server!\nhttps://discord.gg/UmnzdPgn6g")

    @help.command()
    async def guide(self, ctx):
        channel = ctx.channel
        prefix = self.go_get_prefix(ctx)
        embed = discord.Embed(title='__# In-depth Guide__ (normal mode)', description=f"Command : `{prefix}start normal <rounds> <participants>`\n\n**1.** When a lobby is initiated**(start_game command used)**, every participant is required to **prove** their **activity**. This, as of the latest update, is recoginized as reacting to the lobby message with 🖌️. If any of the participants **fail** to prove activity within `30` seconds, the game will consequently fail to start. Players can also vote for take-down using the emoji <:takedown:806794390538027009>.\n\n **2.** After **every** participant have proven their activity, the game will begin after 5 seconds. Chat will be **disabled** until the first drawing is submitted. \n\n **3.** A member is then chosen to submit a drawing of a random theme. You can draw the theme on literally anything, you candraw it on a piece of paper, take a picture and DM the bot, you can draw the picture on MS paint and send the bot, literally anything!. If they **fail** to submit the picture within a time frame of `60 seconds`, they will recieve a deduction and the game will continue onto another person in queue. \n\n **4.** If however the member **successfully** submitted the drawing, the other participants will have a timeframe of `70 seconds` to guess.\n\n**5.** All players who are able to answer correctly gets the points, the faster the more points.\n\n**6.** This process is repeated through every member and every rounds.", color=self.color)
        embed.add_field(name='\nVisual tutorial:',
                        value=f'`{prefix}help tutorial`', inline=True)
        embed.add_field(name='\nDrawing tips and tricks:',
                        value=f'`{prefix}help drawing`', inline=True)
        embed.add_field(name='\n__# Guide for Customs__',
                        value=f'Every game functionality will stay the same except several options such as the guessing time, drawing time and themes(coming soon).', inline=False)
        embed.add_field(name='\u200b\n__# Credits__',
                        value='Image by OpenIcons from Pixabay\nProfile photo by [Steve Johnson](https://unsplash.com/@steve_j?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash')
        embed.add_field(
            name='\u200b', value=f'Join our support [server](https://discord.gg/UmnzdPgn6g) for more support and check out the open sourced Git-Hub repository [here](https://github.com/Ricky-MY/The-Pictionary-Bot).', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        await channel.send(embed=embed)

    @help.command()
    async def drawing(self, ctx):
        prefix = self.go_get_prefix(ctx)
        channel = ctx.channel
        embed = discord.Embed(title='__**# Drawing Guide**__', description=f"Command : `{prefix}start normal <rounds> <participants>`\n\n**How do you draw and submit?**\nIt is highly recommended that you use really simple drawing programs such as MS paint. Here are the main steps:\n- Draw the theme in the art program\n- Screenshot it\n- Reply to the bot's DM *You can use CTRL+V to paste it directly into discord.*\nThe list below shows how to take screenshots on the 3 most popular OS.", color=self.color)
        embed.add_field(name='\nWindows:',
                        value=f'> •`PrntScreen` (RECOMMENDED)\n > •`Alt+PrtScn`\n > •`Win+Shift+S`\n > •`Win+PrtScn`', inline=True)
        embed.add_field(name='\nMacOS:',
                        value=f'> •`Shift+Cmd+3` (RECOMMENDED)\n>  •`Shift+Cmd+4`\n>  •`Shift+Cmd+4+Space`', inline=True)
        embed.add_field(name='\nLinux Debian:',
                        value=f'> •`PrntScreen` (RECOMMENDED)\n > •`Alt+PrtScn`', inline=True)
        embed.add_field(name='\nVisual tutorial:',
                        value=f'`{prefix}help tutorial`', inline=True)
        embed.add_field(name='\nMultipurpose guide:',
                        value=f'`{prefix}help`', inline=True)
        embed.add_field(name='\n__# Guide for Customs__',
                        value=f'Every game functionality will stay the same except several options such as the guessing time, drawing time and themes(coming soon).', inline=False)
        embed.add_field(
            name='\u200b', value=f'[Join our support server for further support!](https://discord.gg/UmnzdPgn6g)', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        await channel.send(embed=embed)

    @help.command()
    async def tutorial(self, ctx):
        menu = HelpMenu()
        await menu.start(ctx)

def setup(bot):
    bot.add_cog(Help(bot))
    print('Help.cog is loaded')
