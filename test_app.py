import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import os
import imutils
import time
import Bot_telegram

fecha = time.ctime()
fecha = fecha.split()
dia = fecha[0]+"_"+fecha[1]+"_"+fecha[2]+"_"+fecha[4]
path = os.getcwd()
Datos = path+'/'+dia

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

def reconocimientoObj(ventana):
    gris = cv2.cvtColor(ventana, cv2.COLOR_BGR2GRAY)
    caras = clasificador.detectMultiScale(gris, 3, 60,minSize=(200,200),maxSize=(350,350))
    
    for (x, y, ancho, alto) in caras:
        cv2.rectangle(ventana, (x, y), (x + ancho, y + alto), (0, 255, 0), 2)
        cv2.putText(ventana,'Cable',(x,y-10),2,0.7,(0,255,0))
    ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    if not (len(caras) == 0):
        ventana2 = ventana
        guardar_captura(ventana2)
    return ventana

def videoDeEntrada():
    global captura
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
    if seleccionado.get() == 1:
        boton.configure(state="active")
        btnRadio1.configure(state="disabled")
        captura = cv2.VideoCapture(0)
    visualizarVideo()
def visualizarVideo():
    global captura
    ret, ventana = captura.read()
    if ret == True:
        ventana = imutils.resize(ventana, width=640)
        ventana = reconocimientoObj(ventana)
        im = Image.fromarray(ventana)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizarVideo)

def finalizarYLimpiar():
    lblVideo.configure(image=fondo)
    lblVideo.image = fondo
    lblInformacionRutaVideo.configure(text="")
    btnRadio1.configure(state="active")
    seleccionado.set(0)
    captura.release()
    Bot_telegram.mensaje_telegram("Analisando capturas")

captura = None
root = tk.Tk()
root.title("Monitoreo Térmico")
lblInformacion1 = tk.Label(root, text="VÍDEO DE ENTRADA", font="bold",width=40)
lblInformacion1.grid(column=0, row=0, columnspan=2)
seleccionado = tk.IntVar()
btnRadio1 = tk.Radiobutton(root, text="", value=1, variable=seleccionado, command=videoDeEntrada)
btnRadio1.grid(column=1, row=0)
lblInformacionRutaVideo = tk.Label(root, text="", width=20)
lblInformacionRutaVideo.grid(column=0, row=2)
lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=3, columnspan=2)
boton = tk.Button(root, text="Ver resultados", state="active", command=finalizarYLimpiar)
boton.grid(column=0, row=4, columnspan=2, pady=10)
image = cv2.imread(path+"/happy.png")
fondo = ImageTk.PhotoImage(image=Image.fromarray(image))
image2 = cv2.imread(path+"/analisis.jpg")
fondo2 = ImageTk.PhotoImage(image=Image.fromarray(image2))
btnRadio1.invoke()
seleccionado.set(2)
Bot_telegram.mensaje_telegram("Empezando")
root.mainloop()
