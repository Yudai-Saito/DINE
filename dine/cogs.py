#coding : utf-8

from discord.ext import commands

from db import DiscordCrud, SessionManager
from line_bot import line_bot_api
from linebot.models import TextSendMessage, FlexSendMessage
from flex_message import register_accept

class DineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_crud = DiscordCrud()
        self.session_mng = SessionManager()

    @commands.group()
    async def dine(self, ctx):
        pass

    @dine.command()
    async def add(self, ctx, password):
        pass

def setup(bot):
    return bot.add_cog(DineCog(bot))
