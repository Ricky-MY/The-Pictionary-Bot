import discord
from discord.ext import commands

import asyncio
import random

class Pictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x87ceeb

        self.channels = {} # {guild_id: channel_id}
        self.to_ready_up = {} # {"message_id" : {user_id : bool}}

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
        scores = {}
        self.to_ready_up[message.id] = {}

        for member in members:
            self.to_ready_up[message.id][member.id] = False
            scores[member.mention] = STARTING_SCORE
        players_text = ' ,'.join([member.mention for member in members])
        await message.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'> Players: {players_text}\n> \n> All members please react with {self.ready_up_emoji} to ready up.\n> Vote with {self.takedown_emoji} to force stop(3/4 votes).\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color = self.color))
        
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
                    return scores
                await asyncio.sleep(1)
        inactive_members = [f'<@{key}>' for key in self.to_ready_up[message.id].keys() if self.to_ready_up[message.id][key] == False]
        inactive_members = ', '.join(inactive_members)
        _ = 'are' if len(inactive_members) >= 2 else 'is'
        await message.edit(embed=discord.Embed(title='__**# Lobby**__', description = f'{inactive_members} {_} inactive - Lobby failed to start.', color = discord.Color.dark_red()))
        self.channels.pop(ctx.guild.id)
        await asyncio.sleep(5)
        await message.delete()
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

    async def build_score(self, scores, members):
        scores = sorted(scores.items(), key=lambda x: x[1], reverse = True)
        embed = discord.Embed(title= '__**# Scoreboard**__', color = 0x9494FF )
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

    '''The event below works hand in hand with rapid_ready_up to form a await_for-like process
    that waits for emojis to be reacted without a halt within the command process. Working smoother.'''

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id in [int(self.channels[key]) for key in self.channels.keys()]:
            guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.user_id in [i for i in self.to_ready_up[message.id].keys()]:
                emoji = str(payload.emoji)
                if emoji == self.ready_up_emoji:
                    self.to_ready_up[message.id][payload.user_id] = True
                    await channel.send(f'<@{payload.user_id}> is now ready!')
                if emoji == self.takedown_emoji:
                    if (target_reaction := [reaction for reaction in message.reactions if f'{reaction.emoji}' == self.takedown_emoji][0]).count == len([i for i in self.to_ready_up[message.id].keys()]):
                        user_list = await target_reaction.users().flatten()
                        sd_people = ', '.join(v := [user.mention for user in user_list if user != self.bot.user])
                        _ = 'have' if len(v) >= 2 else 'has'

                        await message.edit(embed=discord.Embed(title='__**# Force Stop**__', description = f'{sd_people} {_} voted to force stop the match.', color = discord.Color.dark_red()))
                        self.to_ready_up.pop(message.id)
                        self.channels.pop(guild.id)
                        await asyncio.sleep(5)
                        await message.delete()

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def start(self, ctx):
        await ctx.send(embed=discord.Embed(title= "Setup" ,description=f'Please choose __**normal/custom**__ by using the following command\n\n> `{ctx.prefix}start custom <rounds> <participants> <draw_time> <guess_time> `\n> `{ctx.prefix}start normal <rounds> <participants>`', color = 0x9494FF))

    @start.command()
    async def normal(self, ctx, rounds : int = 1 , members : commands.Greedy[discord.Member] = None, draw_time = 60, guess_time = 70):
        # Check up
        if members is None:
            await ctx.send("⚠️ You didn't specify any participants, please try again.")
            return
        if len(members) is not None:
            members = await self.member_validation(members, ctx.author, ctx.guild.me)
        if len(members) < 2:
            await ctx.send("⚠️ You need more than 2 members to start a game.")
            return
        elif len(members) > 30:
            await ctx.send("⚠️ You have way too many members to start a game!")
            return

        # Requirement satisifed

        if ctx.channel.id in [self.channels[key] for key in self.channels.keys()]:
            await ctx.send("⚠️ Unable to start a new game since there is an on-going game in this channel.")
            return
        
        self.channels[ctx.guild.id] = ctx.channel.id

        themes = ['Mom', 'Donald Trump', 'Joe Biden', 'apple', 'orange', 'merman', 'superman', 'thor', 'Timer', 'Paper', 'Pencils', 'Index cards', 'Dice', 'Angry', 'Fireworks', 'Pumpkin', 'Baby', 'Flower', 'Rainbow', 'Beard', 'Flying saucer', 'Recycle', 'Bible', 'Giraffe', 'Sand castle', 'Glasses', 'Snowflake', 'Book', 'High heel', 'Stairs', 'Bucket', 'Ice cream cone', 'Starfish', 'Bumble bee', 'Igloo', 'Strawberry', 'Butterfly', 'Lady bug', 'Sun', 'Camera', 'Lamp', 'Tire', 'Cat', 'Lion', 'Toast', 'Church', 'Mailbox', 'Toothbrush', 'Crayon', 'Night', 'Toothpaste', 'Dolphin', 'Nose', 'Truck', 'Egg', 'Olympics', 'Volleyball', 'Eiffel Tower', 'Peanut', 'Abraham Lincoln', 'Kiss', 'Pigtails', 'Brain', 'Kitten', 'Playground', 'Bubble bath', 'Kiwi', 'Pumpkin pie', 'Buckle', 'Lipstick', 'Raindrop', 'Bus', 'Lobster', 'Robot', 'Car accident', 'Lollipop', 'Sand castle', 'Castle', 'Magnet', 'Slipper', 'Chain saw', 'Megaphone', 'Snowball', 'Circus tent', 'Mermaid', 'Sprinkler', 'Computer', 'Minivan', 'Statue of Liberty', 'Crib', 'Mount Rushmore', 'Tadpole', 'Dragon', 'Music', 'Teepee', 'Dumbbell', 'North pole', 'Telescope', 'Eel', 'Nurse', 'Train', 'Ferris wheel', 'Owl', 'Tricycle', 'Flag', 'Pacifier', 'Tuk Tuk', 'Junk mail', 'Piano']
        channel = ctx.channel
        DRAWING_TIME = draw_time
        GUESSING_TIME = guess_time
        STARTING_SCORE = 0
        BASIC_SCORE = 10
        lobby_init = await ctx.send(embed=discord.Embed(title='__**# Lobby**__', description = f'> Starting in 3 seconds...\n> \n> Guess Time = {guess_time} seconds\n> \n> Drawing Time = {draw_time} seconds\n> \n> No of Participants = {len(members)}', color = self.color))
        await asyncio.sleep(3)

        # Ready-up protocol
        try:
            scores = await self.rapid_ready_up(ctx, lobby_init, members, STARTING_SCORE, GUESSING_TIME, DRAWING_TIME)
        except asyncio.TimeoutError:
            return
        # Ends

        main_embed = await channel.send(embed=discord.Embed(title = "All players ready.", description = "Game will shortly begin in 5 seconds", color = self.color))
        await asyncio.sleep(5)
        await main_embed.edit(embed = discord.Embed(title = "GAME HAS STARTED", description = 'Round : 1', color= self.color))

        for i in range(0, rounds):
            if i > 0:
                await channel.send(embed = discord.Embed(title = "Game Update", description = f'Round : {i+1}', color= self.color))
            for member in members:
                blank, theme = await self.get_word(themes)	
                await channel.send(f"> Its {member.mention}'s turn, lets wait for them to submit their drawing. You can use any drawing apps to draw the theme. All you need to do is reply to the bot's DMs with the picture!")
                try:
                    await member.send(embed = discord.Embed(title=f'Eyo, please draw "{theme}" in MS paint and send me a picture of it.', description='You only have 60 seconds so get it together son.', color = self.color))
                except discord.errors.HTTPException:
                    await ctx.send(f"Unable to send requesting offer to the member {member}. Make sure to enable dms and restart the game!")
                    return

                try:
                    msg = await self.bot.wait_for('message', check=lambda message : len(message.attachments)> 0 and message.guild is None and message.author == member, timeout = DRAWING_TIME)
                except asyncio.TimeoutError:
                    await member.send(f"60 seconds has elapsed and still no drawings, what a let down :p.")
                    await channel.send(f"Got caught lackin, too slow and couldn't submit in time, -{BASIC_SCORE} from your points {member.mention}")
                    scores[member.mention] -= BASIC_SCORE
                else:
                    embed = discord.Embed(title=f'Drawn by {member.display_name}', description = f'Start pushing in THEM guesses, just say it out loud, no fancy commands needed!\n Word : `{blank}`', color = self.color)
                    embed.set_image(url=msg.attachments[0].url)
                    await channel.send(embed=embed)
                    try: 
                        msg = await self.bot.wait_for('message', check=lambda message : message.content.lower() == theme.lower() and message.channel == channel and message.author in members and message.author != member, timeout = GUESSING_TIME  )
                    except asyncio.TimeoutError:
                        await ctx.send(f"You guys couldn't answer it in time. What a let down :p, the theme was `{theme}` btw, it was easy.")
                    else:
                        await ctx.send(f'{msg.author.mention} guessed it correctly. Not bad considering the brain cells count.')
                        scores[msg.author.mention] += BASIC_SCORE
        embed = await self.build_score(scores, members)
        await channel.send(embed=embed)
        self.channels.pop(ctx.guild.id)

    @start.command()
    async def custom(self, ctx, rounds:int = 1, members:commands.Greedy[discord.Member] = None, draw_time = 60, guess_time = 70):
        await self.normal(ctx, rounds, members, draw_time, guess_time)

def setup(bot):
    bot.add_cog(Pictionary(bot))
    print('Pictionary.cog is loaded')
