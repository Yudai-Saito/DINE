#coding : utf-8

import os
import discord
from discord.ext import commands

from db import DiscordCrud, SessionManager

class Dine(commands.Bot):
    def __init__(self):
        super().__init__(self.server_prefix)

        self.load_extension("cogs")

        self.discord_crud = DiscordCrud()
        self.session_mng = SessionManager()

    async def server_prefix(self, bot, message):
        with self.session_mng.session_create() as session:
            return self.discord_crud.get_prefix(session, message.guild.id)
    
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game("dine!"))

    async def on_guild_join(self, guild):
        with self.session_mng.session_create() as session:
            self.discord_crud.add_join_server(session, guild.id)
        
        for channnel in guild.channels:
            if type(channnel) is discord.TextChannel:
                with self.session_mng.session_create() as session:
                    self.discord_crud.set_channel_id(session, str(guild.id), str(channnel.id))
                await channnel.send("DINEへようこそ！\nLINEメッセージの受信チャンネル変更は!dine channelコマンドを使ってください！")
                return
            
    async def on_guild_remove(self, guild):
        with self.session_mng.session_create() as session:
            self.discord_crud.delete_server(session, str(guild.id))
    
    def begin(self):
        self.run(os.environ["DISCORD_TOKEN"])