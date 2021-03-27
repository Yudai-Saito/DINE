#coding : utf-8

import os
import json
import random
import logging
import responder

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, TextMessage, TextSendMessage

from db import LineCrud

api = responder.API()

line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

line_crud = LineCrud()

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
    password = Line.password_gen()
    line_crud.add_following_to_password(event.source.user_id, password)

class Line():
    @staticmethod
    def password_gen():
        password = random.randint(1000,9999)
        if line_crud.exists_password(password) == True:
            return password_gen()
        return password

    def begin(self):
        api.run(address="0.0.0.0", port=8000, debug=True, log_config=None)