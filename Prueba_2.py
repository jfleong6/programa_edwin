import tkinter as tk

root = tk.Tk()

def save():
    print("Guardando...")

# crear el botón
btn_save = tk.Button(root, text="Guardar", command=save, accelerator="Ctrl+S")
btn_save.pack(pady=10, padx=20)

# crear la etiqueta para mostrar el atajo de teclado
lbl_accelerator = tk.Label(root, text="Atajo de teclado: Ctrl+S")
lbl_accelerator.pack(pady=5)

# crear el evento de atajo de teclado
def handle_shortcut(event):
    if event.keysym == 's' and event.state == 0x4:
        save()

root.bind('<Control-s>', handle_shortcut)

root.mainloop()
