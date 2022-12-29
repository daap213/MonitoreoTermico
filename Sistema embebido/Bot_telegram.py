import requests
import socket
import time


apiToken = '5858757321:AAFPFv5JkG6MfDWgzKLg1Su6DXT6KWVRAPM'
chatID = '-1001685279523'

def mensaje_telegram(mensaje, reconectar=False,intentos =10):
    estado = "espera"
    i = 0
    while (not estado == "Enviado") and (i<=intentos) and reconectar:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect(("www.google.com", 80))
        except (socket.gaierror, socket.timeout):
            estado = "Error"
            print("Sin conexión a internet")
            s.close()
            
        else:
            print("Con conexión a internet")
            s.close()
            
            apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

            try:
                
                response = requests.post(apiURL, json={'chat_id': chatID, 'text': mensaje})
                estado = "Enviado"
            except Exception as e:
                estado = "Error"
                print(e)
                
        i = 1+i
        time.sleep(1)
    return estado
    

def imagen_telegram(image,text="", reconectar=False,intentos =10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(("www.google.com", 80))
    except (socket.gaierror, socket.timeout):
        print("Sin conexión a internet")
        s.close()
        return "Error"
    else:
        print("Con conexión a internet")
        s.close()
        
        apiURL =  f'https://api.telegram.org/bot{apiToken}/sendPhoto?chat_id={chatID}&caption={text}'
        files = {'photo':image}
        try:
            response = requests.post(apiURL,files=files)
        except Exception as e:
            print(e)
            return "Error"
    return "Enviado"

def stiker_telegram(id_Stiker, reconectar=False,intentos =10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(("www.google.com", 80))
    except (socket.gaierror, socket.timeout):
        print("Sin conexión a internet")
        s.close()
        return "Error"
    else:
        print("Con conexión a internet")
        s.close()
        
        apiURL =  f'https://api.telegram.org/bot{apiToken}/sendSticker?chat_id={chatID}&sticker={id_Stiker}'
        try:
            response = requests.post(apiURL)
        except Exception as e:
            print(e)
            return "Error"
    return "Enviado"
