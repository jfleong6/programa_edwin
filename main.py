import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
from widgets import *



class MyGUI:
    def __init__(self, master):
        self.frame_menu_izquierda = {}
        self.baseDatos = "Base de datos.s3db"
        self.master = master
        master.title("Mi interfaz gráfica")

        # Hacer que la ventana ocupe toda la pantalla
        master.attributes("-fullscreen", True)

        # Crear el menú
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # Crear el menú Archivo
        self.archivo_menu = tk.Menu(self.menu)
        self.archivo_menu.add_command(label="Abrir")
        self.archivo_menu.add_command(label="Guardar")
        self.menu.add_cascade(label="Archivo", menu=self.archivo_menu)

        # Crear el menú Clientes
        self.clientes_menu = tk.Menu(self.menu)
        self.clientes_menu.add_command(label="Agregar cliente",command=self.agregar_cliente,accelerator='Ctrl+u')
        self.clientes_menu.add_command(label="Editar cliente",command=self.editar_cliente,accelerator="Ctrl+E")
        self.menu.add_cascade(label="Clientes", menu=self.clientes_menu)
        self.master.bind('<Control-u>', lambda event: self.agregar_cliente())
        self.master.bind('<Control-U>', lambda event: self.agregar_cliente())
        self.master.bind('<Control-e>', lambda event: self.editar_cliente())
        self.master.bind('<Control-E>', lambda event: self.editar_cliente())
        self.create_menu()
        self.menu_servicios()

    # Metodos de consulta de base de datos
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.baseDatos) as conect:
            cursor = conect.cursor()
            cursor.execute(query, parameters)
            result = cursor.fetchall()
            conect.commit()
            return result
    def run_queryColumnas(self, query):
        with sqlite3.connect(self.baseDatos) as conect:
            cursor = conect.cursor()
            cursor.execute(query)
            nombres_columnas = [columna[0] for columna in cursor.description]
            conect.commit()
            return nombres_columnas
    def run_query_many(self, query, parameters=()):
        with sqlite3.connect(self.baseDatos) as conect:
            cursor = conect.cursor()
            cursor.executemany(query, parameters)
            result = cursor.fetchall()
            conect.commit()
            return result

    # Crear el menú Ayuda
    def create_menu(self):
        # Crea un frame para el menú de la parte izquierda
        menu_frame = tk.Frame(self.master, bg="lightgray", width=150)
        menu_frame.pack(side="left", fill="y")

        # Crea los botones y los agrega al frame del menú
        boton1 = RoundButton(menu_frame, text="Mesa de trabajo",command=partial(self.Activar_menu_izquierda, "Mesa de trabajo"))
        boton1.pack(fill="x",pady=5,padx=5)
        self.frame_menu_izquierda["Mesa de trabajo"] = tk.Frame(self.master)
        boton2 = RoundButton(menu_frame, text="Servicios",command=partial(self.Activar_menu_izquierda, "Servicios"))
        self.frame_menu_izquierda["Servicios"] = tk.Frame(self.master)
        boton2.pack(fill="x",pady=5,padx=5)
        boton3 = RoundButton(menu_frame, text="Reportes",command=partial(self.Activar_menu_izquierda, "Reportes"))
        self.frame_menu_izquierda["Reportes"] = tk.Frame(self.master)
        boton3.pack(fill="x",pady=5,padx=5)
        boton4 = RoundButton(menu_frame, text="Personal",command=partial(self.Activar_menu_izquierda, "Personal"))
        self.frame_menu_izquierda["Personal"] = tk.Frame(self.master)
        boton4.pack(fill="x",pady=5,padx=5)
        boton5 = RoundButton(menu_frame, text="Cuentas",command=partial(self.Activar_menu_izquierda, "Cuentas"))
        self.frame_menu_izquierda["Cuentas"] = tk.Frame(self.master)
        boton5.pack(fill="x",pady=5,padx=5)
        self.frame_menu_izquierda["Activo"] = self.frame_menu_izquierda["Mesa de trabajo"]

        self.menu_izquierda_activo = self.frame_menu_izquierda["Mesa de trabajo"]
        self.Activar_menu_izquierda("Mesa de trabajo")

    # Activar menu izquierda
    def Activar_menu_izquierda(self,menu_activar):
        self.menu_izquierda_activo.pack_forget()
        self.frame_menu_izquierda[menu_activar].pack(fill="both",expand = True)
        self.menu_izquierda_activo = self.frame_menu_izquierda[menu_activar]

    # Agregar Nuevo cliente
    def agregar_cliente(self):
        # Crear ventana emergente para nuevo cliente
        top = tk.Toplevel(self.master)
        top.title("Nuevo Cliente")

        top.bind('<Escape>', lambda event: top.destroy())

        # Etiqueta y Entrada para Nombre
        nombre_lbl = tk.Label(top, text="Nombres:")
        nombre_lbl.grid(row=0, column=0, padx=5, pady=5)
        nombre_entry = EntryPersonalizado(top)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y Entrada para Apellido
        apellido_lbl = tk.Label(top, text="Apellidos:")
        apellido_lbl.grid(row=1, column=0, padx=5, pady=5)
        apellido_entry = EntryPersonalizado(top)
        apellido_entry.grid(row=1, column=1, padx=5, pady=5)

        # Etiqueta y Entrada para Correo
        correo_lbl = tk.Label(top, text="Correo:")
        correo_lbl.grid(row=2, column=0, padx=5, pady=5)
        correo_entry = EntryPersonalizado(top,titulo="no")
        correo_entry.grid(row=2, column=1, padx=5, pady=5)

        # Etiqueta y Entrada para Celular
        celular_lbl = tk.Label(top, text="Celular:")
        celular_lbl.grid(row=3, column=0, padx=5, pady=5)
        celular_entry = EntryPersonalizado(top)
        celular_entry.grid(row=3, column=1, padx=5, pady=5)



        # Crear botón de "Guardar" para guardar nuevo cliente
        guardar_btn = RoundButton(top, text="Guardar", command=lambda: self.guardar_nuevo_cliente(top,
                                                                                                nombre_entry.get(),
                                                                                                apellido_entry.get(),
                                                                                                correo_entry.get(),
                                                                                                celular_entry.get()))
        nombre_entry.focus()
        guardar_btn.grid(row=5, column=0,columnspan=2, sticky="we", padx=5, pady=5)
        CenterWindow(top)

    # Verificacion y guardar datos
    def guardar_nuevo_cliente(self, ventana, nombre, apellido, correo, celular):

        # Validar que se los datos
        if not nombre or not apellido or not re.match(r"[^@]+@[^@]+\.[^@]+", correo) or not celular.isdigit() or len(celular) != 10:
            messagebox.showerror("Error", "Los datos ingresados no son válidos.")
            ventana.lift()
            return

        nuevo_cliente = [nombre, apellido, correo, celular]
        query = "insert into Clientes VALUES(Null,?,?,?,?)"
        try:
            self.run_query(query,nuevo_cliente)
        except sqlite3.OperationalError as error:
            queryCreartable = 'CREATE TABLE IF NOT EXISTS Clientes (' \
                              'ID INTEGER NOT NULL, '\
                              'Nombre TEXT NOT NULL, ' \
                              'Apellido TEXT NOT NULL, ' \
                              'Correo TEXT NOT NULL, ' \
                              'Celular TEXT NOT NULL,' \
                              'PRIMARY KEY("ID"))'
            self.run_query(queryCreartable)
            self.run_query(query, nuevo_cliente)
        ventana.destroy()

    # ver y clientes y editarlos
    def editar_cliente(self):
        self.top = tk.Toplevel(self.master)
        self.top.title("Editar Cliente")
        self.top.bind('<Escape>', lambda event: self.top.destroy())

        datos = self.run_query("select * from Clientes")

        self.nombre_columnas = self.run_queryColumnas("select * from Clientes")
        frame_editar = Tabla_filtro(self.top,datos,self.nombre_columnas,[30,110,110,130,100],self.frame_editar_clientes,"Cliente")

    # Verificacion los datos y para editar
    def frame_editar_clientes(self,cliente,ventana):
        try:
            self.top = ventana
            seleccion = cliente.selection()[0]
            id = cliente.item(seleccion)["text"]
            datos = cliente.item(seleccion)["values"]
            try:
                self.frame_datos_editar.destroy()
            except:
                pass

            self.frame_datos_editar =tk.LabelFrame(self.top,text=f"Cliente: {id}")
            self.frame_datos_editar.pack(side="left",fill="both",expand=True,pady=5,padx=5)
            nombre_lbl = tk.Label(self.frame_datos_editar, text="Nombres:")
            nombre_lbl.grid(row=0, column=0, padx=5, pady=5)
            nombre_entry = EntryPersonalizado(self.frame_datos_editar)
            nombre_entry.variable.set((datos[0]))
            nombre_entry.grid(row=0, column=1, padx=5, pady=5)

            # Etiqueta y Entrada para Apellido
            apellido_lbl = tk.Label(self.frame_datos_editar, text="Apellidos:")
            apellido_lbl.grid(row=1, column=0, padx=5, pady=5)
            apellido_entry = EntryPersonalizado(self.frame_datos_editar)
            apellido_entry.variable.set((datos[1]))
            apellido_entry.grid(row=1, column=1, padx=5, pady=5)


            # Etiqueta y Entrada para Correo
            correo_lbl = tk.Label(self.frame_datos_editar, text="Correo:")
            correo_lbl.grid(row=2, column=0, padx=5, pady=5)
            correo_entry = EntryPersonalizado(self.frame_datos_editar, titulo="no")
            correo_entry.variable.set((datos[2]))
            correo_entry.grid(row=2, column=1, padx=5, pady=5)

            # Etiqueta y Entrada para Celular
            celular_lbl = tk.Label(self.frame_datos_editar, text="Celular:")
            celular_lbl.grid(row=3, column=0, padx=5, pady=5)
            celular_entry = EntryPersonalizado(self.frame_datos_editar)
            celular_entry.variable.set((datos[3]))
            celular_entry.grid(row=3, column=1, padx=5, pady=5)
            guardar_btn = RoundButton(self.frame_datos_editar, text="Guardar", command=lambda: self.actulizar_cliente(self.top,
                                                                                                      id,
                                                                                                      nombre_entry.get(),
                                                                                                      apellido_entry.get(),
                                                                                                      correo_entry.get(),
                                                                                                      celular_entry.get(),datos))

            guardar_btn.grid(row=5, column=0, columnspan=2, sticky="we", padx=5, pady=5)
            self.top.geometry(f"783x366")

        except IndexError as e:
            messagebox.showerror(title = "Editar Cliente",message="Para continuar, seleccione un cliente de la lista.")
            self.top.lift()
    def actulizar_cliente(self, ventana, id,nombre, apellido, correo, celular,datos):
        # Validar que se los datos
        if not nombre or not apellido or not re.match(r"[^@]+@[^@]+\.[^@]+", correo) or not celular.isdigit() or len(celular) != 10:
            messagebox.showerror("Error", "Los datos ingresados no son válidos.")
            self.top.lift()
            return
        lista = [nombre, apellido, correo, celular]
        for columna,datoA,datoP in zip(self.nombre_columnas[1:],lista,datos):
            if datoA != datoP:
                query = f"UPDATE clientes SET {columna} = '{datoA}' WHERE id = {id}"
                self.run_query(query)
        self.top.destroy()
        messagebox.showinfo(title="Editar Cliente",message="Cliente editado exitosamente")

    # Menu Mesa de Trabajo
    def menu_mesa_Trabajo(self):
        pass

    # Menu Servicios
    def menu_servicios(self):
        #lista_servicios = self.run_query()
        query = "select *from Servicios"
        try:
            lista_servicios = self.run_query(query)
        except:
            queryCreartable = 'CREATE TABLE IF NOT EXISTS Servicios (' \
                              'ID INTEGER NOT NULL, ' \
                              'Descripcion TEXT NOT NULL, ' \
                              'Cant TEXT NOT NULL, ' \
                              'Clasificacion TEXT NOT NULL, ' \
                              'PRIMARY KEY("ID"))'
            self.run_query(queryCreartable)
            lista_servicios =self.run_query(query)
        nombre_columnas = self.run_queryColumnas("select *from Servicios")
        anchos_columnas = [30,130,30]
        frame_lista_servicios = tk.LabelFrame(self.frame_menu_izquierda["Servicios"],text="Servicios y Articulos",font=("Times New Roman",12))
        frame_lista_servicios.pack(side="left",fill="y",expand=True,anchor="nw")
        self.tabla_lista_servicios = Tabla_filtro(frame_lista_servicios,lista_servicios,nombre_columnas[:-1],anchos_columnas,self.editar_servicio,"servicio")
        self.frame_nueva_categoria_articulos = tk.Frame(self.frame_menu_izquierda["Servicios"])
        self.frame_nueva_categoria_articulos.pack(side="left",fill="both",expand=True,anchor="nw")
        self.crear_nuevo_servico()
        self.crear_nueva_categoria()
        self.editar_servicio()
    # Crear nuevo servicio
    def crear_nuevo_servico(self):
        frame_nuevo_servicio = tk.LabelFrame(self.frame_nueva_categoria_articulos, text="Nuevo Servicio o articulo",
                                              font=("Times New Roman", 12))
        frame_nuevo_servicio.grid(padx=5, pady=5, row=0, column=0)
        self.entrada_nuevo_servicio = EntryPersonalizado(frame_nuevo_servicio)
        try:
                
        self.clasificacion = ttk.Combobox(frame_nuevo_servicio,values=["Clasificacion","Servicio","Articulo"],font=("Arial",10),width=10,state="readonly")
        self.clasificacion.current(0)
        boton_nuevo_servicio = RoundButton(frame_nuevo_servicio, text="Guardar servicio")
        boton_nuevo_servicio.config(command=lambda: self.guardar_nuevo_servicio(self.entrada_nuevo_servicio.get(),
                                                                                self.clasificacion.get()))
        self.entrada_nuevo_servicio.pack(side="left", fill="x", pady=5, padx=5)
        self.clasificacion.pack(side="left", pady=5)
        boton_nuevo_servicio.pack(side="left", pady=5, padx=5)

    # Guardar Ariculo
    def guardar_nuevo_servicio(self,servicio,clasificacion):
        print(servicio,clasificacion)
        if clasificacion != "Clasificacion" or not servicio:
            query = "insert into Servicios values (Null,?,?,?)"
            parametros = [servicio,0,clasificacion]
            self.run_query(query,parametros)
            self.tabla_lista_servicios.datos = self.run_query("Select *from Servicios")
            self.tabla_lista_servicios.actualizar_tabla()
            messagebox.showinfo(title="Nuevo servicio o articulo",message=f"{clasificacion} agregado existosamente")
            self.entrada_nuevo_servicio.variable.set("")
            self.clasificacion.current(0)

        else:
            messagebox.showinfo(title="Nuevo servicio o articulo",message="Datos incompletos")
    # Crear nueva Categoria
    def crear_nueva_categoria(self):
        frame_nueva_categoria = tk.LabelFrame(self.frame_nueva_categoria_articulos, text="Nueva Categoria",
                                              font=("Times New Roman", 12))
        frame_nueva_categoria.grid(padx=5,pady=5,row=0,column=1)
        entrada_nueva_categoria = EntryPersonalizado(frame_nueva_categoria)
        boton_nueva_categoria = RoundButton(frame_nueva_categoria,text="Guardar categoria")
        entrada_nueva_categoria.pack(side="left",fill="x",pady=5,padx=5)
        boton_nueva_categoria.pack(side="left",pady=5,padx=5)

    # Editar Servicio
    def editar_servicio(self,cliente=None,ventana=None):
        frame_nueva_categoria = tk.LabelFrame(self.frame_nueva_categoria_articulos, text="Editar Servicio",
                                              font=("Times New Roman", 12))
        frame_nueva_categoria.grid(padx=5, pady=5, row=1, column=0,columnspan=2)

    # Menu Reportes
    def menu_reportes(self):
        pass

    # Menu Servicios
    def menu_personal(self):
        pass
    # Menu Servicios
    def menu_cuentas(self):
        pass



root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()



