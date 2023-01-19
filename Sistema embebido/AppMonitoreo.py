import tkinter as tk
import os

path = os.getcwd()
def on_button_click():
    root.destroy()

    global num
    global second_window
    global label2

    second_window = tk.Tk()
    second_window.title("Configuración de temperatura")
    label2 = tk.Label(second_window, text="Temperatura de alerta: " + str(num) +"ºC", font=("Arial", 18), justify=tk.LEFT)
    label2.pack(expand=True, fill='both')
    global scale
    scale = tk.Scale(second_window, from_=10, to=300, orient=tk.HORIZONTAL, command=on_scale_change,length=290)
    scale.set(num)
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
    global num
    import Monitoreo_Termico
    Monitoreo_Termico.tempMax_chance(num)
    second_window.destroy()

def on_close_click():
    global num
    import Monitoreo_Termico
    Monitoreo_Termico.tempMax_chance(num)
    root.destroy()

def on_scale_change(val):
    global num
    global label2
    num = int(val)
    label2.config(text="Temperatura de alerta: " + str(num) +"ºC")

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

num = 80
root = tk.Tk()
root.title("App Monitoreo")
photo=tk.PhotoImage(file=path+"/mi_drone.png")

canvas = tk.Canvas(root)
canvas.create_image(230,130, image = photo, anchor = "center")
canvas.create_text(245,250, fill = "brown",text="La temperatura de reporte es 80ºC\nPara cambiarla presione continuar\ncaso contrario espere 15s", font=("Arial", 17), anchor = "center")
canvas.pack(expand=True, fill='both')

window_width = 500
window_height = 360
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

var = tk.IntVar()
var.set(num)
button = tk.Button(root, text="Continuar?", font=("Arial", 16), command=on_button_click)
button.pack(side=tk.BOTTOM, pady=2)
root.after(15000, on_close_click)
root.mainloop()
