# This Python file uses the following encoding: utf-8
import tkinter as tk
from tkinter import filedialog
#import Tkinter as tk
#import tkFileDialog as filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils

clasificador = cv2.CascadeClassifier('cascade.xml')
def reconocimientoObj(ventana):
    gris = cv2.cvtColor(ventana, cv2.COLOR_BGR2GRAY)
    caras = clasificador.detectMultiScale(ventana, 4, 60,minSize=(100,100),maxSize=(300,300))
    
    for (x, y, ancho, alto) in caras:
        cv2.rectangle(ventana, (x, y), (x + ancho, y + alto), (0, 255, 0), 2)
        cv2.putText(ventana,'Cable',(x,y-10),2,0.7,(0,255,0))
    ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    if not (len(caras) == 0):
        print("Se ejecuta funcion de captura")
        
    return ventana
def videoDeEntrada():
    global captura
    if seleccionado.get() == 1:

        ruta_video = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")])
        if len(ruta_video) > 0:
            boton.configure(state="active")
            btnRadio1.configure(state="disabled")
            btnRadio2.configure(state="disabled")
            ruta_video_entrada = "..." + ruta_video[20:]
            lblInformacionRutaVideo.configure(text=ruta_video_entrada)
            captura = cv2.VideoCapture(ruta_video)
    if seleccionado.get() == 2:
        boton.configure(state="active")
        btnRadio1.configure(state="disabled")
        btnRadio2.configure(state="disabled")
        lblInformacionRutaVideo.configure(text="")
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
    else:
        lblVideo.image = ""
        lblInformacionRutaVideo.configure(text="")
        btnRadio1.configure(state="active")
        btnRadio2.configure(state="active")
        seleccionado.set(0)
        boton.configure(state="disabled")
        captura.release()
def finalizarYLimpiar():
    lblVideo.configure(image=img2)
    lblVideo.image = img2
    lblInformacionRutaVideo.configure(text="")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="active")
    seleccionado.set(0)
    captura.release()
captura = None
root = tk.Tk()
root.title("Reproductor de vídeo avanzado")
lblInformacion1 = tk.Label(root, text="VÍDEO DE ENTRADA", font="bold")
lblInformacion1.grid(column=0, row=0, columnspan=2)
seleccionado = tk.IntVar()
btnRadio1 = tk.Radiobutton(root, text="Toma térmica", width=20, value=1, variable=seleccionado, command=videoDeEntrada)
btnRadio2 = tk.Radiobutton(root, text="Vídeo en directo", width=20, value=2, variable=seleccionado, command=videoDeEntrada)
btnRadio1.grid(column=0, row=1)
btnRadio2.grid(column=1, row=1)
lblInformacionRutaVideo = tk.Label(root, text="", width=20)
lblInformacionRutaVideo.grid(column=0, row=2)
lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=3, columnspan=2)
boton = tk.Button(root, text="Finalizar visualización y limpiar", state="disabled", command=finalizarYLimpiar)
boton.grid(column=0, row=4, columnspan=2, pady=10)
image = cv2.imread("D:/ESPOL/Tesis/prueba_opencv/happy.png")
imageToShow = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
im2 = Image.fromarray(image)
img2 = ImageTk.PhotoImage(image=im2)
btnRadio2.invoke()
seleccionado.set(2)
root.mainloop()
