import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from model.Prestamo import Prestamo


class PrestamosPantalla(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        # Guarda el estado real del modelo por item_id para saber si aún es Activo
        self._estado_modelo = {}

        tk.Label(self, text="SISTEMA DE PRÉSTAMOS DE BIBLIOTECA UDI",
                 font=("Arial", 14, "bold"), bg="white").pack(pady=(10, 5))

        # --- FORMULARIO ---
        frame_form = tk.Frame(self, bg="white")
        frame_form.pack(padx=20, pady=5)

        tk.Label(frame_form, text="CÓDIGO ESTUDIANTE", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=3)
        self.ent_codigo = tk.Entry(frame_form, font=("Arial", 10), width=20)
        self.ent_codigo.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(frame_form, text="NOMBRES Y APELLIDOS", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=2, sticky="w", pady=3, padx=(20, 0))
        self.ent_nombre = tk.Entry(frame_form, font=("Arial", 10), width=30)
        self.ent_nombre.grid(row=0, column=3, sticky="w", padx=5)

        # --- TABLA LIBROS ---
        tk.Label(self, text="LIBROS DISPONIBLES", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=20, pady=(5, 0))

        frame_libros = tk.Frame(self)
        frame_libros.pack(padx=20, pady=(3, 0), fill="x")

        cols_libros = ("id_libro", "nombre_libro", "num_copias")
        self.tabla_libros = ttk.Treeview(frame_libros, columns=cols_libros, show="headings", height=4)
        self.tabla_libros.heading("id_libro", text="Id Libro")
        self.tabla_libros.heading("nombre_libro", text="Nombre Libro")
        self.tabla_libros.heading("num_copias", text="Num. Copias")
        self.tabla_libros.column("id_libro", width=80, anchor="center")
        self.tabla_libros.column("nombre_libro", width=500, anchor="w")
        self.tabla_libros.column("num_copias", width=100, anchor="center")

        scroll_libros = ttk.Scrollbar(frame_libros, orient="vertical", command=self.tabla_libros.yview)
        self.tabla_libros.configure(yscrollcommand=scroll_libros.set)
        self.tabla_libros.pack(side="left", fill="x", expand=True)
        scroll_libros.pack(side="right", fill="y")

        # --- BOTONES (debajo de tabla libros) ---
        frame_botones = tk.Frame(self, bg="white")
        frame_botones.pack(pady=8)

        tk.Button(frame_botones, text="Prestar", width=10, command=self.registrar_prestamo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Cancelar", width=10, command=self.limpiar_cajas).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Volver", width=10,
                  command=lambda: controller.mostrar_pantalla("biblioteca")).grid(row=0, column=2, padx=5)

        # --- TABLA PRÉSTAMOS ---
        tk.Label(self, text="PRÉSTAMOS REGISTRADOS  (clic para ver detalle)",
                 font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=20, pady=(5, 0))

        frame_prestamos = tk.Frame(self)
        frame_prestamos.pack(padx=20, pady=(3, 10), fill="both", expand=True)

        cols_prestamos = ("cod_est", "nombre_est", "id_libro", "nombre_libro",
                          "cantidad", "fecha_prestamo", "fecha_devolucion", "dias_multa", "estado")
        self.tabla_prestamos = ttk.Treeview(frame_prestamos, columns=cols_prestamos, show="headings", height=7)

        self.tabla_prestamos.heading("cod_est", text="Cód. Estudiante")
        self.tabla_prestamos.heading("nombre_est", text="Nombre")
        self.tabla_prestamos.heading("id_libro", text="Id Libro")
        self.tabla_prestamos.heading("nombre_libro", text="Nombre Libro")
        self.tabla_prestamos.heading("cantidad", text="Cantidad")
        self.tabla_prestamos.heading("fecha_prestamo", text="F. Préstamo")
        self.tabla_prestamos.heading("fecha_devolucion", text="F. Devolución")
        self.tabla_prestamos.heading("dias_multa", text="Días Multa")
        self.tabla_prestamos.heading("estado", text="Estado")

        self.tabla_prestamos.column("cod_est", width=100, anchor="center")
        self.tabla_prestamos.column("nombre_est", width=140, anchor="w")
        self.tabla_prestamos.column("id_libro", width=65, anchor="center")
        self.tabla_prestamos.column("nombre_libro", width=145, anchor="w")
        self.tabla_prestamos.column("cantidad", width=60, anchor="center")
        self.tabla_prestamos.column("fecha_prestamo", width=85, anchor="center")
        self.tabla_prestamos.column("fecha_devolucion", width=90, anchor="center")
        self.tabla_prestamos.column("dias_multa", width=75, anchor="center")
        self.tabla_prestamos.column("estado", width=70, anchor="center")

        # Rojo = vencido (se pasó la fecha), Verde = al día o ya devuelto
        self.tabla_prestamos.tag_configure("rojo", foreground="red")
        self.tabla_prestamos.tag_configure("verde", foreground="green")

        self.tabla_prestamos.bind("<ButtonRelease-1>", self.abrir_modal_prestamo)

        scroll_prestamos = ttk.Scrollbar(frame_prestamos, orient="vertical", command=self.tabla_prestamos.yview)
        self.tabla_prestamos.configure(yscrollcommand=scroll_prestamos.set)
        self.tabla_prestamos.pack(side="left", fill="both", expand=True)
        scroll_prestamos.pack(side="right", fill="y")

    # ------------------------------------------------------------------

    def _calcular_indicador(self, estado_modelo, fecha_devolucion_str):
        """Devuelve (texto_estado, tag) según si el préstamo está vencido o no."""
        if estado_modelo == "Inactivo":
            return "●", "verde"
        try:
            fecha_d = datetime.strptime(fecha_devolucion_str, "%d/%m/%Y")
            if datetime.now().date() > fecha_d.date():
                return "●", "rojo"
        except Exception:
            pass
        return "●", "verde"

    # ------------------------------------------------------------------

    def cargar_libros(self):
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)
        for libro in self.controller.gestion_libros.obtener_todos():
            self.tabla_libros.insert("", "end", values=(libro.id, libro.nombre, libro.copias))

    def cargar_prestamos(self):
        for item in self.tabla_prestamos.get_children():
            self.tabla_prestamos.delete(item)
        self._estado_modelo.clear()
        for p in self.controller.gestion_prestamos.obtener_todos():
            indicador, tag = self._calcular_indicador(p.estado, p.fecha_devolucion)
            iid = self.tabla_prestamos.insert("", "end", values=(
                p.codigo_estudiante, p.nombre_estudiante, p.id_libro,
                p.nombre_libro, p.cantidad, p.fecha_prestamo,
                p.fecha_devolucion, p.dias_multa, indicador
            ), tags=(tag,))
            self._estado_modelo[iid] = p.estado

    def limpiar_cajas(self):
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)

    # ------------------------------------------------------------------

    def registrar_prestamo(self):
        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()

        if not codigo or not nombre:
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese el código y nombre del estudiante.")
            return

        seleccion = self.tabla_libros.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un libro de la tabla.")
            return

        valores = self.tabla_libros.item(seleccion[0], "values")
        id_libro, nombre_libro, copias = valores[0], valores[1], valores[2]

        if int(copias) <= 0:
            messagebox.showerror("Sin copias", "No hay copias disponibles de este libro.")
            return

        hoy = datetime.now()
        fecha_prestamo = hoy.strftime("%d/%m/%Y")
        fecha_devolucion = (hoy + timedelta(days=15)).strftime("%d/%m/%Y")

        nuevo = Prestamo(codigo, nombre, id_libro, nombre_libro, "1",
                         fecha_prestamo, fecha_devolucion, "0", "Activo")
        self.controller.gestion_prestamos.registrar(nuevo)

        # Préstamo nuevo siempre es verde (fecha_devolucion es en 15 días)
        iid = self.tabla_prestamos.insert("", "end", values=(
            codigo, nombre, id_libro, nombre_libro, "1",
            fecha_prestamo, fecha_devolucion, "0", "●"
        ), tags=("verde",))
        self._estado_modelo[iid] = "Activo"

        messagebox.showinfo("Éxito", "Préstamo registrado exitosamente.")
        self.limpiar_cajas()

    # ------------------------------------------------------------------

    def abrir_modal_prestamo(self, event):
        seleccion = self.tabla_prestamos.selection()
        if not seleccion:
            return

        item_id = seleccion[0]
        valores = self.tabla_prestamos.item(item_id, "values")
        estado_modelo = self._estado_modelo.get(item_id, "Inactivo")

        modal = tk.Toplevel(self)
        modal.title("Detalle del Préstamo")
        modal.geometry("380x260")
        modal.resizable(False, False)
        modal.configure(bg="white")
        modal.update_idletasks()
        modal.grab_set()

        tk.Label(modal, text="DETALLE DEL PRÉSTAMO", font=("Arial", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=(15, 10))

        campos = [
            ("ID LIBRO", valores[2]),
            ("NOMBRE LIBRO", valores[3]),
            ("ESTUDIANTE", valores[1]),
            ("FECHA PRÉSTAMO", valores[5]),
            ("FECHA DEVOLUCIÓN", valores[6]),
        ]
        for i, (label, valor) in enumerate(campos, start=1):
            tk.Label(modal, text=label + ":", font=("Arial", 9, "bold"), bg="white", anchor="e", width=16).grid(
                row=i, column=0, sticky="e", padx=(15, 5), pady=3)
            tk.Label(modal, text=valor, font=("Arial", 9), bg="#e0e0e0", width=22,
                     relief="sunken", anchor="w").grid(row=i, column=1, sticky="w", padx=(0, 15), pady=3)

        # Determinar color del estado en el modal
        _, tag = self._calcular_indicador(estado_modelo, valores[6])
        color_estado = "red" if tag == "rojo" else "green"
        texto_estado = "● Rojo (Vencido)" if tag == "rojo" else "● Verde"

        tk.Label(modal, text="ESTADO:", font=("Arial", 9, "bold"), bg="white", anchor="e", width=16).grid(
            row=len(campos) + 1, column=0, sticky="e", padx=(15, 5), pady=3)
        tk.Label(modal, text=texto_estado, font=("Arial", 9, "bold"), fg=color_estado, bg="white").grid(
            row=len(campos) + 1, column=1, sticky="w", padx=(0, 15), pady=3)

        frame_btn = tk.Frame(modal, bg="white")
        frame_btn.grid(row=len(campos) + 2, column=0, columnspan=2, pady=12)

        if estado_modelo == "Activo":
            tk.Button(frame_btn, text="Marcar Inactivo", width=14,
                      command=lambda: self._devolver_desde_modal(item_id, valores, modal)).pack(side="left", padx=8)

        tk.Button(frame_btn, text="Cerrar", width=10, command=modal.destroy).pack(side="left", padx=8)

    def _devolver_desde_modal(self, item_id, valores, modal):
        if not messagebox.askyesno("Confirmar devolución", "¿Confirmar la devolución del libro?", parent=modal):
            return

        exito, msg = self.controller.gestion_prestamos.devolver(valores[0], valores[2])
        if exito:
            try:
                fecha_d = datetime.strptime(valores[6], "%d/%m/%Y")
                hoy = datetime.now()
                dias_multa = str(max(0, (hoy.date() - fecha_d.date()).days)) if hoy.date() > fecha_d.date() else "0"
            except Exception:
                dias_multa = "0"

            nuevos_valores = list(valores)
            nuevos_valores[7] = dias_multa
            nuevos_valores[8] = "●"
            self.tabla_prestamos.item(item_id, values=nuevos_valores, tags=("verde",))
            self._estado_modelo[item_id] = "Inactivo"
            messagebox.showinfo("Éxito", msg, parent=modal)
            modal.destroy()
        else:
            messagebox.showerror("Error", msg, parent=modal)