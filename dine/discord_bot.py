#coding : utf-8

import os
import re
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
 
        for channel in guild.channels:
            if type(channel) is discord.TextChannel:
                await channel.send("DINEへようこそ！\nLINEメッセージを受信するチャンネルで!dine channelコマンドを実行してください！")
                return

    async def on_webhooks_update(self, channel):
        await self.on_webhook_delete(channel)
        
    async def on_guild_channel_delete(self, channel):
        await self.on_webhook_delete(channel)

    async def on_webhook_delete(self, channel): 
        webhook_lists = await channel.guild.webhooks()

        with self.session_mng.session_create() as session:
            server_webhook = self.discord_crud.get_webhook_id(session, str(channel.guild.id))

        for webhook in webhook_lists:
            webhook = re.sub("\D", "", str(webhook.id))
            if server_webhook[0] == webhook: 
                return

        with self.session_mng.session_create() as session:
            self.discord_crud.set_webhook_id(session, str(channel.guild.id), None)

        for channel in channel.guild.channels:
            if type(channel) is discord.TextChannel:
                await channel.send("設定されているwebhookが削除されました！\nLINEを受信するには !dine channel コマンドで受信チャンネルを設定してください！")
                return

    async def on_guild_remove(self, guild):
        with self.session_mng.session_create() as session:
            self.discord_crud.delete_server(session, str(guild.id))
    
    def begin(self):
        self.run(os.environ["DISCORD_TOKEN"])