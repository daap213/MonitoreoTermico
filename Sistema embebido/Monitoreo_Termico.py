import tkinter as tk
import tkinter.font as fnt
from PIL import Image
from PIL import ImageTk
import cv2
import os
import time
import Bot_telegram
import pi_therm_cam

TempMax = 80
inicio = time.time()
fecha = time.ctime()
fecha = fecha.split()
dia = fecha[0]+"_"+fecha[1]+"_"+fecha[2]+"_"+fecha[4]
path = os.getcwd()
Datos = path+'/'+dia
clasificador = cv2.CascadeClassifier('cascade.xml')
cantidad = 0
captura = cv2.VideoCapture(0) 
Imagen_ref = None 

def referencia():
    A = time.ctime()
    A = A.split()
    hora = A[3].replace(':', '_')
    return hora

def guardar_captura(ventana1,ventana2,temp ):
    global Datos
    if not os.path.exists(Datos):
        print('Carpeta creada: ',Datos)
        os.makedirs(Datos)
    count =  referencia()
    ventana1 = cv2.cvtColor(ventana1, cv2.COLOR_BGR2RGB)
    ventana = cv2.vconcat([ventana1, ventana2])
    cv2.imwrite(Datos + "/image_" + str(count) +"_Temp_ %.2f_.jpg"% temp, ventana)
    print("Guardo captura")

def capturar():
    global Imagen_ref
    global captura
    thermcam = pi_therm_cam.pithermalcam(output_folder = "")
    temp = thermcam._temp_max
    ret, ventana = captura.read()
    
    if ret == True :
        ventana = cv2.resize(ventana, (640, 380))
        ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    guardar_captura(ventana,Imagen_ref,temp)

def reconocimientoObj(ventana):
    global Imagen_ref
    global cantidad
    global Datos
    global TempMax
    gris = cv2.cvtColor(ventana, cv2.COLOR_BGR2GRAY)
    caras = clasificador.detectMultiScale(gris, 5, 70,minSize=(75,75),maxSize=(350,350))
    ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
    if (not len(caras) == 0) and (cantidad >= 20):
        thermcam = pi_therm_cam.pithermalcam(output_folder = "")
        temp = thermcam._temp_max
        if(temp >TempMax):
            captu = thermcam.get_current_image_frame()
            Imagen_ref = cv2.resize(captu, (640, 380))
            guardar_captura(ventana,Imagen_ref,temp)
        cantidad = 0
    else:
        cantidad = 1 + cantidad
    return ventana

def monitoreoAuto():
    global captura
    btnRadio1.configure(state="disabled")
    boton.configure(state="active")
    boton2.configure(state="disabled")
    btnRadio2.configure(state="active")
    time.sleep(1)
    
def VideoTermo():
    #global captura
    #captura.release()
    #cv2.destroyAllWindows()
    boton.configure(state="active")
    boton2.configure(state="active")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="disabled")
    
def verResultado():
    seleccionado.set(0)
    lblVideo.configure(image=fondo)
    lblVideo.image = fondo
    captura.release()
    cv2.destroyAllWindows()
    boton.configure(state="disabled")
    boton2.configure(state="disabled")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="active")
    lblVideo.after(10, Enviar_telegram)


def  Enviar_telegram():
    global Datos
    global TempMax
    global captura
    Bot_telegram.stiker_telegram("CAACAgEAAxkBAAEHExhjrwgfvrsgKcUruOs42gVuVYzJYwACzgEAAqLNVzOBFRaZmhALYS0E",True,5) 
    Bot_telegram.mensaje_telegram("Fecha: "+dia,True,5)
    Bot_telegram.mensaje_telegram("Temperatura de reporte: "+str(TempMax)+" ºC",True,5)
    Bot_telegram.mensaje_telegram("Formato: Hora_Minuto_Segundo__TEMP_C",True,5)
    Bot_telegram.mensaje_telegram("Alistando capturas",True,5)
    #files_names = os.listdir(Datos)
    id_Sticker = "CAACAgEAAxkBAAEHIEVjtexuKURTLHyhb4sCYh4FkJ5KgwACrAIAAv4jsUUxMtwZpLKnIi0E"
    list_of_files = filter( lambda x: os.path.isfile(os.path.join(Datos, x)),
                        os.listdir(Datos) )
    list_of_files = sorted( list_of_files,
                        key = lambda x: os.path.getmtime(os.path.join(Datos, x))
                        )
    for file_name in list_of_files:

        image_path = Datos + "/" + file_name
        imagen = open(image_path, 'rb')
        
        if not(image is None):
            name = file_name.split("_")
            tem = name[-2]
            tem = float(tem)            
            if tem > TempMax:
                Bot_telegram.stiker_telegram(id_Sticker, True,5)                
            Bot_telegram.imagen_telegram(imagen,file_name,True,5)

    Bot_telegram.mensaje_telegram("Finalizado",True,5)
    Bot_telegram.stiker_telegram("CAACAgEAAxkBAAEHExxjrwg_kQa4l7enT1avpvjqtW_H_QACQAADmfh7JbCahlhKF3gsLQQ", True,5)
    captura.release()
    cv2.destroyAllWindows()
    root.destroy()
    #os.system("shutdown now -h")

def visualizarVideo():
    global captura
    global Imagen_ref
    global inicio

    actual = time.time()
    if (actual-inicio)<=900:
        ret, ventana = captura.read()
        img = fondo
        if ret == True and seleccionado.get() == 1:
            ventana = cv2.resize(ventana, (640, 380)) 
            ventana = reconocimientoObj(ventana)
            im = Image.fromarray(ventana)
            img = ImageTk.PhotoImage(image=im)

        if seleccionado.get() == 2 :
            thermcam = pi_therm_cam.pithermalcam(output_folder = "")  # Instantiate class
            captu = thermcam.get_current_image_frame()
            ventana = cv2.resize(captu, (640, 380))
            Imagen_ref = ventana
            ventana = cv2.cvtColor(ventana, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ventana)
            img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizarVideo)
    else:
        verResultado()


root = tk.Tk()
root.title("Monitoreo Térmico")
window_width = 640
window_height = 420
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

tamaño = fnt.Font(size = 10)
seleccionado = tk.IntVar()

lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=0, columnspan=2,rowspan=40,sticky ="NWES")

boton = tk.Button(root, text="Ver resultados",bd = '3',font = tamaño, state="active", command=verResultado)
boton.grid(column=1, row=41, pady=1, sticky ="NWES")

boton2 = tk.Button(root, text="Tomar captura",bd = '3',font = tamaño, state="disabled", command=capturar)
boton2.grid(column=0,row=41, pady=1,sticky ="NWES")

btnRadio1 = tk.Radiobutton(root, text="Automático", variable=seleccionado,
                        bd = '3',value = 1, indicator = 0,
                        font = tamaño, state="active", command=monitoreoAuto)
btnRadio1.grid(column=0, row=0,sticky ="NWE")

btnRadio2 = tk.Radiobutton(root, text="Manual", variable=seleccionado,
                        bd = '3',value = 2, indicator = 0,
                        font = tamaño, state="active", command=VideoTermo)
btnRadio2.grid(column=1, row=0,sticky ="NWE")

image = cv2.imread(path+"/telegram.png")
image = cv2.resize(image, (640, 380)) 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
fondo = ImageTk.PhotoImage(image=Image.fromarray(image))

image2 = cv2.imread(path+"/analisis.png")
image2 = cv2.resize(image2, (640, 380)) 
fondo2 = ImageTk.PhotoImage(image=Image.fromarray(image2))

btnRadio1.invoke()
visualizarVideo()
root.mainloop()
