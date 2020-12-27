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
    cal=[1200,1500,1800,2000,2200,2500,2700]
    veg=[3,3,3,4,4,5,5]
    fru=[2,2,2,3,3,4,4]

def decide(re_token,text):
    
    if state.s==0 :
        if text=="Start" :
            state.s=state.s+1
            send_text_message(re_token, "請輸入您的年齡(0~150):")
        else:
            send_text_message(re_token, "如要開始服務，請輸入 Start")
    elif state.s==1: 
        try:
            n=(int)(text)
        except ValueError:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的年齡(0~150):")
        if (int)(text)>=0 and (int)(text)<150:
            state.old=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的身高(cm):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的年齡(0~150):")
    elif state.s==2:
        try:
            n=(int)(text)
        except ValueError:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的身高(0~300)(cm):")
        if (int)(text)>0 and (int)(text)<300:
            state.height=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的體重(kg):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的身高(0~300)(cm):")
    elif state.s==3:
        try:
            n=(int)(text)
        except ValueError:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的體重(0~200)(kg):")
        if (int)(text)>0 and (int)(text)<200:
            state.weight=(int)(text)
            state.s+=1
            send_text_message(re_token, "請輸入您的性別(男or女):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的體重(0~200)(kg):")
    elif state.s==4:
        if text=="男" or text=="女":
            state.gender=text
            state.s+=1
            send_text_message(re_token, "請輸入您平均一周的運動量(分鐘):")
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您的性別(男or女):")
    elif state.s==5:
        try:
            n=(int)(text)
        except ValueError:
            send_text_message(re_token, "輸入錯誤，請正確輸入您平均一周的運動量(分鐘):")
        if (int)(text)>=0 and (int)(text)<5000:
            state.movement=(int)(text)
            state.s+=1
            result(re_token)
            state.s=0
        else:
            send_text_message(re_token, "輸入錯誤，請正確輸入您平均一周的運動量(0~5000)(分鐘):")
    
        
    return
def result(re_token):
    reply=""
    reply="您的個人資料:\n年齡:"+(str)(state.old)+"\n身高:"+(str)(state.height)+"\n體重:"+(str)(state.weight)+"\n性別:"+(str)(state.gender)+"\n運動量:"+(str)(state.movement)+"\n"
    total_cal=0
    rice=0
    meat=0
    fruit=0
    veg=0
    milk=1.5
    oil=0
    if state.gender=="男":
        total_cal=13.7 * state.weight+5.0 * state.height -6.8 *state.old+66
    else:
        total_cal=9.6 * state.weight+1.8 * state.height -4.7 *state.old+655
    if state.movement>=150:
        total_cal=total_cal*(1.5+0.5*(state.movement-150)/(5000-150))
    else:
        total_cal=total_cal*1.2
    total_cal=(int)(total_cal+0.5)
    n=0
    if total_cal<state.cal[0]:
        n=0
    elif total_cal<state.cal[1]:
        n=1
    elif total_cal<state.cal[2]:
        n=2
    elif total_cal<state.cal[3]:
        n=3
    elif total_cal<state.cal[4]:
        n=4
    elif total_cal<state.cal[5]:
        n=5
    else:
        n=6
    fruit=state.fru[n]
    veg=state.veg[n]
    meat=(total_cal*0.2/4-milk*8)/7
    meat=(int)(meat+0.5)
    oil=(total_cal*0.3/9-milk*4)/5
    oil=(int)(oil+0.5)
    rice=(total_cal*0.5/4-milk*12-veg*5-fruit*15)/15/4
    rice=(int)(rice+0.5)
    
    reply=reply+"您的一天所需營養:\n"
    reply=reply+"熱量:"+(str)(total_cal)+"大卡\n"
    reply=reply+"全穀雜糧:"+(str)(rice)+"碗\n"
    reply=reply+"蛋豆魚肉:"+(str)(meat)+"份\n"
    reply=reply+"蔬菜:"+(str)(veg)+"份\n"
    reply=reply+"油脂:"+(str)(oil)+"茶匙\n"
    reply=reply+"水果:"+(str)(fruit)+"份\n"
    reply=reply+"乳製品:"+(str)(milk)+"杯"
    
    send_text_message(re_token,reply)
    
    
    
    
    return
