import discord
import time
import datetime


class Paginator:

    def __init__(self, buttons, timeout=40) -> None:
        self.backward, self.forward, self.delete = buttons
        self.pages = []

        self.index = 0
        self.state = "1"
        self.timeout = timeout

    def add_page(self, title=None, description=None, color=0x000000, thumbnail_url=None, image_url=None, fields=(), timestamp=None, footer=None):
        embed = discord.Embed(color=color)
        if thumbnail_url is not None:
            embed.set_thumbnail(url=thumbnail_url)
        if image_url is not None:
            embed.set_image(url=image_url)
        if title is not None:
            embed.title = title
        if description is not None:
            embed.description = description
        if fields:
            for (name, value, inline) in fields:
                embed.add_field(name=name, value=value, inline=inline)
        if timestamp is not None:
            embed.timestamp = datetime.datetime.now()
        self.pages.append(embed)

    async def send_pages(self, channel, author):
        self.channel = channel
        self.author = author
        for i, page in enumerate(self.pages):
            page.set_footer(text=f"Page {i+1}/{len(self.pages)}")
        self.message = await self.channel.send(embed=self.pages[0])
        if len(self.pages) > 1:
            for button in [self.backward, self.forward, self.delete]:
                await self.message.add_reaction(button)
        self.start_time = time.time()

    async def _change_pages(self):
        await self.message.edit(embed=self.pages[self.index])

    async def check_action(self, payload):
        if payload.member != self.author:
            return
        if time.time() - self.start_time >= self.timeout:
            self.state = '0'
        if str(payload.emoji) == self.forward:
            if self.index < len(self.pages) - 1:
                self.index += 1
                await self._change_pages()
        elif str(payload.emoji) == self.backward:
            if self.index > 0:
                self.index -= 1
                await self._change_pages()
        elif str(payload.emoji) == self.delete:
            await self.message.delete()
            self.state = "0"
