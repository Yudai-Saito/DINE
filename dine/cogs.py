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
        with self.session_mng.session_create() as session:
            if self.discord_crud.exists_password(session, password) == True:

                ctx.send("認証が完了しました！LINEで登録を完了させましょう！")
                
                with self.session_mng.session_create() as session:
                    self.discord_crud.add_register_to_password(session, password, ctx.author.id)

                with self.session_mng.session_create() as session:   
                    line_id = self.discord_crud.register_user(session, password)

                register_accept["header"]["contents"][0]["text"] = "\"{}\"".format(ctx.guild.name)

                line_bot_api.push_message(line_id, [
                                    FlexSendMessage(alt_text="登録メッセージ", contents=register_accept),
                                    TextSendMessage("登録リンクは5分間有効となります！\n時間が過ぎてしまったら再度パスワードを発行してください！")
                                ]
                            )
            else:
                await ctx.send("入力されたパスワードは存在しません！")

def setup(bot):
    return bot.add_cog(DineCog(bot))
