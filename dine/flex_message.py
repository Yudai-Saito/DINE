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

carousel_message = {
  "type": "carousel",
  "contents": [
  ]
}

delete_server_contents = {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://example.com/",
            "size": "full",
            "margin": "sm"
          }
        ],
        "paddingBottom": "none",
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "server_name",
            "align": "center",
            "position": "relative",
            "weight": "bold",
            "size": "md",
            "margin": "md"
          }
        ],
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "解除する",
              "data": "delete,server_id"
            }
          }
        ],
        "paddingTop": "none",
        "paddingBottom": "none"
      },
      "styles": {
        "footer": {
          "separator": False
        }
      }
    }

setting_contens = {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://example.com/",
            "size": "full",
            "margin": "sm"
          }
        ],
        "paddingBottom": "none",
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "server_name",
            "align": "center",
            "position": "relative",
            "weight": "bold",
            "size": "md",
            "margin": "md"
          }
        ],
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "メッセージ通知",
            "align": "center"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "オン",
              "data": "setting_text,server_id"
            },
            "style": "secondary"
          },
          {
            "type": "text",
            "text": "ボイチャ通知",
            "align": "center"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "オン",
              "data": "setting_vc,server_id"
            },
            "style": "secondary"
          }
        ],
        "spacing": "md"
      },
      "styles": {
        "footer": {
          "separator": False
        }
      }
    } 

select_contents = {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://example.com/",
            "size": "full",
            "margin": "sm"
          }
        ],
        "paddingBottom": "none",
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "server_name",
            "align": "center",
            "position": "relative",
            "weight": "bold",
            "size": "md",
            "margin": "md"
          }
        ],
        "paddingTop": "none",
        "backgroundColor": "#AFEEEE"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "選択する",
              "data": "select,server_id"
            }
          }
        ],
        "paddingTop": "none",
        "paddingBottom": "none"
      },
      "styles": {
        "footer": {
          "separator": False
        }
      }
    }