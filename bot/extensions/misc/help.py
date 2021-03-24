import discord
import datetime

from discord.ext import commands

from bot.constants import Colour
from bot.extensions.utils.prefixes import get_real_prefix
from bot.utils.paginator import Paginator


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.books = []
        self.color = Colour.BABY_PINK
        self.embed = discord.Embed(color=self.color)
        self.embed.set_author(name="Information Manual", icon_url="https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f4d6.png")
        self.embed.set_footer(text="Join our support server for more support and check out the open sourced Git-Hub repository!.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) not in ['⬅️', '➡️', '🗑️'] or payload.member == self.bot:
            return
        if self.books:
            for book in self.books:
                if book.state == '0':
                    self.books.remove(book)
                elif book.state == '1':
                    await book.check_action(payload)

    @commands.command(name="updates", aliases=["changelog", "ch", "up"])
    async def updates(self, ctx):
        prefix = await get_real_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.title="Changelog"
        embed.description=f'Command : `{prefix}start normal <rounds> <participants>`\n\n__**Update Pushed : 05/02/2021**__'
        embed.add_field(name='\nNew Leaderboard System:',
                        value=f'A **daily** and a **all times** leaderboard has been introduced in the latest update. The daily leaderboard holds the first 50 players that has the highest score of the day whilst the all times leaderboard holds the total score of all the games the player has played.', inline=False)
        embed.add_field(name='\nNew Database for prefixes:',
                        value=f'The update does not alter any behavior of the bot. Can expect better latency and responsiveness. Your personal prefixes are transferred to the new database so there should be no worry for data loss.', inline=False)
        embed.add_field(name='\nNew anti-abuse system:',
                        value=f'Along with global leaderboards, an anti-abuse system is introduced to enhance the integrity of the leaderboard.\n\n Color changed to: 0x1A7B9C(check config.yml for further information)', inline=False)
        embed.add_field(name='\u200b\nCommands:',
                        value=f'`{prefix}top <daily/alltime>` (Shows Leaderboard)', inline=True)
        embed.add_field(name='\u200b\nMultipurpose Help:',
                        value=f'Use `{prefix}help`', inline=True)
        embed.add_field(
            name='\u200b', value=f'[Find the open-source code here!](https://github.com/Ricky-MY/The-Pictionary-Bot)', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        embed.set_footer(text="Version 1.0.0.1")
        embed.timestamp = datetime.datetime(2021, 2, 14)
        await ctx.reply(embed=embed, mention_author=False)

    # Guilds Checker
    @commands.group(name="help", aliases=['manual', 'YOOO', 'info'], invoke_without_command=True)
    async def help(self, ctx):
        prefix = await get_real_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.description = f"Normal Command: `$start normal <rounds> <participants>`\n\nBasic help menu. Use the following commands to find more information.\n\n**[📜 Commands:](https://github.com/Ricky-MY/The-Pictionary-Bot)**\n> **{prefix}help guide**\n> **{prefix}help tutorial**\n> **{prefix}help drawing**\n> **{prefix}updates**\n> **{prefix}feedback <feedback>**\n> **{prefix}prefix** (Current Prefix)\n> **{prefix}prefix change <new_prefix>**\n\nCustom Command: `{prefix}start custom <rounds> <draw_time> <guess_time> <participants>`"
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="tips", aliases=["tricks"])
    async def tips_and_trick(self, ctx):
        prefix = await get_real_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.add_field(name="🔔 All participants must be active when the game is started.", value="> When the game starts each participant in the game will have a chance to draw and guess.", inline=False)
        embed.add_field(name=f"🖌️ To draw, you should use MS paint or any simple paint application screenshot it and submit it.", value=f"> For more drawing related tips do $help drawing. Normally, each person gets 60 seconds to draw and 70 seconds to guess (Support: `{prefix}help drawing`)", inline=False)
        embed.add_field(name=f"🍅 Each person gets 60s to draw and 70s to guess.", value="> You get higher points the faster you get the answer. Note that the scores are built for every game session.", inline=False)
        embed.set_thumbnail(url="https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f48c.png")
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="support")
    async def support(self, ctx):
        message = ctx.message
        member = ctx.author
        await message.add_reaction('<:blue_check_mark:768785950947409972>')
        await ctx.send('> Check your dms!')
        await member.send("> Here's the link to the support server!\nhttps://discord.gg/UmnzdPgn6g")

    @help.command(name="guide")
    async def guide(self, ctx):
        channel = ctx.channel
        prefix = await get_real_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.title = 'In-depth Guide (normal mode)'
        embed.description = f"Command : `{prefix}start normal <rounds> <participants>`\n\n**1.** When a lobby is initiated**(start_game command used)**\n Every participant is required to **prove** their **activity**. This, as of the latest update, is recoginized as reacting to the lobby message with 🖌️. If any of the participants **fail** to prove activity within `30` seconds, the game will consequently fail to start. Players can also vote for take-down using the emoji <:takedown:806794390538027009>.\n\n **2.** After **every** participant have proven their activity.\nThe game will begin after 5 seconds. Chat will be **disabled** until the first drawing is submitted. \n\n **3.** A member is then chosen to submit a drawing of a random theme.\nYou can draw the theme on literally anything, you candraw it on a piece of paper, take a picture and DM the bot, you can draw the picture on MS paint and send the bot, literally anything!. If they **fail** to submit the picture within a time frame of `60 seconds`, they will recieve a deduction and the game will continue onto another person in queue. \n\n **4.** If however the member **successfully** submitted the drawing.\nThe other participants will have a timeframe of `70 seconds` to guess.\n\n**5.** All players who are able to answer correctly gets the points.\nThe faster the more points.\n\n**6.** This process is repeated through every member and every rounds.\n\n**Custom**: Every game functionality will stay the same except several options such as the guessing time, drawing time and themes(coming soon)."
        embed.add_field(name='\nVisual tutorial:',
                        value=f'`{prefix}help tutorial`', inline=True)
        embed.add_field(name='\nDrawing tips and tricks:',
                        value=f'`{prefix}help drawing`', inline=True)
        embed.add_field(name='\u200b\nCredits',
                        value='Image by OpenIcons from Pixabay\nProfile photo by [Steve Johnson](https://unsplash.com/@steve_j?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash\n\nJoin our support [server](https://discord.gg/UmnzdPgn6g) for more support and check out the open sourced Git-Hub repository [here](https://github.com/Ricky-MY/The-Pictionary-Bot).', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        await channel.send(embed=embed)

    @help.command(name="drawing", aliases=["draw"])
    async def drawing(self, ctx):
        prefix = await get_real_prefix(ctx.guild.id)
        channel = ctx.channel
        embed = self.embed.copy()
        embed.title = '**Drawing Guide**'
        embed.description = f"Command : `{prefix}start normal <rounds> <participants>`\n\n**How do you draw and submit?**\nIt is highly recommended that you use really simple drawing programs such as MS paint. Here are the main steps:\n- Draw the theme in the art program\n- Screenshot it\n- Reply to the bot's DM *You can use CTRL+V to paste it directly into discord.*\nThe list below shows how to take screenshots on the 3 most popular OS."
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
        embed.add_field(name='\nGuide for Customs',
                        value=f'Every game functionality will stay the same except several options such as the guessing time, drawing time and themes(coming soon).', inline=False)
        embed.add_field(
            name='\u200b', value=f'[Join our support server for further support!](https://discord.gg/UmnzdPgn6g)', inline=False)
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2013/04/01/21/30/book-99131_960_720.png')
        embed.set_footer(text='')
        await channel.send(embed=embed)

    @help.command(name="tutorial")
    async def tutorial(self, ctx):
        entry = Paginator(['⬅️', '➡️', '🗑️'], 60)
        prefix = await get_real_prefix(ctx.guild.id)
        fields = [('\nStep 1:',
                   f'Initiate a lobby using the command \n`{prefix}start <mode> <rounds> <participants>`\nAll participants have to react to the message with the emoji given to start the game!',
                   False)]
        entry.add_page(title="Visual Tutorial", color=self.color, image_url="https://i.gyazo.com/f641c27eac788ebb888455ba58826a33.png", fields=fields,
                       thumbnail_url="https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png", footer="Use the buttons below to browse through the guide")

        fields = [('\nStep 2:',
                   f'If its your turn to draw, the bot will DM you the details, just draw and submit by replying to the dm!',
                   False)]
        entry.add_page(title="Visual Tutorial", color=self.color, image_url="https://i.gyazo.com/e4be08116bdd0fedab95c70f200f5dee.png", fields=fields,
                       thumbnail_url="https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png", footer="Use the buttons below to browse through the guide")

        fields = [('\nStep 3:',
                   f'Is it not your turn to draw?!, son, its still your turn to guess, wake yourself up!',
                   False)]
        entry.add_page(title="Visual Tutorial", color=self.color, image_url="https://i.gyazo.com/bd8c8a8b42e6da796317a87077bced4a.png", fields=fields,
                       thumbnail_url="https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png", footer="Use the buttons below to browse through the guide")

        fields = [(" \nThat's about it!", 'Have a slipping fun playing!', False),
                  ("You've reached the end! wasn't so hard was it.", f'[Join our support server for further support!](https://discord.gg/UmnzdPgn6g)', False)]
        entry.add_page(title="Visual Tutorial", color=self.color, image_url="https://i.gyazo.com/f641c27eac788ebb888455ba58826a33.png", fields=fields,
                       thumbnail_url="https://i.gyazo.com/520cb9b88550dae05d4a340f33eec10c.png", footer="Use the buttons below to browse through the guide")
        await entry.send_pages(ctx.channel, ctx.author)
        self.books.append(entry)


def setup(bot):
    bot.add_cog(Help(bot))
    print('Help.cog is loaded')
