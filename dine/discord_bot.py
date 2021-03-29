#coding : utf-8

import os
import discord
from discord.ext import commands

from db import DiscordCrud, SessionManager

class Dine(commands.Bot):
    def __init__(self):
        super().__init__("!")
        
        self.discord_crud = DiscordCrud()
        self.session_mng = SessionManager()
    
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game("dine!"))

    async def on_guild_join(self, guild):
        with self.session_mng.session_create() as session:
            self.discord_crud.add_join_server(session, guild.id)

    def begin(self):
        self.run(os.environ["DISCORD_TOKEN"])