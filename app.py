# app.py
# =============庫==================

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, FlexSendMessage, LocationSendMessage, LocationMessage
)
# =============副程式==================

from function import (templates, spider2)

# =============變數==================
app = Flask(__name__)

line_bot_api = LineBotApi(
    '80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('adef5f3ce019ca875e5fe10c1dff3b15')

# ==========這裡基本不用動============


@app.route("/", methods=['GET'])
def test():
    return "ok"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# =============收到文字訊息==================


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("=============")
    test = templates()
    test.add_restaurant_bubble(
        "https://janstockcoin.com/wp-content/uploads/2021/06/pexels-photo-747964-scaled.jpeg", "name", "rating", "add", "open")
    # test.add_restaurant_bubble("test2", "456")

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage("flex", test.template)
    )
# ========================================================若是位置訊息


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    restaurants = spider2(event.message.latitude, event.message.longitude)
    print(restaurants)
    rtTemplate = templates()
    for i, d in enumerate(restaurants):
        # print("+"*20)
        # print(d['resPhoto'])
        # print("+"*20)
        try:
            rtTemplate.add_restaurant_bubble(
                d['resPhoto'], d['resName'], d['resRating'], d["resAdd"], d["resOpen"])
        except Exception as e:
            print(e)
        if i > 8:
            break

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage("flex", rtTemplate.template)
    )


if __name__ == "__main__":
    app.run(port=8080)
