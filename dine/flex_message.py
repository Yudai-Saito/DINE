password_generate = {
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "setting password",
          "weight": "bold",
          "size": "xxl",
          "align": "center",
          "contents": []
        }
      ]
    }
  }

register_accept = {
  "type": "bubble",
  "direction": "ltr",
  "header": {
    "type": "box",
    "layout": "vertical",
    "backgroundColor": "#7FDEDBFF",
    "contents": [
      {
        "type": "text",
        "text": "server_name",
        "weight": "bold",
        "align": "center",
        "contents": []
      },
      {
        "type": "text",
        "text": "にLINEを登録しますか？",
        "weight": "bold",
        "align": "center",
        "contents": []
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "register_accept"
        },
        "margin": "xl",
        "height": "md",
        "position": "relative"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "register_deny"
        },
        "margin": "xxl",
        "height": "md",
        "gravity": "bottom",
        "position": "relative"
      }
    ]
  }
}