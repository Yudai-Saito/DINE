#coding : utf-8
import discord
from discord.ext import commands

from db import DiscordCrud, SessionManager
from line_bot import line_bot_api
from linebot.models import TextSendMessage, FlexSendMessage
from flex_message import register_accept

import os
import re
from linebot import LineBotApi          
from linebot.models import TextSendMessage

line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])

class DineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_crud = DiscordCrud()
        self.session_mng = SessionManager()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            with self.session_mng.session_create() as session:
                prefix = self.discord_crud.get_prefix(session, message.guild.id)
            await message.channel.send("サーバーのprefixは {} です！".format(prefix))

    @commands.command()
    async def dine(self, ctx, *args):
        command = args[0] 

        if command == "prefix":
            await self.prefix(ctx, args[1])
        elif command == "channel":
            await self.channel(ctx)
        elif command == "add": 
            await self.add(ctx, args[1])
        else:
            try:
                index = args.index(",")
                discord_user_id = [re.sub("\D+", "", x) for x in args[:index]]
                message = "".join(map(str, args[index + 1:]))

                with self.session_mng.session_create() as session:
                    line_users = self.discord_crud.get_line_id(session, str(ctx.guild.id), discord_user_id)

                line_send_message = ("[{}]\n[{}]\n{}".format(ctx.guild.name, ctx.author.name, message))
                line_bot_api.multicast(list(line_users[0]), TextSendMessage(line_send_message)) 
            except:
                await ctx.send("入力に誤りがあります！")

    async def prefix(self, ctx, prefix):
        if ctx.author.guild_permissions.administrator:
            if len(prefix) == 1:
                with self.session_mng.session_create() as session:
                    self.discord_crud.set_prefix(session, ctx.guild.id, prefix)
                await ctx.send("prefixを変更しました！")
            else:
                await ctx.send("prefixは1文字で設定してください！")
        else:
            await ctx.send("管理者用コマンドです！")

    async def channel(self, ctx):
        if ctx.author.guild_permissions.administrator:
            with self.session_mng.session_create() as session:
                delete_webhook = self.discord_crud.get_webhook_id(session, str(ctx.guild.id))

            webhook = await ctx.message.channel.create_webhook(name="Dine_Webhook")

            with self.session_mng.session_create() as session:
                self.discord_crud.set_webhook_id(session, str(ctx.guild.id), str(webhook.id))

            if delete_webhook[0] != None:
                delete_webhook = discord.utils.get(await ctx.guild.webhooks(), id=int(delete_webhook[0]))
                await delete_webhook.delete()

            await webhook.send("LINE受信チャンネルの設定が完了しました！")
        else:
            await ctx.send("管理者用コマンドです！")

    async def add(self, ctx, password):
        with self.session_mng.session_create() as session:
            if self.discord_crud.exists_user(session, ctx.guild.id, ctx.author.id) == False:
                with self.session_mng.session_create() as session:
                    if self.discord_crud.exists_password(session, password) == True:

                        await ctx.send("認証が完了しました！LINEで登録を完了させましょう！")

                        with self.session_mng.session_create() as session:
                            self.discord_crud.add_register_to_password(session, password, ctx.author.id, ctx.guild.id)

                        with self.session_mng.session_create() as session:   
                            line_id = self.discord_crud.register_user(session, password)

                        flex_message = register_accept

                        flex_message["header"]["contents"][0]["text"] = "\"{}\"".format(ctx.guild.name)

                        line_bot_api.push_message(line_id, [
                                            FlexSendMessage(alt_text="登録メッセージ", contents=flex_message),
                                            TextSendMessage("登録リンクは5分間有効となります！\n時間が過ぎてしまったら再度パスワードを発行してください！")
                                        ]
                                    )
                    else:
                        await ctx.send("入力されたパスワードは使用済みか存在しません！")
            else:
                await ctx.send("このサーバーには既に登録済みです！")

def setup(bot):
    return bot.add_cog(DineCog(bot))
