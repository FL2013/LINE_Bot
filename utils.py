import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = os.getenv("mFC8FpopMi8xVPR1JbRtaAfCNnyYCesTmpNRxtfhQQbGsmyDphUODmRSdX1gXpIRO9uV4PkLRKGQE5bW7Z0/0wsetr/rMSUd5szRHPpnoE2VOu109qNtqYYVcS5Fv351+tFZd2vkTv+/qHakTYF+ygdB04t89/1O/w1cDnyilFU=", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
