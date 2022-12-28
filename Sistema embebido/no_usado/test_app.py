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
def referencia():
    A = time.ctime()
    A = A.split()
    hora = A[3].replace(':', '_')
    return hora

def guardar_captura(ventana2):
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
    gris = cv2.cvtColor(ventana, cv2.COLOR_BGR2GRAY)
    caras = clasificador.detectMultiScale(gris, 5, 70,minSize=(75,75),maxSize=(350,350))
    for (x, y, ancho, alto) in caras:
        cv2.rectangle(ventana, (x, y), (x + ancho, y + alto), (0, 255, 0), 2)
        cv2.putText(ventana,'Cable',(x,y-10),2,0.7,(0,255,0))
    ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    if not (len(caras) == 0):
        ventana2 = ventana
        guardar_captura(ventana2)
    return ventana


def monitoreoAuto():
    global captura
    global estado
    if not estado == "Inicio":
        boton.invoke()
        
    if seleccionado.get() == 1:
        btnRadio1.configure(state="disabled")
        btnRadio2.configure(state="active")
        estado = "uno"
    if seleccionado.get() == 2:
        btnRadio1.configure(state="active")
        btnRadio2.configure(state="disabled")
        estado = "dos"
    
    boton.configure(state="active")
    btnRadio3.configure(state="active")
    captura = cv2.VideoCapture(0) 
    visualizarVideo()
    
def VideoTermo():
    captura.release()
    boton.configure(state="active")
    btnRadio2.configure(state="active")
    btnRadio1.configure(state="active")
    btnRadio3.configure(state="disabled")
    lblVideo.configure(image=fondo2)
    lblVideo.image = fondo2
    
def visualizarVideo():
    global captura
    ret, ventana = captura.read()
    if ret == True:
        ventana = cv2.resize(ventana, (640, 480)) 
        if seleccionado.get() == 1:
            ventana = reconocimientoObj(ventana)
        if seleccionado.get() == 2:
            ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(ventana)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizarVideo)


def finalizarYLimpiar():
    seleccionado.set(0)
    captura.release()
    cv2.destroyAllWindows()
    lblVideo.configure(image=fondo)
    lblVideo.image = fondo
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="active")
    btnRadio3.configure(state="active")
    Bot_telegram.mensaje_telegram("Analisando capturas")

captura = None

root = tk.Tk()
tamaño = fnt.Font(size = 12)
root.title("Monitoreo Térmico")
seleccionado = tk.IntVar()
lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=0, columnspan=10,rowspan=40)
boton = tk.Button(root, text="Ver resultados",bd = '5',font = tamaño, state="active", command=finalizarYLimpiar)
boton.grid(column=0, row=42, columnspan=10, pady=3)

btnRadio1 = tk.Radiobutton(root, text="Automático", variable=seleccionado,
                        bd = '3',value = 1, indicator = 0,
                        font = tamaño, state="active", command=monitoreoAuto)
btnRadio1.grid(column=0, row=0,sticky ="NWE")
btnRadio2 = tk.Radiobutton(root, text="Cámara normal", variable=seleccionado,
                        bd = '3',value = 2, indicator = 0,
                        font = tamaño, state="active", command=monitoreoAuto)
btnRadio2.grid(column=1, row=0,sticky ="NWE")
btnRadio3 = tk.Radiobutton(root, text="Cámara térmica", variable=seleccionado,
                        bd = '3',value = 3, indicator = 0,
                        font = tamaño, state="active", command=VideoTermo)
btnRadio3.grid(column=2, row=0,sticky ="NWE")
image = cv2.imread(path+"/happy.png")
fondo = ImageTk.PhotoImage(image=Image.fromarray(image))
image2 = cv2.imread(path+"/analisis.jpg")
fondo2 = ImageTk.PhotoImage(image=Image.fromarray(image2))
#lblVideo.configure(image=fondo)
#lblVideo.image = fondo
btnRadio1.invoke()
Bot_telegram.mensaje_telegram("Empezando")
root.mainloop()

"""     if seleccionado.get() == 1:
        boton.configure(state="active")
        btnRadio1.configure(state="disabled")
        btnRadio2.configure(state="disabled")
        lblInformacionRutaVideo.configure(text="")
        captura = cv2.VideoCapture(1) """
""" 
        ruta_video = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")])
        if len(ruta_video) > 0:
            boton.configure(state="active")
            btnRadio1.configure(state="disabled")
            btnRadio2.configure(state="disabled")
            ruta_video_entrada = "..." + ruta_video[20:]
            lblInformacionRutaVideo.configure(text=ruta_video_entrada)
            captura = cv2.VideoCapture(ruta_video) """