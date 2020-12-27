from utils import send_text_message
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

class state:
    s = 0
    old=0
    weight=0
    height=0
    gender=""
    movement=0

def decide(re_token,text):
    
    if state.s==0 :
        if text=="Start" :
            state.s=state.s+1
            send_text_message(re_token, "請輸入您的年齡(0~150):")
        else:
            send_text_message(re_token, "如要開始服務，請輸入 Start")
    elif state.s==1: 
        if (int)(text)>0 and (int)(text)<150:
            state.old=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的身高(cm):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的年齡(0~150):")
    elif state.s==2:
        if (int)(text)>0 and (int)(text)<300:
            state.height=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的體重(kg):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的身高(0~300)(cm):")
    elif state.s==3:
        if (int)(text)>0 and (int)(text)<200:
            state.weight=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的性別(男or女):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的體重(0~200)(cm):")
    elif state.s==4:
        if text=="男" or text=="女":
            state.gender=text
            state.s+=1
            send_text_message(re_token, "請輸入您平均一周的運動量(分鐘):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的性別(男or女):")
    elif state.s==5:
        if (int)(text)>0 and (int)(text)<8400:
            state.movement=(int)(text)
            state.s+=1
            result(re_token)
            state.s=0
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您平均一周的運動量(分鐘):")
    
        
    return
def result(re_token):
    reply="年齡:"+state.old+"\n身高:"+state.height+"\n體重:"+state.weight+"\n性別:"+state.gender+"\n運動量:"+state.movement
    send_text_message(re_token, reply)
    return
