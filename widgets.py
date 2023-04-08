import tkinter as tk
import tkinter.font as tkfont
from functools import partial
from tkinter import ttk
from tkinter import messagebox

class CenterWindow:
    def __init__(self, window):
        self.window = window
        self.center()

    def center(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update_center(self):
        self.center()

class RoundButton(tk.Button):
    def __init__(self, master=None, cnf={}, command=None, **kw):
        cnf['relief'] = tk.FLAT
        cnf['bd'] = 0
        cnf['highlightthickness'] = 0
        super().__init__(master, cnf=cnf, command=command, **kw)
        self.config(
            padx=10,
            pady=5,
            bg="#007bff",
            fg="white",
            font=("Helvetica", 12),
            cursor="hand2",
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.config(
            bg="#0062cc",
        )

    def on_leave(self, event=None):
        self.config(
            bg="#007bff",
        )

class EntryPersonalizado(tk.Entry):
    def __init__(self, *args, font=("Times New Roman", 12), bg="#ffffff", fg="#000000",titulo="si", **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(font=font, bg=bg, fg=fg,justify="right")
        self.variable = tk.StringVar()
        self.config(textvariable=self.variable)

        self.bind("<FocusIn>", self.on_entry_focus_in)
        self.bind("<FocusOut>", self.on_entry_focus_out)

        if titulo == "si":
            self.bind("<KeyRelease>", self.actualizar_entry)
    def actualizar_entry(self,event=None):
        filtro = self.variable.get()
        self.variable.set(filtro.title())
    def on_entry_focus_in(self, event):
        self.configure(bg="#f0f0f0")

    def on_entry_focus_out(self, event):
        self.configure(bg="#ffffff")
class TreeView(ttk.Treeview):
    def __init__(self, parent, colunmas,anchos):
        font = tkfont.Font(family=("Times New Roman",12))
        style = ttk.Style()
        style.layout('Custom.Treeview', [
            ('Custom.Treeview.treearea', {'sticky': 'nswe'})
        ])
        #style.configure("Treeview.Heading", background="blue", foreground="#CFDBE8")
        #style.configure('Custom.Treeview', rowheight=30)
        super().__init__(parent, columns=colunmas[1:])
        self.configure(style='Custom.Treeview')

        self.column("#0", width=anchos[0],anchor="w")
        self.heading("#0", text=colunmas[0])
        for col,ancho in zip(colunmas[1:],anchos[1:]):
            self.column(col, width=ancho, anchor="w")
            self.heading(col, text=col)

        self.parent = parent
        self.elements = {}
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=vsb.set)

        self.pack(side="left",fill="both", pady=5, padx=5, expand=True, anchor="n")
        vsb.pack(side="right",fill="y",pady=5)

        self.tag_configure("fila_par", background="#f0f0ff")
        self.tag_configure("fila_impar", background="#CFDBE8",font=font)
        self.tag_configure('fila_principal', font=font)
    def insertar_elemento_principal(self, iid, codigo, nombre):
        # Crear un ID único para el elemento
        # Insertar el elemento en el TreeView
        self.insert("", "end", iid=iid, text=codigo, values=nombre)
        # Guardar una referencia al elemento
        self.elements[iid] = {"codigo": codigo, "nombre": nombre}
        return iid
    def insertar_sub_elementos(self, iid, id_padre,codigo, datos):
        # Crear un ID único para el subelemento
        # Insertar el subelemento en el TreeView
        self.insert(id_padre, "end", iid=iid, text=codigo, values=datos)
        # Guardar una referencia al subelemento
    def cambiar_color_fila(self):
        for i,item in enumerate(self.get_children()):
            self.item(item, tags=("fila_principal",))
            for j,subitem in enumerate(self.get_children(item)):
                if j%2:
                    self.item(subitem, tags=("fila_par",))
            if i % 2:
                self.item(item, tags=("fila_impar",))

    def limpiar_tabla(self):
        for item in self.get_children():
            self.delete(item)
        self.elements = {}

class Tabla_filtro(tk.Frame):
    def __init__(self, parent, datos, nombre_columnas,ancho_columnas,funcion,buscar):
        super().__init__(parent)
        self.parent = parent
        self.funcion = funcion
        self.pack(side="left",fill="both",expand=True,pady=5,padx=5)
        frame_busqueda_filtro = tk.LabelFrame(self,bd=0)
        frame_busqueda_filtro.pack(fill="both")
        frame_busqueda = tk.LabelFrame(frame_busqueda_filtro,text = f"Buscar {buscar}",labelanchor="n",font=("Times New Roman",12))
        frame_busqueda.pack(side="left",expand=True,padx=5,pady=5,fill="x")
        frame_filtrar = tk.LabelFrame(frame_busqueda_filtro,text = "Filtrar",labelanchor="n",font=("Times New Roman",12))
        frame_filtrar.pack(fill="both",padx=5,pady=5)
        frame_tabla_filtro = tk.LabelFrame(self, text="",bd=0,font=("Times New Roman",12))
        frame_tabla_filtro.pack(fill="both",expand=True,padx=5,pady=5)
        self.entry = EntryPersonalizado(frame_busqueda)
        self.entry.pack(fill="x",padx=5,pady=5)
        self.entry.config(justify="left")
        self.filtro = ttk.Combobox(frame_filtrar,values=nombre_columnas,state="readonly",font=("Times New Roman", 12))
        self.filtro.pack(padx=5,pady=5)
        self.filtro.current(1)
        frame_seleccionar = tk.LabelFrame(self, bd=0)
        frame_seleccionar.pack(fill="both")


        self.datos = datos
        self.treeview = TreeView(frame_tabla_filtro, nombre_columnas,ancho_columnas)
        self.treeview.pack(side="left", fill="both", pady=5, padx=5, expand=True, anchor="n")
        self.treeview.limpiar_tabla()
        self.entry.bind("<KeyRelease>", self.actualizar_tabla)
        self.filtro.bind("<<ComboboxSelected>>", self.actualizar_tabla)
        self.actualizar_tabla()
        boton_seleccionar = RoundButton(frame_seleccionar, text="Seleccionar")
        boton_seleccionar.pack(fill="both", expand=True, pady=5, padx=5)
        try:
            ventana = CenterWindow(self.parent)
            ventana = ventana.window
        except:
            ventana = parent
        boton_seleccionar.config(command=partial(self.funcion, self.treeview,ventana))

    def actualizar_tabla(self, event=None):
        index = self.filtro.current()
        filtro = self.entry.get()
        x = len(filtro)
        self.treeview.limpiar_tabla()
        for i, dato in enumerate(self.datos):
            lista_dato = dato[index].split()
            for e_dato in lista_dato:
                if str(filtro).lower() in e_dato[0:x].lower():
                    self.treeview.insertar_elemento_principal(i, dato[0], dato[1:])
                    break
        self.treeview.cambiar_color_fila()
class CheckboxCombobox(ttk.Combobox):
    def __init__(self, parent, values):
        self.valuesOriginal = values
        self.values = []
        for valor in values:
            self.values.append(f"☐ {valor}")
        super().__init__(parent, values=self.values, state="readonly")
        self.pack(fill="x",expand=True)

        self.check_values = []
        self.bind("<<ComboboxSelected>>", self.on_select)
    def on_select(self, event):
        index = self.current()
        value = self.get()
        self.set("")
        if self.valuesOriginal[index] not in self.check_values:
            self.check_values.append(self.valuesOriginal[index])
            self.values[index] = f"☑ {self.valuesOriginal[index]}"
        else:
            self.check_values.remove(self.valuesOriginal[index])
            self.values[index] = f"☐ {self.valuesOriginal[index]}"
        self["values"] = self.values
