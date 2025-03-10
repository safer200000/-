# !/usr/bin/python
# coding=utf-8


import requests, json, random
import telebot
from time import sleep

bot = telebot.TeleBot("")

#! YOUR USERNAME AND PASSWORD (my.rade.ir)
username = ""
password = ""

#! 
admins = ['111111', '22222']
#!

datacard = []
dicdatacard = {}



#Headers
rade_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host': 'api.rade.ir',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://my.rade.ir',
    'Connection': 'keep-alive',
}

entertainment = ['برای حمایت از ما میوه بخرید ازمون',
'میوه فروشی ما 24 ساعته بازه',
'من شبیه میمون نیستم میمون شبیه منه',
'مو هام شبیه گوسفنده ولی گوسفند نیستم',
'اف کورس که اطلاعات و کد ملی منو همه دارن',
'خیار های میوه فروشی ما سریع تموم میشه پس رزرو کنید',
'معین جعفرلو هستم',
'سلام',
'شمارمو بزن آشنا شیم : ۰۹۹۳۹۳۰۰۹۳۴',
'کد پسنی میدم برام خیار پست کنید مادرم میخواد ۵۸۵۱۵۹۵۳۶۸۹',
'میدونی چند سالمه ؟ ۱۳۸۳/۰۳/۱۶',
'کوچه پوراحمد ۵ پلاک ۵ خونم اینجاست',
'راستی میدونستی اسم بابام احده ؟',
'میدونستی من معین جعفر لو هستم پسر احد ؟',
'میدونستی من موقعی که خرابم مادرم خونه نیست ؟',
'اگه خراب بودم دوباره شماره کارتتو برام بفرست',
'به نظرت اسم معین با فامیلیه جعغر لو به عکسم میاد ؟',
'معین جعفر لولو 😈',
'میدونستی مادرم خرج کل خانواده جغفر لو رو میده و میوه فروشی فقط یه پوششه ؟']



session = requests.session()

#Defs
def login():
    try:
        global rade_headers
        
        csrf = session.get('https://api.rade.ir/api/v2/csrf-cookie', headers=rade_headers, verify=False, timeout=10)
        rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in csrf.cookies])

        payload = {
        "username":f"{username}",   
        "password":f"{password}",
        "captcha":"",
        "reference":None
        }

        resc = session.post('https://api.rade.ir/api/v2/checkExist', json={"username": f"{username}", "reference":None}, headers=rade_headers, verify=False, timeout=10)
        rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in resc.cookies])
        res = session.post('https://api.rade.ir/api/v2/login', json=payload, headers=rade_headers, verify=False)
        rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in res.cookies])
        if res.status_code == 200:
            return True
        else:
            return False
        
    except Exception as e:
        print(e)
    

def get_card_information(card):
    global rade_headers
    try:

        payload = {
            'card_number':	f"{card}"
        }

        response = session.post('https://api.rade.ir/api/v2/service/cardToIban', json=payload, headers=rade_headers, timeout=10)
        if response.status_code == 200:
            print(response.text)
            jsondata = json.loads(response.text)
            return jsondata['data']
        else:
           print(response.text)
           login()
           return False
        
    except Exception as e:
        print(e)
        

def get_shaba_information(shaba):
    global rade_headers
    try:
        
        payload = {
            'iban':	f"{shaba}"
        }

        response = session.post('https://api.rade.ir/api/v2/service/ibanInquiry', json=payload, headers=rade_headers, timeout=10)
        if response.status_code == 200:
            print(response.text)
            jsondata = json.loads(response.text)
            return jsondata['data']
        else:
           print(response.text)
           login()
           return False
        
    except Exception as e:
        print(e)
        



def getInfo(card):
    try:

        global dicdatacard, datacard
        if card.isdigit():
            if str(card) in datacard: 
                print("iam in the list")
                return dicdatacard[card] 
            else:    
                resultt = get_card_information(card)
                print(resultt)
                if resultt:
                    dicdatacard[f"{card}"] = resultt
                    datacard.append(str(card))
                    return resultt
                else:
                    return False
        else:
            return False
        
    except Exception as e:
        print(e)

def getInfoShaba(shaba):
    try:

        global dicdatacard, datacard
        if shaba.isdigit():
            if str(shaba) in datacard: 
                print("iam in the list")
                return dicdatacard[shaba] 
            else:    
                resultt = get_shaba_information(shaba)
                print(resultt)
                if resultt:
                    dicdatacard[f"{shaba}"] = resultt
                    datacard.append(str(shaba))
                    return resultt
                else:
                    return False
        else:
            return False
        
    except Exception as e:
        print(e)





