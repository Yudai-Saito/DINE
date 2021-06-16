#coding : utf-8

import os
import json
import random
import logging
import requests
import responder
import copy

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, FollowEvent, PostbackEvent, UnfollowEvent, TextMessage, TextSendMessage, FlexSendMessage,
                            RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction)

from db import LineCrud, SessionManager
from flex_message import password_generate, carousel_message, delete_server_contents, setting_contens, select_contents

BASE_URL = "https://discord.com/api"
HADER = {"Authorization":"Bot {}".format(os.environ["DISCORD_TOKEN"])}

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
    with session_mng.session_create() as session:
        webhook_id = line_crud.get_webhook_id(session, event.source.user_id) 

    if webhook_id == None:
       line_bot_api.push_message(event.source.user_id, TextSendMessage("送信先サーバーを選択してください！"))     
       return     

    with session_mng.session_create() as session:
        user = line_crud.get_discord_user(session, event.source.user_id) 

    user_info = json.loads(requests.get("{}/users/{}".format(BASE_URL, user), headers=HADER).text)
    avatar_url = "https://cdn.discordapp.com/avatars/{}/{}.jpg".format(user_info["id"], user_info["avatar"])

    webhook_contents = {
        "username" : user_info["username"],
        "avatar_url" : avatar_url,
        "content" : event.message.text
    }

    webhook_info = json.loads(requests.get("{}/webhooks/{}".format(BASE_URL, webhook_id), headers=HADER).text)
    webhook_url =  "{}/webhooks/{}/{}".format(BASE_URL, webhook_info["id"], webhook_info["token"])

    res = requests.post(webhook_url, webhook_contents)

    with session_mng.session_create() as session:
        line_crud.set_talk_time(session, event.source.user_id)

