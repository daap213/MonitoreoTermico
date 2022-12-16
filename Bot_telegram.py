import requests
import socket

apiToken = '5858757321:AAFPFv5JkG6MfDWgzKLg1Su6DXT6KWVRAPM'
chatID = '-1001685279523'

def mensaje_telegram(mensaje):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(("www.google.com", 80))
    except (socket.gaierror, socket.timeout):
        print("Sin conexión a internet")
        s.close()
    else:
        print("Con conexión a internet")
        s.close()
        
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        try:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': mensaje})
        except Exception as e:
            print(e)

def imagen_telegram(image,text=""):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(("www.google.com", 80))
    except (socket.gaierror, socket.timeout):
        print("Sin conexión a internet")
        s.close()
    else:
        print("Con conexión a internet")
        s.close()
        
        apiURL =  f'https://api.telegram.org/bot{apiToken}/sendPhoto?chat_id={chatID}&caption={text}'
        files = {'photo':image}
        try:
            response = requests.post(apiURL,files=files)
        except Exception as e:
            print(e)