def getText(shaba, hesab, fullName, bankName):
    text = f'''
🏦 #{bankName}
👤 OwnerName: <code>{fullName}</code>
🗂 Shabah: <code>{shaba}</code>
🔘 Hesab: <code>{hesab}</code>

🖥📱Developer By @MrXnxVip

{random.choice(entertainment)}
'''
    return text



def GetCard(message):
    try:

        chat_id = message.chat.id
        text = message.text.split('card_')[1]

        result = getInfo(text)
        if result != False:
            shaba = result['result']['result']['IBAN']
            fullName = result['result']['result']['depositOwners']
            hesab = result['result']['result']['deposit']
            bankEnum = result['result']['result']['bankEnum']
            myText = getText(shaba, hesab, fullName, bankEnum)

            bot.send_message(chat_id, text=myText, parse_mode='html')
        else:
            bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")
    
    except Exception as e:
        print(e)



def GetShaba(message):
    try:

        chat_id = message.chat.id
        text = message.text.split('shaba_')[1]

        result = getInfoShaba(text)
        if result != False:
            fullName = result['result']['result']['depositOwners']
            hesab = result['result']['result']['deposit']
            bankEnum = result['result']['result']['bankEnum']
            myText = getText(text, hesab, fullName, bankEnum)

            bot.send_message(chat_id, text=myText, parse_mode='html')
        else:
            bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")
    
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    well = '''
سلام اسم من معین جعفر لو هست پسر احد میوه ای

/shaba_
/card_

متولد : ۱۳۸۳/۰۳/۱۶
کد ملیم : ۲۷۹۱۱۱۶۵۶۷
کد پستیم : ۵۸۵۱۵۹۵۳۶۸۹
'''  
    bot.reply_to(message, well)



@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        if message.content_type == "text":  
            chat_id = message.chat.id
            if str(chat_id) in admins:
                #*Mellat
                if message.text.startswith("610433") or message.text.startswith("991975"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Mellat")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")
                #*Meli
                elif message.text.startswith("603799") or message.text.startswith("170019") or message.text.startswith("589905"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Meli")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*SanatMadan
                elif message.text.startswith("627961"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "SanatMadan")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Keshavarzi
                elif message.text.startswith("603770") or message.text.startswith("639217"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Keshavarzi")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Maskan
                elif message.text.startswith("628023"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Maskan")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Post_bank_iran
                elif message.text.startswith("627760"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Post_bank_iran")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*tosee_taavon
                elif message.text.startswith("502908"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "tosee_taavon")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*eghtsad_novin
                elif message.text.startswith("627412"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "eghtsad_novin")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*parsian
                elif message.text.startswith("622106") or message.text.startswith("639194") or message.text.startswith("627884"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "parsian")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")


                #*pasargad
                elif message.text.startswith("502229") or message.text.startswith("639347"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "pasargad")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                
                #*kar_afarin
                elif message.text.startswith("627488") or message.text.startswith("502910"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "kar_afarin")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                          
                #*Sina
                elif message.text.startswith("639346"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Sina")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                               
                #*Sarmaye
                elif message.text.startswith("639607"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Sarmaye")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Ayande
                elif message.text.startswith("636214"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Ayande")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Shahr
                elif message.text.startswith("502806") or message.text.startswith("504706"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Shahr")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Day
                elif message.text.startswith("502938"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Day")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                
                #*Saderat
                elif message.text.startswith("603769"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Saderat")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")


                #*Tejarat
                elif message.text.startswith("585983"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Tejarat")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*Refah
                elif message.text.startswith("589463"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Refah")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*ansar
                elif message.text.startswith("627381"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "ansar")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                
                #*iran_zamin
                elif message.text.startswith("505785"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "iran_zamin")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                     
                #*Markazi
                elif message.text.startswith("636795"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "Markazi")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*qarzolhasane_iran
                elif message.text.startswith("606373"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "qarzolhasane_iran")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")

                #*BlueBank / Saman
                elif message.text.startswith("621986"):
                    result = getInfo(message.text)
                    if result != False:
                        shaba = result['result']['result']['IBAN']
                        fullName = result['result']['result']['depositOwners']
                        hesab = result['result']['result']['deposit']
                        myText = getText(shaba, hesab, fullName, "BlueBank")

                        print(shaba)
                        bot.send_message(chat_id, text=myText, parse_mode='html')
                    else:
                        bot.send_message(chat_id=chat_id, text="سلام معین خرابه مثل همونی که خودت میدونی")


                elif message.text.startswith("/card"):
                    GetCard(message)

                elif message.text.startswith("/shaba"):
                    GetShaba(message)

                   
            else:
                bot.send_message(chat_id=chat_id, text="سلام معین توی این گروه کار نمیکنه")

    except Exception as e:
        print(e)


bot.infinity_polling()
   
