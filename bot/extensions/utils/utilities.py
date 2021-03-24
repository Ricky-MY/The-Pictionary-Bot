import discord

from discord.ext import commands

from bot.constants import Colour

class Util(commands.Cog):

    ''' Interactable utilities commands subclass '''

    def __init__(self, bot):
        self.bot = bot
        self.color = Colour.BABY_PINK

    @commands.command(name="feedback", aliases=['fb', 'report'])
    async def feedback(self, ctx, *, feedback):
        guild = discord.utils.find(
            lambda g: g.id == 793047973751554088, self.bot.guilds)
        channel = guild.get_channel(807217915006287880)
        to_deliver = discord.Embed(
            title="Feedback", description=f"Feedback:\n```{feedback}```\nGuild: {ctx.guild.name}\nOwner: <@{ctx.guild.owner_id}>", color=self.color)
        to_deliver.set_footer(
            text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await channel.send(embed=to_deliver)
        await ctx.send(embed=discord.Embed(title="Success!", description=f"Thank you so much for your feedback. We will notify the developer right away.\nFeedback:```{feedback}```", color=self.color))


def setup(bot):
    bot.add_cog(Util(bot))
    print('Util.cog is loaded')
