from bot.constants import ADMINS


def is_admin(ctx):
    return ctx.message.author.id in ADMINS