@handler.add(FollowEvent)
def following(event):
    with session_mng.session_create() as session:
        line_crud.add_following_user(session, event.source.user_id)

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

    elif event.postback.data == "delete_server":
        with session_mng.session_create() as session:
            servers = line_crud.get_server_id(session, event.source.user_id)

        if len(servers) > 0:
            delete_flex_message = copy.deepcopy(carousel_message)
            delete_flex_message_contents = copy.deepcopy(delete_server_contents)

            for server in servers:
                res = requests.get("{}/guilds/{}".format(BASE_URL, str(server[0])), headers=HADER)
                server_info = json.loads(res.text)

                delete_flex_message_contents["hero"]["contents"][0]["url"] = "https://cdn.discordapp.com/icons/{}/{}.png".format(str(server_info["id"]), str(server_info["icon"]))
                delete_flex_message_contents["body"]["contents"][0]["text"] = server_info["name"]
                delete_flex_message_contents["footer"]["contents"][0]["action"]["data"] = "delete,{}".format(server_info["id"])

                delete_flex_message["contents"].append(copy.deepcopy(delete_flex_message_contents))

            line_bot_api.push_message(event.source.user_id, FlexSendMessage(alt_text="登録メッセージ", contents=delete_flex_message))
        else:
            line_bot_api.push_message(event.source.user_id, TextSendMessage("登録してるサーバーが１つもありません！"))

    elif event.postback.data == "setting_server":
        with session_mng.session_create() as session:
            servers = line_crud.get_server_id(session, event.source.user_id)

        if len(servers) > 0:
            setting_flex_message = copy.deepcopy(carousel_message)
            setting_flex_message_contents = copy.deepcopy(setting_contens)

            for server in servers:
                res = requests.get("{}/guilds/{}".format(BASE_URL, server[0]), headers=HADER)
                server_info = json.loads(res.text)

                with session_mng.session_create() as session:
                    if line_crud.get_server_text(session, event.source.user_id, server[0]) == True:
                        setting_flex_message_contents["footer"]["contents"][1]["action"]["label"] = "オフ にする"
                    elif line_crud.get_server_text(session, event.source.user_id, server[0])  == False:
                        setting_flex_message_contents["footer"]["contents"][1]["action"]["label"] = "オン にする"
                
                with session_mng.session_create() as session:
                    if line_crud.get_server_voice(session, event.source.user_id, server[0]) == True:
                        setting_flex_message_contents["footer"]["contents"][3]["action"]["label"] = "オフ にする"
                    elif line_crud.get_server_voice(session, event.source.user_id, server[0])  == False:
                        setting_flex_message_contents["footer"]["contents"][3]["action"]["label"] = "オン にする"

                setting_flex_message_contents["hero"]["contents"][0]["url"] = "https://cdn.discordapp.com/icons/{}/{}.png".format(str(server_info["id"]), str(server_info["icon"]))
                setting_flex_message_contents["body"]["contents"][0]["text"] = server_info["name"]
                setting_flex_message_contents["footer"]["contents"][1]["action"]["data"] = "setting_text,{}".format(server_info["id"])
                setting_flex_message_contents["footer"]["contents"][3]["action"]["data"] = "setting_vc,{}".format(server_info["id"])

                setting_flex_message["contents"].append(copy.deepcopy(setting_flex_message_contents))

            line_bot_api.push_message(event.source.user_id, FlexSendMessage(alt_text="設定メッセージ", contents=setting_flex_message))
        else:
            line_bot_api.push_message(event.source.user_id, TextSendMessage("登録してるサーバーが１つもありません！"))

    elif event.postback.data == "select_server":
        with session_mng.session_create() as session:
            servers = line_crud.get_server_id(session, event.source.user_id)

        if len(servers) > 0:
            select_flex_message = copy.deepcopy(carousel_message)
            select_flex_message_contents = copy.deepcopy(select_contents)

            for server in servers:
                res = requests.get("{}/guilds/{}".format(BASE_URL, server[0]), headers=HADER)
                server_info = json.loads(res.text)

                select_flex_message_contents["hero"]["contents"][0]["url"] = "https://cdn.discordapp.com/icons/{}/{}.png".format(str(server_info["id"]), str(server_info["icon"]))
                select_flex_message_contents["body"]["contents"][0]["text"] = server_info["name"]
                select_flex_message_contents["footer"]["contents"][0]["action"]["data"] = "select,{}".format(server_info["id"])

                select_flex_message["contents"].append(copy.deepcopy(select_flex_message_contents))

            line_bot_api.push_message(event.source.user_id, FlexSendMessage(alt_text="選択メッセージ", contents=select_flex_message))
        else:
            line_bot_api.push_message(event.source.user_id, TextSendMessage("登録してるサーバーが１つもありません！"))

    elif event.postback.data == "register_accept":
        with session_mng.session_create() as session:
            line_crud.accept_user(session, event.source.user_id)
        
        with session_mng.session_create() as session:
            line_crud.set_user_info(session, event.source.user_id)
        
        line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーへの登録が完了しました！"))
    
    elif event.postback.data == "register_deny":
        line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーへの登録を拒否しました。\n再度登録する場合はパスワードを再生成してください。"))

    else:
        data = event.postback.data.split(",")
        if data[0] == "delete":
            with session_mng.session_create() as session:
                line_crud.delete_server(session, event.source.user_id, data[1])
            line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーとの連携を解除しました！"))

        if data[0] == "setting_text":
            with session_mng.session_create() as session:
                text_notice = line_crud.setting_server_text(session, event.source.user_id, data[1])

            if text_notice == True:
                notice_message = "オン"
            elif text_notice == False:
                notice_message = "オフ"

            line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーのメッセージ通知を {} にしました！".format(notice_message)))

        if data[0] == "setting_vc":
            with session_mng.session_create() as session:
                text_notice = line_crud.setting_server_voice(session, event.source.user_id, data[1])
            
            if text_notice == True:
                notice_message = "オン"
            elif text_notice == False:
                notice_message = "オフ"

            line_bot_api.push_message(event.source.user_id, TextSendMessage("サーバーのボイスチャット通知を {} にしました！".format(notice_message)))
        
        if data[0] == "select":
            with session_mng.session_create() as session:
                line_crud.set_user_talk_server(session, event.source.user_id, data[1])

            line_bot_api.push_message(event.source.user_id, TextSendMessage("メッセージ送信先のサーバーを変更しました！"))

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
                    action=PostbackAction(data="register_server", display_text="サーバを登録したいよ！")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=843, width=2500, height=1686),
                    action=PostbackAction(data="select_server", display_text="サーバーを選びたいよ！")
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