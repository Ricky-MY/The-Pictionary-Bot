import discord
from discord.ext import commands

import asyncio
import random


class Pictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x87ceeb
        self.basic_score = 7

        self.channels = {}  # {guild_id: channel_id}

        self.to_ready_up = {}  # {messageID : {user_id : bool}}
        self.to_complete_answers = {} # {channelID : ['theme', [members], place]}
        
        self.scores = {} # {channelID : {authorID :score, authorID2 :score}}

        self.ready_up_emoji = '🖌️'
        self.takedown_emoji = '<:takedown:806794390538027009>'

    ''' ======= Pictionary =========
    This is the main cog that every game loop will be in.
    
    Initiator - 'start'
        - normal 
        - custom
    
    A member checkup is done before bot enters the game loop.'''

    '''This async function loops through self.to_ready_up which contains lobbies that have to be dealt with.
        It checks whether if the current server that the function is invoked on has all members responded and commited
        to the lobby.'''

    async def rapid_ready_up(self, ctx, message, members, STARTING_SCORE, guess_time, draw_time):
        self.to_ready_up[message.id] = {}
        self.scores[ctx.channel.id] = {}
        for member in members:
            self.to_ready_up[message.id][member.id] = False
            self.scores[ctx.channel.id][member.id] = STARTING_SCORE
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
                if False in [self.to_ready_up[message.id][key] for key in self.to_ready_up[message.id].keys()]:
                    pass
                elif False not in [self.to_ready_up[message.id][key] for key in self.to_ready_up[message.id].keys()]:
                    self.to_ready_up.pop(message.id)
                    return
                await asyncio.sleep(1)
        inactive_members = [f'<@{key}>' for key in self.to_ready_up[message.id].keys() if self.to_ready_up[message.id][key] == False]
        inactive_members = ', '.join(z := inactive_members)
        _ = 'are' if len(z) >= 2 else 'is'
        await message.edit(embed=discord.Embed(title='__**# Lobby**__', description=f'{inactive_members} {_} inactive - Lobby failed to start.', color=discord.Color.dark_red()))
        self.channels.pop(ctx.guild.id)
        raise asyncio.TimeoutError

    '''This is a function to generate a string of blanks and words used to hint and 
    process through the pictionary guessing system.'''

    async def get_word(self, themes):
        theme = random.choice(themes)
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

    '''The function below takes in scores and members, sorts them accordingly to their scores
    and arranges a scoreboard.'''

    async def build_score(self, channel, members):
        scores = self.scores[channel.id]
        scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title='__**# Scoreboard**__', color=self.color)
        places = ['🥇', '🥈', '🥉', ':four:', ':five:',
                  ':six:', ':seven:', ':eight:', ':nine:', '🔟']
        if len(members) >= 10:
            count = 0
            for i in range(0, 10):
                embed.add_field(
                    name='\u200b', value=f'{places[count]} : <@{scores[count][0]}> : {scores[count][1]} pts', inline=False)
                count += 1
        elif len(members) < 10:
            count = 0
            for i in range(0, len(members)):
                embed.add_field(
                    name='\u200b', value=f'{places[count]} : <@{scores[count][0]}> : {scores[count][1]} pts', inline=False)
                count += 1
        self.scores.pop(channel.id)
        return embed

    '''To add the author into the basic game construct if it is not included. 
    It also removes duplicate member argument.'''

    async def member_validation(self, members, author, bot):
        members = list(set(members))
        if author not in members:
            members.append(author)
        if self.bot.user in members:
            members.remove(bot)
        return members

    '''To request a drawing from a player through dms.'''

    async def get_drawing_and_redirect(self, theme, blank, member, channel, waiting_time):
        await channel.send(embed = discord.Embed(title="**Drawing**", description = f"> Its {member.mention}'s turn. You can use any drawing apps to draw the theme. All you need to do is reply to the bot's DMs with the picture!", color = self.color))
        try:
            # Attempting dm to member
            await member.send(embed=discord.Embed(title=f'Eyo, please draw "{theme}" in MS paint and send me a picture of it.', description='You only have 60 seconds so get it together son.', color=self.color))
        except discord.errors.HTTPException:
            #DM failure
            raise discord.errors.HTTPException
        else:
            #DM success
            try:
                #Waiting time
                msg = await self.bot.wait_for('message', check=lambda message: len(message.attachments) > 0 and message.guild is None and message.author == member, timeout=waiting_time)
            except asyncio.TimeoutError:
                #Timeout
                raise asyncio.TimeoutError
            else:
                #Successful submission
                embed = discord.Embed(
                    title=f'Drawn by {member.display_name}', description=f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`', color=self.color)
                embed.set_image(url=msg.attachments[0].url)
                message = await channel.send(embed=embed)
                return message

    async def get_answers_from_players(self, message, channel, theme, blank, members, artist, answer_time):
        data = [theme, [member for member in members if member!= artist], len(members)]
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
            if i >= (i // 2) and i % 6 == 0 and i != 0:
                for i in range(len(fake_blank)):
                    if (fake_blank[i] != list(theme_copy)[i]) and (not changed) and (list(theme_copy)[i] != ' '):
                        fake_blank[i] = list(theme_copy)[i]
                        changed = True
                blank = ''.join(fake_blank)
                embed = message.embeds[0]
                embed.description = f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`'
                await message.edit(embed=embed)

        if len(z:= data[1]) > 0:
            unanswered = [f'{i.mention}' for i in data[1]]
            text = ', '.join(unanswered)
            _ = 'have' if len(z) >= 2 else 'has'
            await channel.send(f"{text} {_} failed to answer correctly. What a let down fellas :p. The theme was {theme}")
        try:
            self.to_complete_answers.pop(channel.id)
        except KeyError:
            pass
    
    '''The event below will handle answers from players and score them accordingly'''

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

    '''The event below works hand in hand with rapid_ready_up to form a await_for-like process
    that waits for emojis to be reacted without a halt within the command process.
    Making it work like a well oiled machine.'''

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id in [int(self.channels[key]) for key in self.channels.keys()]:
            guild = discord.utils.find(
                lambda g: g.id == payload.guild_id, self.bot.guilds)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.user_id in [i for i in self.to_ready_up[message.id].keys()] and not self.to_ready_up[message.id][payload.user_id]:
                emoji = str(payload.emoji)
                member = guild.get_member(payload.user_id)
                if emoji == self.ready_up_emoji:
                    self.to_ready_up[message.id][payload.user_id] = True
                    await channel.send(f'{member.display_name} is now ready!')
                if emoji == self.takedown_emoji:
                    if (target_reaction := [reaction for reaction in message.reactions if f'{reaction.emoji}' == self.takedown_emoji][0]).count == len([i for i in self.to_ready_up[message.id].keys()]):
                        user_list = await target_reaction.users().flatten()
                        sd_people = ', '.join(
                            v := [i.mention for i in [user for user in user_list if user != self.bot.user] if i.id in self.to_ready_up[message.id].keys()])
                        _ = 'have' if len(v) >= 2 else 'has'

                        await message.edit(embed=discord.Embed(title='__**# Force Stop**__', description=f'{sd_people} {_} voted to force stop the match.', color=discord.Color.dark_red()))
                        self.to_ready_up.pop(message.id)
                        self.channels.pop(guild.id)
                        await asyncio.sleep(5)
                        await message.delete()

    @commands.group(invoke_without_command=True)
    @commands.bot_has_permissions(manage_messages = True)
    @commands.guild_only()
    async def start(self, ctx):
        await ctx.send(embed=discord.Embed(title="Setup", description=f'Please choose __**normal/custom**__ by using the following command\n\n> `{ctx.prefix}start custom <rounds> <participants> <draw_time> <guess_time> `\n> `{ctx.prefix}start normal <rounds> <participants>`', color=self.color))

    @start.command()
    @commands.bot_has_permissions(manage_messages = True)
    async def normal(self, ctx, rounds: int = 1, members: commands.Greedy[discord.Member] = None, draw_time=60, guess_time=70):
        # Pre-member validation
        if members is None:
            await ctx.send("⚠️ You didn't specify any participants, please try again.")
            return
        elif members is not None:
            members = await self.member_validation(members, ctx.author, ctx.guild.me)

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
        themes = ['Mom', 'Donald Trump', 'Joe Biden', 'apple', 'orange', 'merman', 'superman', 'thor', 'Timer', 'Paper', 'Pencils', 'Index cards', 'Dice', 'Angry', 'Fireworks', 'Pumpkin', 'Baby', 'Flower', 'Rainbow', 'Beard', 'Flying saucer', 'Recycle', 'Bible', 'Giraffe', 'Sand castle', 'Glasses', 'Snowflake', 'Book', 'High heel', 'Stairs', 'Bucket', 'Ice cream cone', 'Starfish', 'Bumble bee', 'Igloo', 'Strawberry', 'Butterfly', 'Lady bug', 'Sun', 'Camera', 'Lamp', 'Tire', 'Cat', 'Lion', 'Toast', 'Church', 'Mailbox', 'Toothbrush', 'Crayon', 'Night', 'Toothpaste', 'Dolphin', 'Nose', 'Truck', 'Egg', 'Olympics', 'Volleyball',
                  'Eiffel Tower', 'Peanut', 'Abraham Lincoln', 'Kiss', 'Pigtails', 'Brain', 'Kitten', 'Playground', 'Bubble bath', 'Kiwi', 'Pumpkin pie', 'Buckle', 'Lipstick', 'Raindrop', 'Bus', 'Lobster', 'Robot', 'Car accident', 'Lollipop', 'Sand castle', 'Castle', 'Magnet', 'Slipper', 'Chain saw', 'Megaphone', 'Snowball', 'Circus tent', 'Mermaid', 'Sprinkler', 'Computer', 'Minivan', 'Statue of Liberty', 'Crib', 'Mount Rushmore', 'Tadpole', 'Dragon', 'Music', 'Teepee', 'Dumbbell', 'North pole', 'Telescope', 'Eel', 'Nurse', 'Train', 'Ferris wheel', 'Owl', 'Tricycle', 'Flag', 'Pacifier', 'Tuk Tuk', 'Junk mail', 'Piano']
        channel = ctx.channel
        DRAWING_TIME = draw_time
        GUESSING_TIME = guess_time
        STARTING_SCORE = 0
        BASIC_SCORE = 10
        lobby_init = await ctx.send(embed=discord.Embed(title='__**# Lobby**__', description=f'> Starting in 3 seconds...\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color=self.color))
        await asyncio.sleep(3)

        # Rapid ready-up protocol
        try:
            await self.rapid_ready_up(ctx, lobby_init, members, STARTING_SCORE, GUESSING_TIME, DRAWING_TIME)
        except asyncio.TimeoutError:
            return

        main_embed = await channel.send(embed=discord.Embed(title="All players ready.", description="Game will shortly begin in 5 seconds", color=self.color))
        await asyncio.sleep(5)
        await main_embed.edit(embed=discord.Embed(title="GAME HAS STARTED", description='Round : 1', color=self.color))

        for i in range(0, rounds):
            if i > 0:
                await channel.send(embed=discord.Embed(title="Game Update", description=f'Round : {i+1}', color=self.color))
            for member in members:
                blank, theme = await self.get_word(themes)
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
        embed = await self.build_score(channel, members)
        await channel.send(embed=embed)
        self.channels.pop(ctx.guild.id)
        print(self.channels)
        print(self.to_complete_answers)
        print(self.to_ready_up)

    @start.command()
    @commands.bot_has_permissions(manage_messages = True)
    async def custom(self, ctx, rounds: int = 1, members: commands.Greedy[discord.Member] = None, draw_time=60, guess_time=70):
        await self.normal(ctx, rounds, members, draw_time, guess_time)

    @start.command(name= 'debug', aliases=['d'])
    @commands.bot_has_permissions(manage_messages = True)
    async def debug(self, ctx, members: commands.Greedy[discord.Member] = None, *, tags: str = ''):
        draw_time=60
        guess_time=70
        if 'r' in list(tags):
            draw_time = 5
            guess_time = 5
        await self.normal(ctx, 2, members, draw_time, guess_time)

def setup(bot):
    bot.add_cog(Pictionary(bot))
    print('Pictionary.cog is loaded')
