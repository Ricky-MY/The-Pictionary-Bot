import dbl
from discord.ext import commands, tasks
import aiohttp
import logging


class Marketing(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2ODQ0Mjg3MzU2MTQ4MTIxNiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEyMzQyNTgzfQ.nMNHg0C2PpAN93JC59y-UmKjcu0AdP8tVj0pDH1uDco'
        self.dblpy = dbl.DBLClient(self.bot, self.token)

    # The decorator below will work only on discord.py 1.1.0+
    # In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())

    @commands.command(name = 'postserver', aliases=['ps'])
    async def post_server(self, ctx):
        guild_count = len(self.bot.guilds)
        async with aiohttp.ClientSession() as session:
            async with session.post('https://discord.bots.gg/api/v1/bots/768442873561481216/stats', json = {'guildCount': guild_count}, headers = {'Content-type' : 'application/json','Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiMzY4NjcxMjM2MzcwNDY0NzY5IiwiaWF0IjoxNjEyMzQwMjc3fQ.nKHkGVPbcne2ZGofe6BFNfa3qYHW-uxu4Ax-lT99OgM'}) as r:
                await ctx.send(f'DiscordBotsGG: {r.status}')
            async with session.post('https://www.motiondevelopment.top/api/bots/768442873561481216/stats', json = {'server-count': guild_count}, headers = {'content-type' : 'application/json', 'api-key':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'}) as r:
                await ctx.send(f'MotionDev: {r.status}')
            async with session.post('https://discordbotlist.com/api/v1/bots/768442873561481216/stats', json = {'guilds': guild_count}, headers = {'content-type' : 'application/json', 'Authorization':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'}) as r:
                await ctx.send(f'DiscordBotList: {r.status}')
        
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_count = len(self.bot.guilds)
        async with aiohttp.ClientSession() as session:
            await session.post('https://discord.bots.gg/api/v1/bots/768442873561481216/stats', json = {'guildCount': guild_count}, headers = {'Content-type' : 'application/json','Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiMzY4NjcxMjM2MzcwNDY0NzY5IiwiaWF0IjoxNjEyMzQwMjc3fQ.nKHkGVPbcne2ZGofe6BFNfa3qYHW-uxu4Ax-lT99OgM'})
            await session.post('https://www.motiondevelopment.top/api/bots/768442873561481216/stats', json = {'server-count': guild_count}, headers = {'content-type' : 'application/json', 'api-key':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'})
            await session.post('https://discordbotlist.com/api/v1/bots/768442873561481216/stats', json = {'guilds': guild_count}, headers = {'content-type' : 'application/json', 'Authorization':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'})
        
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guild_count = len(self.bot.guilds)
        async with aiohttp.ClientSession() as session:
            await session.post('https://discord.bots.gg/api/v1/bots/768442873561481216/stats', json = {'guildCount': guild_count}, headers = {'Content-type' : 'application/json','Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiMzY4NjcxMjM2MzcwNDY0NzY5IiwiaWF0IjoxNjEyMzQwMjc3fQ.nKHkGVPbcne2ZGofe6BFNfa3qYHW-uxu4Ax-lT99OgM'})
            await session.post('https://www.motiondevelopment.top/api/bots/768442873561481216/stats', json = {'server-count': guild_count}, headers = {'content-type' : 'application/json', 'api-key':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'})
            await session.post('https://discordbotlist.com/api/v1/bots/768442873561481216/stats', json = {'guilds': guild_count}, headers = {'content-type' : 'application/json', 'Authorization':'xdyczhvgmkIx4haeqaot2czAdC4ABojkPK3WMsHi'})

        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(Marketing(bot))
    print("Marketing is loaded")