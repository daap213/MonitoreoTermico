import tkinter as tk
import tkinter.font as fnt
from PIL import Image
from PIL import ImageTk
import cv2
import os
import time
import Bot_telegram

fecha = time.ctime()
fecha = fecha.split()
dia = fecha[0]+"_"+fecha[1]+"_"+fecha[2]+"_"+fecha[4]
path = os.getcwd()
Datos = path+'/'+dia
estado = "Inicio"
clasificador = cv2.CascadeClassifier('cascade.xml')

captura = None
Imagen_ref = None 

def referencia():
    A = time.ctime()
    A = A.split()
    hora = A[3].replace(':', '_')
    return hora

def guardar_captura(ventana2 ):
        if not os.path.exists(Datos):
            print('Carpeta creada: ',Datos)
            os.makedirs(Datos)
        count =  referencia()  
        cv2.imwrite(Datos + "/image" + str(count) + ".jpg", ventana2)
        print("Guardo captura")
        #imagen = open(Datos+ "/image" + str(count) + ".jpg", 'rb')
        #Bot_telegram.imagen_telegram(imagen,"image" + str(count) + ".jpg")
        #print("Enviando imagen")

def reconocimientoObj(ventana):
    global Imagen_ref
    gris = cv2.cvtColor(ventana, cv2.COLOR_BGR2GRAY)
    caras = clasificador.detectMultiScale(gris, 5, 70,minSize=(75,75),maxSize=(350,350))
    ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    if not (len(caras) == 0):
        Imagen_ref = ventana
        guardar_captura(ventana)
    return ventana

def capturar():
    global Imagen_ref
    guardar_captura(Imagen_ref)

def monitoreoAuto():
    global captura
    btnRadio1.configure(state="disabled")
    boton.configure(state="active")
    boton2.configure(state="disabled")
    btnRadio2.configure(state="active")
    captura = cv2.VideoCapture(0) 
    visualizarVideo()
    
def VideoTermo():
    global Imagen_ref
    captura.release()
    boton.configure(state="active")
    boton2.configure(state="active")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="disabled")
    lblVideo.configure(image=fondo2)
    lblVideo.image = fondo2
    #Imagen_ref = 
    
def verResultado():
    seleccionado.set(0)
    captura.release()
    cv2.destroyAllWindows()
    lblVideo.configure(image=fondo)
    lblVideo.image = fondo
    boton.configure(state="disabled")
    boton2.configure(state="disabled")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="active")
    Bot_telegram.mensaje_telegram("Analisando capturas")

def visualizarVideo():
    global captura
    ret, ventana = captura.read()
    if ret == True:
        ventana = cv2.resize(ventana, (640, 480)) 
        ventana = reconocimientoObj(ventana)
        im = Image.fromarray(ventana)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizarVideo)


root = tk.Tk()
root.title("Monitoreo Térmico")
window_width = 640
window_height = 525
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

tamaño = fnt.Font(size = 12)
seleccionado = tk.IntVar()
lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=0, columnspan=2,rowspan=40,sticky ="NWES")

boton = tk.Button(root, text="Ver resultados",bd = '5',font = tamaño, state="active", command=verResultado)
boton.grid(column=1, row=41, pady=3, sticky ="NWES")

boton2 = tk.Button(root, text="Tomar captura",bd = '5',font = tamaño, state="disabled", command=capturar)
boton2.grid(column=0,row=41, pady=3,sticky ="NWES")

btnRadio1 = tk.Radiobutton(root, text="Automático", variable=seleccionado,
                        bd = '3',value = 1, indicator = 0,
                        font = tamaño, state="active", command=monitoreoAuto)
btnRadio1.grid(column=0, row=0,sticky ="NWE")

btnRadio2 = tk.Radiobutton(root, text="Manual", variable=seleccionado,
                        bd = '3',value = 2, indicator = 0,
                        font = tamaño, state="active", command=VideoTermo)
btnRadio2.grid(column=1, row=0,sticky ="NWE")

image = cv2.imread(path+"/happy.png")
image = cv2.resize(image, (640, 480)) 
fondo = ImageTk.PhotoImage(image=Image.fromarray(image))

image2 = cv2.imread(path+"/analisis.jpg")
image2 = cv2.resize(image2, (640, 480)) 
fondo2 = ImageTk.PhotoImage(image=Image.fromarray(image2))
#lblVideo.configure(image=fondo)
#lblVideo.image = fondo
btnRadio1.invoke()
Bot_telegram.mensaje_telegram("Empezando")
root.mainloop()
