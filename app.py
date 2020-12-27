import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message
from self_reply import decide
import pydot

load_dotenv()


machine = TocMachine(
    states=["user_join", "wait_old", "wait_height","wait_weight","wait_gender","wait_sport"],
    transitions=[
        {
            "trigger": "input",
            "source": "user_join",
            "dest": "wait_old",
            "conditions": "Start",
        },
        {
            "trigger": "input",
            "source": "wait_old",
            "dest": "wait_height",
            "conditions": "0~150",
        },
        {
            "trigger": "input",
            "source": "wait_height",
            "dest": "wait_weight",
            "conditions": "0~300",
        },
        {
            "trigger": "input",
            "source": "wait_weight",
            "dest": "wait_gender",
            "conditions": "0~200",
        },
        {
            "trigger": "input",
            "source": "wait_gender",
            "dest": "wait_sport",
            "conditions": "男or女",
        },
        {
            "trigger": "input",
            "source": "wait_sport",
            "dest": "user_join",
            "conditions": "0~5000",
        },
        {
            "trigger": "input",
            "source": "wait_old",
            "dest": "wait_old",
            "conditions": "not in 0~150",
        },
        {
            "trigger": "input",
            "source": "wait_height",
            "dest": "wait_height",
            "conditions": "not in 0~300",
        },
        {
            "trigger": "input",
            "source": "wait_weight",
            "dest": "wait_weight",
            "conditions": "not in 0~200",
        },
        {
            "trigger": "input",
            "source": "wait_gender",
            "dest": "wait_gender",
            "conditions": "not 男or女",
        },
        {
            "trigger": "input",
            "source": "wait_sport",
            "dest": "wait_sport",
            "conditions": "not in 0~5000",
        },
        {"trigger": "input", "source": ["wait_height","wait_weight","wait_gender","wait_sport"], "dest": "wait_old","conditions":"Restart"},
    ],
    initial="user_join",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = "95ddc092f3a8e4f51dda8d4d0e043e08"
channel_access_token = "mFC8FpopMi8xVPR1JbRtaAfCNnyYCesTmpNRxtfhQQbGsmyDphUODmRSdX1gXpIRO9uV4PkLRKGQE5bW7Z0/0wsetr/rMSUd5szRHPpnoE2VOu109qNtqYYVcS5Fv351+tFZd2vkTv+/qHakTYF+ygdB04t89/1O/w1cDnyilFU="
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        decide(event.reply_token,event.message.text)
        

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")
@app.route("/")
def hello():
    
    print (pydot.find_graphviz())
    return "hello from python"


if __name__ == "__main__":
     
     
     port = os.environ.get("PORT", 8000)
     app.run(host="0.0.0.0", port=port, debug=True)
