import tkinter as tk
import tkinter.font as fnt
from PIL import Image
from PIL import ImageTk
import cv2
import os
import time
import Bot_telegram
import pi_therm_cam

inicio = time.time()
fecha = time.ctime()
fecha = fecha.split()
dia = fecha[0]+"_"+fecha[1]+"_"+fecha[2]+"_"+fecha[4]
#path = os.getcwd()
path = "/home/piDrone/Desktop/App"
Datos = path+'/'+dia
clasificador = cv2.CascadeClassifier('/home/piDrone/Desktop/App/cascade.xml')
cantidad = 0
time.sleep(5)
captura = cv2.VideoCapture(0)
time.sleep(5)
Imagen_ref = None 
window_width = 640
window_height = 420
root = None
seleccionado = None
lblVideo = None
boton = None
boton2 = None
btnRadio1 = None
btnRadio2 = None
fondo = None
image = None

def tempMax_chance():
    Ventana_video()

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
    global boton
    global boton2
    global btnRadio1
    global btnRadio2
    btnRadio1.configure(state="disabled")
    boton.configure(state="active")
    boton2.configure(state="disabled")
    btnRadio2.configure(state="active")
    time.sleep(1)
    
def VideoTermo():
    #global captura
    #captura.release()
    #cv2.destroyAllWindows()
    global boton
    global boton2
    global btnRadio1
    global btnRadio2
    
    boton.configure(state="active")
    boton2.configure(state="active")
    btnRadio1.configure(state="active")
    btnRadio2.configure(state="disabled")
    
def verResultado():
    global fondo
    global seleccionado
    global lblVideo
    global boton
    global boton2
    global btnRadio1
    global btnRadio2
    
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
    global root
    global image
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
    os.system("shutdown now -h")

def visualizarVideo():
    global captura
    global Imagen_ref
    global inicio
    global seleccionado
    global lblVideo
    global fondo
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
            thermcam = pi_therm_cam.pithermalcam(output_folder = "") 
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

def Ventana_video():
    global root
    global seleccionado
    global lblVideo
    global boton
    global boton2
    global btnRadio1
    global btnRadio2
    global fondo
    global image
    root = tk.Tk()
    root.title("Monitoreo Térmico")
    
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
    btnRadio1.invoke()
    visualizarVideo()
    

def on_button_click():
    Princ.destroy()

    global TempMax
    global second_window
    global label2

    second_window = tk.Tk()
    second_window.title("Configuración de temperatura")
    label2 = tk.Label(second_window, text="Temperatura de alerta: " + str(TempMax) +"ºC", font=("Arial", 18), justify=tk.LEFT)
    label2.pack(expand=True, fill='both')
    global scale
    scale = tk.Scale(second_window, from_=10, to=300, orient=tk.HORIZONTAL, command=on_scale_change,length=290)
    scale.set(TempMax)
    scale.pack(side=tk.LEFT, padx=3, pady=3,expand=True)
    button = tk.Button(second_window, text="Terminar", font=("Arial", 16), command=on_end_temp_click)
    button.pack(side=tk.LEFT, padx=3, pady=3)
    window_width = 400
    window_height = 200
    screen_width = second_window.winfo_screenwidth()
    screen_height = second_window.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    second_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    second_window.configure(background='white')

def on_end_temp_click():
    second_window.destroy()
    tempMax_chance()

def on_close_click():
    Princ.destroy()
    tempMax_chance()

def on_scale_change(val):
    global TempMax
    global label2
    TempMax = int(val)
    label2.config(text="Temperatura de alerta: " + str(TempMax) +"ºC")

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

TempMax = 80
Princ = tk.Tk()
Princ.title("App Monitoreo")
photo=tk.PhotoImage(file=path+"/mi_drone.PNG")

canvas = tk.Canvas(Princ)
canvas.create_image(230,130, image = photo, anchor = "center")
canvas.create_text(245,250, fill = "Black",text="La temperatura de reporte es 80ºC\nPara cambiarla presione continuar\ncaso contrario espere 15s", font=("Arial", 17), anchor = "center")
canvas.pack(expand=True, fill='both')

windowWidth = 500
windowHeight = 360
screenWidth = Princ.winfo_screenwidth()
screenHeight = Princ.winfo_screenheight()
centerx = int(screenWidth/2 - windowWidth / 2)
centery = int(screenHeight/2 - windowHeight / 2)
Princ.geometry(f'{windowWidth}x{windowHeight}+{centerx}+{centery}')

var = tk.IntVar()
var.set(TempMax)
button = tk.Button(Princ, text="Continuar?", font=("Arial", 16), command=on_button_click)
button.pack(side=tk.BOTTOM, pady=2)
Princ.after(15000, on_close_click)
Princ.mainloop()
