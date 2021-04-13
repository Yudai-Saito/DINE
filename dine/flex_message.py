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

delete_server = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "nano",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "icon_url",
            "offsetTop": "none",
            "offsetBottom": "none",
            "offsetStart": "none",
            "offsetEnd": "none"
          }
        ],
        "paddingBottom": "none",
        "backgroundColor": "#AFEEEE",
        "paddingTop": "none"
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
            "margin": "xs"
          }
        ],
        "backgroundColor": "#AFEEEE",
        "paddingTop": "none"
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
              "data": "server_id"
            },
            "offsetTop": "none",
            "offsetBottom": "none"
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
  ]
}

delete_server_contents =     {
      "type": "bubble",
      "size": "nano",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "icon_url",
            "offsetTop": "none",
            "offsetBottom": "none",
            "offsetStart": "none",
            "offsetEnd": "none"
          }
        ],
        "paddingBottom": "none",
        "backgroundColor": "#AFEEEE",
        "paddingTop": "none"
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
            "margin": "xs"
          }
        ],
        "backgroundColor": "#AFEEEE",
        "paddingTop": "none"
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
              "data": "server_id"
            },
            "offsetTop": "none",
            "offsetBottom": "none"
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