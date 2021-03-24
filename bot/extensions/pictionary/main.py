import discord
import asyncio
import random
import yaml

from json import load
from datetime import datetime
from discord.ext import commands, tasks

from bot.utils.databases import DB
from bot.constants import Colour
from bot.utils.anti_abuse import AntiAbuse
from bot.utils.checks import is_admin


class Pictionary(commands.Cog):

    ''' +-------------------------- Pictionary --------------------------+
        | This is the main cog that the game loop will be written in.    |
        |                                                                |
        | Main Commands - 'start'                                        |
        |    Parameters:                                                 |
        |        - normal                                                |
        |        - custom                                                |
        |            - rounds                                            |
        |                - members                                       |
        |                                                                |
        | start <normal/custom> <rounds> <members>                       |
        +-------------------------- Pictionary --------------------------+ '''

    def __init__(self, bot):
        self.bot = bot

        self.watchdog = AntiAbuse()

        self.basic_score = 7
        self.starting_score = 0

        self.channels = {}  # {guild_id: channel_id}

        self.to_ready_up = {}           # {messageID : {user_id : bool}}
        # {channelID : ['theme', [members], place]}
        self.to_complete_answers = {}

        self.scores = {}   # {channelID : {authorID :score, authorID2 :score}}
        self.scotd = {}    # Scores of the day for leaderboards
        self.latest_answers = {}

        self.ready_up_emoji = '🖌️'
        self.takedown_emoji = '<:takedown:806794390538027009>'

        with open('./bot/assets/themes.json', 'r') as f:
            self.themes = (load(f))["words"]

        self.color = Colour.LIGHT_BLUE
        self.report_channel = 812956440972230706

        self.update_alltime_board.start()
        self.update_daily_board.start()

    async def handle_abuse(self, value):
        """
        Sends required data if an activity has been flagged
        suspicious or abusive by the anti-abuse system.
        """
        if value is None:
            return
        header, details, suspicion = value.split('|')
        guild = discord.utils.find(
            lambda g: g.id == 793047973751554088, self.bot.guilds)
        channel = guild.get_channel(self.report_channel)
        embed = discord.Embed(
            title=header, description=f"```yaml\n{details}```\n**Suspicion:**\n```yaml\n{suspicion}```", color=discord.Color.dark_red())
        embed.timestamp = datetime.now()
        await channel.send(embed=embed)

    async def rapid_ready_up(self, ctx, message, members, guess_time, draw_time):
        """
        A lobby system is used before a game instance; that is invoked by
        the rapid-ready-up function. The function cycles through a request process
        for 50 seconds, checking whether if all players have responded and commited
        to the lobby. A on_raw_reaction_add event is used as a reciever that completes a
        series of checklists.
        """
        self.to_ready_up[message.id] = {}
        self.scores[ctx.channel.id] = {}
        for member in members:
            self.to_ready_up[message.id][member.id] = False
            self.scores[ctx.channel.id][member.id] = self.starting_score

        players_text = ' ,'.join([member.mention for member in members])
        await message.edit(embed=discord.Embed(title='__**# Lobby**__', description=f'> Players: {players_text}\n> \n> All members please react with {self.ready_up_emoji} to ready up.\n> Vote with {self.takedown_emoji} to force stop(3/4 votes).\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color=self.color))

        for emoji in [self.ready_up_emoji, self.takedown_emoji]:
            await message.add_reaction(emoji)

        for i in range(50):
            try:
                self.to_ready_up[message.id]
            except KeyError:
                raise asyncio.TimeoutError
            else:
                if False not in [self.to_ready_up[message.id][key] for key in self.to_ready_up[message.id].keys()]:
                    self.to_ready_up.pop(message.id)
                    return
                await asyncio.sleep(1)

        inactive_members = [f'<@{key}>' for key in self.to_ready_up[message.id].keys(
        ) if self.to_ready_up[message.id][key] == False]
        inactive_members = ', '.join(z := inactive_members)
        await message.edit(embed=discord.Embed(title="__**# Lobby**__", description=f"{inactive_members} {'are' if len(z) >= 2 else 'is'} inactive - Lobby failed to start.", color=discord.Color.dark_red()))
        self.to_ready_up.pop(message.id)
        self.channels.pop(ctx.guild.id)
        self.scores.pop(ctx.channel.id)
        raise asyncio.TimeoutError

    def update_leaderboard(self, scores):
        """
        Daily leaderboard are updated every 2 hour whilst
        updatitive data is stored as an instant variable that gets emptied
        once being commited into the global datbase
        """
        for author in scores.keys():
            try:
                self.scotd[author]
                self.latest_answers[author]
            except KeyError:
                self.scotd[author] = 0
                self.latest_answers[author] = 0
            finally:
                self.latest_answers[author] = int(scores[author])
                self.scotd[author] = int(
                    self.scotd[author]) + int(scores[author])
        return sorted(self.scotd.items(),
                      key=lambda x: x[1], reverse=True)

    def get_word(self):
        """
        We use the get_word function to forumulate an omitted word. This is done by
        replacing all the characters from the theme with underscores. Although there is
        a minimal chance that a character stays unomitted
        """
        theme = random.choice(self.themes)
        words_of_theme = list(theme)
        blank_list = []
        hinting_words = random.randint(0, (len(words_of_theme) // 2))
        for i in words_of_theme:
            if i == ' ':
                blank_list.append('  ')
            else:
                if random.randint(0, 1) == 0 or hinting_words == 0:
                    blank_list.append(' _ ')
                else:
                    blank_list.append(f' {i} ')
                    hinting_words -= 1
        blank = ''.join(blank_list)
        return blank, theme

    async def build_score(self, guild, channel, members):
        """We use the build_score function that takes in scores and members to
        build the final embed that contains the position and scores of every
        player. This is done by sorting them accordingly to their scores from highest
        to lowest and pairing them up with positions by index.
        """
        target = self.scores[channel.id]
        scores = sorted(target.items(),
                        key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title='__**# Scoreboard**__', color=self.color)
        places = ['🥇', '🥈', '🥉', ':four:', ':five:',
                  ':six:', ':seven:', ':eight:', ':nine:', '🔟']
        for i in range(0, len(members)):
            embed.add_field(
                name='\u200b', value=f'{places[i]} : <@{scores[i][0]}> : {scores[i][1]} pts', inline=False)
        await self.handle_abuse(self.watchdog.do_reality_check(target, guild.id, channel.id))
        self.update_leaderboard(target)
        self.scores.pop(channel.id)
        return embed

    def member_validation(self, members, author, bot):
        """
        When the start command is invoked, the bot filters through the member list
        given. It ensures that there are no repeating players and that the bot is not included.
        """
        members = list(set(members))
        if author not in members:
            members.append(author)
        if self.bot.user in members:
            members.remove(bot)
        return list(members)

    async def get_drawing_and_redirect(self, theme, blank, member, channel, waiting_time):
        """
        When a lobby begins, the game instance begins looping through all members, requesting drawings.
        We get the drawing from a target member by sending them a Dm and `wait_for` a response that has
        an attachment. If a message that contains an attachment is sent, it will get redirected to the
        target channel
        """
        await channel.send(embed=discord.Embed(title="**Drawing**", description=f"> Its {member.mention}'s turn. You can use any drawing apps to draw the theme. All you need to do is reply to the bot's DMs with the picture!", color=self.color))
        try:
            # Attempting dm to member
            await member.send(embed=discord.Embed(title=f'Eyo, please draw "{theme}" in MS paint and send me a picture of it.', description='You only have 60 seconds so get it together son.', color=self.color))
        except discord.errors.HTTPException:
            # DM failure
            raise discord.errors.HTTPException
        else:
            # DM success
            try:
                # Waiting time
                msg = await self.bot.wait_for('message', check=lambda message: len(message.attachments) > 0 and message.guild is None and message.author == member, timeout=waiting_time)
            except asyncio.TimeoutError:
                # Timeout
                raise asyncio.TimeoutError
            else:
                # Successful submission
                embed = discord.Embed(
                    title=f'Drawn by {member.display_name}', description=f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`', color=self.color)
                embed.set_image(url=msg.attachments[0].url)
                message = await channel.send(embed=embed)
                return message

    async def get_answers_from_players(self, message, channel, theme, blank, members, artist, answer_time):
        """
        After a drawing has been submitted. We use a on_message event and the get_answers_from_players function
        that work collaboratively to get the correct answer from every member and reward them accordingly. This is done by
        looping through a check list for the answer_time given. When the check list is completely satisfied, the loop ends.
        The on_message event handles which member had answered correctly and how. This data is stored in a variable that gets
        checked through the loop
        """
        data = [
            theme, [member for member in members if member != artist], len(members)]
        self.to_complete_answers[channel.id] = data
        fake_blank = [i for i in blank]
        theme_copy = ''.join([f' {i} ' for i in list(theme)])
        for i in range(answer_time // 3):
            await asyncio.sleep(3)
            changed = False
            data = self.to_complete_answers[channel.id]
            if len(data[1]) == 0:
                await channel.send("Great job! Everyone answered correctly.")
                self.to_complete_answers.pop(channel.id)
                return
            if i >= (i // 2) and i % 6 == 0 and i != 0 and len(theme) > 5:
                for i in range(len(fake_blank)):
                    if (fake_blank[i] != list(theme_copy)[i]) and (not changed) and (list(theme_copy)[i] != ' '):
                        fake_blank[i] = list(theme_copy)[i]
                        changed = True
                blank = ''.join(fake_blank)
                embed = message.embeds[0]
                embed.description = f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`'
                await message.edit(embed=embed)
        if len(z := data[1]) > 0:
            unanswered = [f'{i.mention}' for i in data[1]]
            text = ', '.join(unanswered)
            await channel.send(f"{text} {'have' if len(z) >= 2 else 'has'} failed to answer correctly. What a let down fellas :p. The theme was {theme}")
        try:
            self.to_complete_answers.pop(channel.id)
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author == self.bot:
            return
        channel = message.channel
        if channel.id in self.to_complete_answers.keys():
            data = self.to_complete_answers[channel.id]
            if author in data[1] and message.content.lower() == data[0].lower():
                await message.delete()
                await channel.send(f"{author.mention} has answered correctly and scored {self.basic_score * data[2]}!")
                self.scores[channel.id][author.id] += self.basic_score * data[2]
                self.to_complete_answers[channel.id][2] -= 1
                self.to_complete_answers[channel.id][1].remove(author)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Works hand in hand with rapid_ready_up to form a await_for like process
        that waits for emojis to be reacted without a halt within the command process.
        Making it work like a well oiled machine.
        """
        if payload.channel_id in [self.channels[key] for key in self.channels.keys()]:
            guild = discord.utils.find(
                lambda g: g.id == payload.guild_id, self.bot.guilds)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.user_id in [i for i in self.to_ready_up[message.id].keys()] and not self.to_ready_up[message.id][payload.user_id]:
                emoji = str(payload.emoji)
                member = await guild.fetch_member(payload.user_id)
                if emoji == self.ready_up_emoji:
                    self.to_ready_up[message.id][payload.user_id] = True
                    await channel.send(f'{member.display_name} is now ready!')
                if emoji == self.takedown_emoji:
                    if (target_reaction := [reaction for reaction in message.reactions if f'{reaction.emoji}' == self.takedown_emoji][0]).count == len([i for i in self.to_ready_up[message.id].keys()]):
                        user_list = await target_reaction.users().flatten()
                        sd_people = ', '.join(
                            v := [i.mention for i in [user for user in user_list if user != self.bot.user] if i.id in self.to_ready_up[message.id].keys()])

                        await message.edit(embed=discord.Embed(title='__**# Force Stop**__', description=f"{sd_people} {'have' if len(v) >= 2 else 'has'} voted to force stop the match.", color=discord.Color.dark_red()))
                        self.to_ready_up.pop(message.id)
                        self.scores.pop(payload.channel_id)
                        self.channels.pop(guild.id)

    @commands.group(invoke_without_command=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    async def start(self, ctx):
        await ctx.send(embed=discord.Embed(title="Setup", description=f'Please choose __**normal/custom**__ by using the following command\n\n> `{ctx.prefix}start custom <rounds> <participants> <draw_time> <guess_time> `\n> `{ctx.prefix}start normal <rounds> <participants>`', color=self.color))

    @start.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def normal(self, ctx, rounds: int = 1, members: commands.Greedy[discord.Member] = None, draw_time=60, guess_time=70):
        # Pre-member validation
        if members is None:
            await ctx.send("⚠️ You didn't specify any participants, please try again.")
            return
        elif members is not None:
            members = self.member_validation(members, ctx.author, ctx.guild.me)

        if len(members) < 2:
            await ctx.send("⚠️ You need more than 2 members to start a game.")
            return
        elif len(members) > 30:
            await ctx.send("⚠️ You have way too many members to start a game!")
            return

        # Prevention of hosting two game instances in the same channel
        if ctx.channel.id in [self.channels[key] for key in self.channels.keys()]:
            await ctx.send("⚠️ Unable to start a new game since there is an on-going game in this channel.")
            return

        self.channels[ctx.guild.id] = ctx.channel.id
        channel = ctx.channel
        guild = ctx.guild
        DRAWING_TIME = draw_time
        GUESSING_TIME = guess_time
        BASIC_SCORE = 10
        lobby_init = await ctx.send(embed=discord.Embed(title='__**# Lobby**__', description=f'> Starting in 3 seconds...\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color=self.color))
        self.watchdog.start_watching_session(
            guild.id, channel.id, rounds, members)
        await self.handle_abuse(self.watchdog.do_entrance_check(guild.id, channel.id))
        await asyncio.sleep(3)

        # Rapid ready-up protocol
        try:
            await self.rapid_ready_up(ctx, lobby_init, members, GUESSING_TIME, DRAWING_TIME)
        except asyncio.TimeoutError:
            return

        main_embed = await channel.send(embed=discord.Embed(title="All players ready.", description="Game will shortly begin in 5 seconds", color=self.color))
        await asyncio.sleep(5)
        await main_embed.edit(embed=discord.Embed(title="GAME HAS STARTED", description='Round : 1', color=self.color))

        for i in range(0, rounds):
            if i > 0:
                await channel.send(embed=discord.Embed(title="Game Update", description=f'Round : {i+1}', color=self.color))
            for member in members:
                blank, theme = self.get_word()
                # To request the drawing and redirection of the drawing from the member
                try:
                    message = await self.get_drawing_and_redirect(theme, blank, member, channel, DRAWING_TIME)
                except discord.errors.HTTPException:
                    await channel.send(f'⚠️ Unable to send a DM to {member}, please open your dms and restart the game.')
                    return
                except asyncio.TimeoutError:
                    await member.send(f"{DRAWING_TIME} seconds has elapsed and still no drawings, what a let down :p.")
                    await channel.send(f"Got caught lackin, too slow and couldn't submit in time, -{BASIC_SCORE} from your points {member.mention}")
                    self.scores[channel.id][member.id] -= BASIC_SCORE
                else:
                    await self.get_answers_from_players(message, channel, theme, blank, members, member, GUESSING_TIME)
        embed = await self.build_score(guild, channel, members)
        await channel.send(embed=embed)
        self.channels.pop(ctx.guild.id)
        await self.handle_abuse(self.watchdog.do_exit_check(guild.id, channel.id, lobby_init.id, [self.channels, self.to_ready_up, self.to_complete_answers, self.scores]))
        self.watchdog.end_watching_session(guild.id, channel.id)

    @start.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def custom(self, ctx, rounds: int = 1, draw_time=60, guess_time=70, members: commands.Greedy[discord.Member] = None):
        await self.normal(ctx, rounds, members, draw_time, guess_time)

    @commands.command(name="log", aliases=["logger", "logging"])
    @commands.check(is_admin)
    async def logger(self, ctx):
        await ctx.send(f"scores:{self.scores}\ntoReadyUp:{self.to_ready_up}\ntoCompleteAnswers:{self.to_complete_answers}\nchannels:{self.channels}\nscoresOfTheDay:{self.scotd}")

    @commands.command(name="force24")
    @commands.check(is_admin)
    async def force_24(self, ctx):
        async with DB('bot/assets/major.db') as ctx:
            await ctx.update_value("all_time_leaderboards", self.scotd)
        async with DB('bot/assets/major.db') as cont:
            await cont.truncate('daily_boards')
        self.scotd = {}
        await ctx.send("over")

    @commands.command(name="force2")
    @commands.check(is_admin)
    async def force_2(self, ctx):
        async with DB('bot/assets/major.db') as cont:
            await cont.update_value("daily_boards", self.latest_answers)
        self.latest_answers = {}
        await ctx.send("over")

    @tasks.loop(hours=2)
    async def update_daily_board(self):
        async with DB('bot/assets/major.db') as cont:
            await cont.update_value("daily_boards", self.latest_answers)
        self.latest_answers = {}

    @tasks.loop(hours=24)
    async def update_alltime_board(self):
        async with DB('bot/assets/major.db') as ctx:
            await ctx.update_value("all_time_leaderboards", self.scotd)
        async with DB('bot/assets/major.db') as cont:
            await cont.truncate('daily_boards')
        self.scotd = {}


def setup(bot):
    bot.add_cog(Pictionary(bot))
    print('Pictionary.cog is loaded')
