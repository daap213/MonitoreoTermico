import tkinter as tk

def on_button_click():
    root.destroy()

    global num
    global second_window
    global label2

    second_window = tk.Tk()
    second_window.title("Configuración de temperatura")
    label2 = tk.Label(second_window, text="Modifique el número: " + str(num), font=("Arial", 18), justify=tk.LEFT)
    label2.pack(expand=True, fill='both')
    global scale
    scale = tk.Scale(second_window, from_=10, to=300, orient=tk.HORIZONTAL, command=on_scale_change)
    scale.set(num)
    scale.pack(side=tk.LEFT, padx=10, pady=10)
    button = tk.Button(second_window, text="Terminar", font=("Arial", 20), command=on_end_temp_click)
    button.pack(side=tk.RIGHT, padx=10, pady=10)
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
    #import Monitoreo_Termico
    #Monitoreo_Termico.tempMax_chance(num)
    second_window.destroy()

def on_close_click():
    global num
    #import Monitoreo_Termico
    #Monitoreo_Termico.tempMax_chance(num)
    root.destroy()

def on_scale_change(val):
    global num
    global label2
    num = int(val)
    label2.config(text="Modifique el número: " + str(num))

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
label = tk.Label(root, text="La temperatura de reporte es 80ºC\nSi desea cambiarla presione continuar\ncaso contrario espere 15s", font=("Arial", 18), justify=tk.LEFT)
label.pack(expand=True, fill='both',pady=10)

window_width = 500
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.configure(background='white')

var = tk.IntVar()
var.set(num)
button = tk.Button(root, text="Continuar?", font=("Arial", 16), command=on_button_click)
button.pack(side=tk.BOTTOM, pady=10)
root.after(10000, on_close_click)
root.mainloop()
