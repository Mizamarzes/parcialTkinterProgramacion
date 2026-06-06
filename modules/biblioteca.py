# modules/biblioteca.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from model.Libro import Libro

class BibliotecaPantalla(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        self.fila_en_edicion = None
        
        # --- TÍTULOS ---
        tk.Label(self, text="SISTEMA DE GESTIÓN DE BIBLIOTECA UDI", font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 2))
        
        # --- FORMULARIO ---
        frame_form = tk.Frame(self, bg="white")
        frame_form.pack(padx=20, pady=5)
        
        reg_num = self.register(self.validar_numeros)
        
        # 1. Fecha de Ingreso
        tk.Label(frame_form, text="FECHA DE INGRESO", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=4)
        self.lbl_fecha = tk.Label(frame_form, text="", font=("Arial", 10, "italic"), bg="#e0e0e0", width=12, relief="sunken")
        self.lbl_fecha.grid(row=0, column=1, sticky="w", padx=5)
        
        # 2. ID Libro
        tk.Label(frame_form, text="ID LIBRO", font=("Arial", 10, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_id = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.ent_id.grid(row=1, column=1, sticky="w", padx=5)
        self.ent_id.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.ent_id, 10))
        
        # 3. Nombre del Libro
        tk.Label(frame_form, text="NOMBRE DEL LIBRO", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_nombre = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.ent_nombre.grid(row=2, column=1, sticky="w", padx=5)
        self.ent_nombre.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.ent_nombre, 100))
        
        # 4. Editorial
        tk.Label(frame_form, text="EDITORIAL", font=("Arial", 10, "bold"), bg="white").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_editorial = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.ent_editorial.grid(row=3, column=1, sticky="w", padx=5)
        self.ent_editorial.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.ent_editorial, 100))
        
        # 5. Autor
        tk.Label(frame_form, text="AUTOR", font=("Arial", 10, "bold"), bg="white").grid(row=4, column=0, sticky="w", pady=4)
        self.ent_autor = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.ent_autor.grid(row=4, column=1, sticky="w", padx=5)
        self.ent_autor.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.ent_autor, 100))
        
        # 6. Número de Copias
        tk.Label(frame_form, text="NUMERO DE COPIAS", font=("Arial", 10, "bold"), bg="white").grid(row=5, column=0, sticky="w", pady=4)
        self.ent_copias = tk.Entry(frame_form, font=("Arial", 10), width=8, validate="key", validatecommand=(reg_num, '%P'))
        self.ent_copias.grid(row=5, column=1, sticky="w", padx=5)
        self.ent_copias.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.ent_copias, 3))

        # --- BOTONES DE ACCIÓN ---
        frame_botones_top = tk.Frame(self, bg="white")
        frame_botones_top.pack(pady=10)
        
        tk.Button(frame_botones_top, text="Nuevo", width=10, command=self.guardar_cambios_dialogo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones_top, text="Editar", width=10, command=self.cargar_registro_a_editar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones_top, text="Guardar", width=10, command=self.guardar_cambios_dialogo).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones_top, text="Eliminar", width=10, command=self.eliminar_registro).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones_top, text="Dar de baja", width=10, command=self.abrir_modal_baja).grid(row=0, column=4, padx=5)

        # --- NUEVO: BARRA DE BÚSQUEDA ---
        frame_buscar = tk.Frame(self, bg="white")
        frame_buscar.pack(pady=5)
        
        tk.Label(frame_buscar, text="BUSCAR (ID o Nombre):", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=5)
        self.ent_buscar = tk.Entry(frame_buscar, font=("Arial", 10), width=25)
        self.ent_buscar.grid(row=0, column=1, padx=5)
        tk.Button(frame_buscar, text="Buscar", width=10, command=self.buscar_libro).grid(row=0, column=2, padx=5)

        # --- GRILLA (TREEVIEW) ---
        frame_grilla = tk.Frame(self)
        frame_grilla.pack(padx=20, pady=5, fill="both", expand=True)
        
        columnas = ("id", "nombre", "editorial", "autor", "copias", "fecha")
        self.grilla = ttk.Treeview(frame_grilla, columns=columnas, show="headings", height=8)
        
        self.grilla.heading("id", text="Id Libro")
        self.grilla.heading("nombre", text="Nombre Libro")
        self.grilla.heading("editorial", text="Editorial")
        self.grilla.heading("autor", text="Autor")
        self.grilla.heading("copias", text="Num. copias")
        self.grilla.heading("fecha", text="Fecha Ingreso")
        
        self.grilla.column("id", width=80, anchor="center")
        self.grilla.column("nombre", width=200, anchor="w")
        self.grilla.column("editorial", width=150, anchor="w")
        self.grilla.column("autor", width=150, anchor="w")
        self.grilla.column("copias", width=80, anchor="center")
        self.grilla.column("fecha", width=100, anchor="center")
        
        self.grilla.pack(fill="both", expand=True)

        # --- BOTONES INFERIORES ---
        frame_botones_bottom = tk.Frame(self, bg="white")
        frame_botones_bottom.pack(pady=15)
        
        tk.Button(frame_botones_bottom, text="Cancelar", width=12, command=self.limpiar_y_cancelar_edicion).grid(row=0, column=0, padx=15)
        tk.Button(frame_botones_bottom, text="Mostrar datos", width=12, command=self.mostrar_datos_mock).grid(row=0, column=1, padx=15)
        tk.Button(frame_botones_bottom, text="Salir", width=12, command=self.quit).grid(row=0, column=2, padx=15)
        tk.Button(frame_botones_bottom, text="Préstamos", width=12, command=lambda: self.controller.mostrar_pantalla("prestamos")).grid(row=0, column=3, padx=15)

    def actualizar_fecha(self):
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.lbl_fecha.config(text=fecha_actual)

    def validar_numeros(self, texto):
        if texto == "" or texto.isdigit():
            return True
        return False

    def limitar_caracteres(self, entrada, max_caracteres):
        contenido = entrada.get()
        if len(contenido) > max_caracteres:
            entrada.delete(max_caracteres, tk.END)

    def limpiar_cajas(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_editorial.delete(0, tk.END)
        self.ent_autor.delete(0, tk.END)
        self.ent_copias.delete(0, tk.END)

    def limpiar_y_cancelar_edicion(self):
        self.limpiar_cajas()
        self.ent_buscar.delete(0, tk.END)  
        self.fila_en_edicion = None
        self.actualizar_fecha()

    def cargar_registro_a_editar(self):
        seleccion = self.grilla.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un registro de la grilla para poder editarlo.")
            return
            
        self.fila_en_edicion = seleccion[0]
        valores = self.grilla.item(self.fila_en_edicion, "values")
        
        self.limpiar_cajas()
        self.ent_id.insert(0, valores[0])
        self.ent_nombre.insert(0, valores[1])
        self.ent_editorial.insert(0, valores[2])
        self.ent_autor.insert(0, valores[3])
        self.ent_copias.insert(0, valores[4])
        self.lbl_fecha.config(text=valores[5])

    def guardar_cambios_dialogo(self):
        if not self.ent_id.get() or not self.ent_nombre.get():
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese el ID y Nombre del Libro para procesar el registro.")
            return
            
        id_ingresado = self.ent_id.get().strip()
        for item in self.grilla.get_children():
            if self.fila_en_edicion and item == self.fila_en_edicion:
                continue
            
            valores_fila = self.grilla.item(item, "values")
            if valores_fila and valores_fila[0] == id_ingresado:
                messagebox.showerror("ID Duplicado", f"El ID '{id_ingresado}' ya se encuentra registrado. Ingrese un ID único.")
                return
            
        respuesta = messagebox.askyesno("Desea guardar cambios?", "¿Desea guardar cambios?")
        if respuesta:
            datos_formulario = (
                self.ent_id.get(),
                self.ent_nombre.get(),
                self.ent_editorial.get(),
                self.ent_autor.get(),
                self.ent_copias.get(),
                self.lbl_fecha.cget("text")
            )
            
            if self.fila_en_edicion:
                exito, msg = self.controller.gestion_libros.editar(
                    datos_formulario[0], datos_formulario[1], datos_formulario[2],
                    datos_formulario[3], datos_formulario[4], datos_formulario[5]
                )
                if exito:
                    self.grilla.item(self.fila_en_edicion, values=datos_formulario)
                    messagebox.showinfo("Éxito", msg)
            else:
                nuevo_libro = Libro(*datos_formulario)
                exito, msg = self.controller.gestion_libros.guardar(nuevo_libro)
                if exito:
                    self.grilla.insert("", "end", values=datos_formulario)
                    messagebox.showinfo("Éxito", msg)
                else:
                    messagebox.showerror("Error", msg)
                
            self.limpiar_y_cancelar_edicion()

    def eliminar_registro(self):
        seleccion = self.grilla.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un registro de la grilla para eliminar.")
            return
            
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar el registro seleccionado?")
        if respuesta:
            valores = self.grilla.item(seleccion[0], "values")
            id_eliminar = valores[0]
            
            self.controller.gestion_libros.eliminar(id_eliminar)
            
            self.grilla.delete(seleccion[0])
            self.limpiar_y_cancelar_edicion()
            messagebox.showinfo("Éxito", "El registro ha sido eliminado correctamente.")

    def mostrar_datos_mock(self):
        """Limpiar la tabla y lee los datos actuales directamente del JSON."""
        for item in self.grilla.get_children():
            self.grilla.delete(item)
            
        libros_json = self.controller.gestion_libros.obtener_todos()
        
        if not libros_json:
            messagebox.showinfo("Archivo vacío", "No hay registros guardados en el archivo JSON actualmente.")
            return
            
        for libro in libros_json:
            self.grilla.insert("", "end", values=(
                libro.id,
                libro.nombre,
                libro.editorial,
                libro.autor,
                libro.copias,
                libro.fecha
            ))

    def buscar_libro(self):
        termino_busqueda = self.ent_buscar.get().strip().lower()
        
        if not termino_busqueda:
            messagebox.showwarning("Búsqueda vacía", "Por favor, ingrese un ID o Nombre de libro para realizar la búsqueda.")
            return

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        todos_los_libros = self.controller.gestion_libros.obtener_todos()
        encontrado = False

        for libro in todos_los_libros:
            if termino_busqueda in libro.id.lower() or termino_busqueda in libro.nombre.lower():
                self.grilla.insert("", "end", values=(
                    libro.id,
                    libro.nombre,
                    libro.editorial,
                    libro.autor,
                    libro.copias,
                    libro.fecha
                ))
                encontrado = True

        if not encontrado:
            messagebox.showinfo("Sin resultados", f"No se encontró ningún libro con el criterio: '{termino_busqueda}'.")

    def abrir_modal_baja(self):
        """Abre un modal para dar de baja una copia del libro seleccionado indicando el motivo."""
        seleccion = self.grilla.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un libro de la grilla para darlo de baja.")
            return

        valores = self.grilla.item(seleccion[0], "values")
        id_libro, nombre, editorial, autor, copias = valores[0], valores[1], valores[2], valores[3], valores[4]

        if int(copias) <= 0:
            messagebox.showwarning("Sin copias", f"El libro '{nombre}' no tiene copias disponibles para dar de baja.")
            return

        modal = tk.Toplevel(self)
        modal.title("Dar de baja un libro")
        modal.configure(bg="white")
        modal.resizable(False, False)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        tk.Label(modal, text="DAR DE BAJA UNA COPIA", font=("Arial", 12, "bold"), bg="white").pack(pady=(15, 5), padx=20)
        tk.Label(modal, text=f"Libro: {nombre} (ID: {id_libro})", font=("Arial", 10), bg="white").pack(pady=2, padx=20)
        tk.Label(modal, text=f"Copias actuales: {copias}", font=("Arial", 10, "italic"), bg="white").pack(pady=(2, 10), padx=20)

        tk.Label(modal, text="Seleccione el motivo de la baja:", font=("Arial", 10, "bold"), bg="white").pack(pady=(5, 5), padx=20)

        motivo_var = tk.StringVar(value="Deterioro")
        motivos = ["Deterioro", "No aparece el libro", "Tiene muy poco movimiento"]
        for motivo in motivos:
            tk.Radiobutton(
                modal, text=motivo, variable=motivo_var, value=motivo,
                font=("Arial", 10), bg="white", anchor="w"
            ).pack(fill="x", padx=40, pady=2)

        frame_botones = tk.Frame(modal, bg="white")
        frame_botones.pack(pady=15)

        tk.Button(
            frame_botones, text="Confirmar baja", width=14,
            command=lambda: self.confirmar_baja(
                modal, seleccion[0], id_libro, nombre, editorial, autor, motivo_var.get()
            )
        ).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Cancelar", width=14, command=modal.destroy).grid(row=0, column=1, padx=10)

    def confirmar_baja(self, modal, item_grilla, id_libro, nombre, editorial, autor, motivo):
        """Resta una copia al libro y registra la baja con su motivo en el JSON de bajas."""
        respuesta = messagebox.askyesno(
            "Confirmar baja",
            f"¿Está seguro de dar de baja una copia del libro '{nombre}' por el motivo: '{motivo}'?",
            parent=modal
        )
        if not respuesta:
            return

        self.controller.gestion_libros.actualizar_copias(id_libro, -1)
        self.controller.gestion_libros_baja.registrar(id_libro, nombre, editorial, autor, motivo)

        # Refrescar la copia mostrada en la grilla con el valor actualizado
        valores = list(self.grilla.item(item_grilla, "values"))
        valores[4] = str(max(0, int(valores[4]) - 1))
        self.grilla.item(item_grilla, values=valores)

        modal.destroy()
        messagebox.showinfo("Éxito", f"Se dio de baja una copia del libro '{nombre}'.\nMotivo: {motivo}")