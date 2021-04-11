#coding : utf-8

import os
import json
import random
import logging
import responder

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, FollowEvent, PostbackEvent, UnfollowEvent, TextMessage, TextSendMessage, FlexSendMessage,
                            RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction)

from db import LineCrud, SessionManager
from flex_message import password_generate

api = responder.API()

line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

line_crud = LineCrud()
session_mng = SessionManager()

@api.route("/callback")
async def on_post(req, resp):
    @api.background.task
    def handles():
        handler.handle(body, signature)

    signature = req.headers['X-Line-Signature']
    
    body = await req.media()
    body = json.dumps(body, ensure_ascii=False).replace(' ', '')

    try:
        handles()
        resp.status_code = 200
        resp.text = 'OK'
    except InvalidSignatureError as e:
        resp.status_code = 400
        resp.text = e

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

@handler.add(FollowEvent)
def following(event):
    pass

@handler.add(UnfollowEvent)
def unfollow(event):
    with session_mng.session_create() as session:
        line_crud.del_userinfo_block(session, event.source.user_id)

@handler.add(PostbackEvent)
def post_back(event):
    if event.postback.data == "register_server":
        with session_mng.session_create() as session:
            if line_crud.exists_line_user(session, event.source.user_id) == True:
                line_bot_api.push_message(event.source.user_id, TextSendMessage("既に登録用コマンドを発行済です！"))
            else:
                password = Line.password_gen()

                flex_message = password_generate

                flex_message["header"]["contents"][0]["text"] = "!dine add " + str(password)

                with session_mng.session_create() as session:
                    line_crud.add_following_to_password(session, event.source.user_id, password)

                line_bot_api.push_message(
                                event.source.user_id, 
                                [
                                    FlexSendMessage(alt_text="登録メッセージ", contents=flex_message),
                                    TextSendMessage("上記のコマンドを登録したいサーバーのDiscordチャットに入力してください！")
                                ]
                            )

    elif event.postback.data == "register_accept":
        with session_mng.session_create() as session:
            line_crud.accept_user(session, event.source.user_id)

        line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーへの登録が完了しました！"))
    
    elif event.postback.data == "register_deny":
        line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーへの登録を拒否しました。\n再度登録する場合はパスワードを再生成してください。"))

class Line():
    @staticmethod
    def password_gen():
        password = random.randint(100000, 999999)
        with session_mng.session_create() as session:
            if line_crud.exists_password(session, password) == True:
                return password_gen()
        return password

    def __create_richmenu(self):
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=2500, height=1686),
            selected = True,
            name = "dine_richmenu",
            chat_bar_text = "BOT設定はここ！",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                    action=PostbackAction(data="delete_server", display_text="サーバーを消したいよ！")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=843, width=1250, height=1686),
                    action=PostbackAction(data="setting_server", display_text="サーバーを設定したいよ！")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=0, width=2500, height=843),
                    action=PostbackAction(data="select_server", display_text="サーバを登録したいよ！")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=843, width=2500, height=1686),
                    action=PostbackAction(data="register_server", display_text="サーバーを選びたいよ！")
                )
            ]
        )
        
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)       

        with open("picture/richmenu.png", 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)           

        line_bot_api.set_default_rich_menu(richMenuId)    

    def begin(self):
        self.__create_richmenu()
        api.run(address="0.0.0.0", port=8000, debug=True, log_config=None)