import tkinter as tk
from modules.biblioteca import BibliotecaPantalla
from modules.prestamos import PrestamosPantalla
from model.Libro import GestionLibros
from model.Prestamo import GestionPrestamos
from model.LibrosBaja import GestionLibrosBaja

class BibliotecaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA DE GESTIÓN DE BIBLIOTECA UDI")
        self.geometry("900x700")
        self.resizable(False, False)

        self.gestion_libros = GestionLibros()
        self.gestion_prestamos = GestionPrestamos()
        self.gestion_libros_baja = GestionLibrosBaja()

        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.pantalla_biblioteca = BibliotecaPantalla(parent=self.contenedor, controller=self)
        self.pantalla_biblioteca.grid(row=0, column=0, sticky="nsew")

        self.pantalla_prestamos = PrestamosPantalla(parent=self.contenedor, controller=self)
        self.pantalla_prestamos.grid(row=0, column=0, sticky="nsew")

        self.mostrar_pantalla("biblioteca")
        self.pantalla_biblioteca.actualizar_fecha()

    def mostrar_pantalla(self, nombre):
        if nombre == "biblioteca":
            self.pantalla_biblioteca.tkraise()
        elif nombre == "prestamos":
            self.pantalla_prestamos.tkraise()
            self.pantalla_prestamos.cargar_libros()
            self.pantalla_prestamos.cargar_prestamos()

if __name__ == "__main__":
    app = BibliotecaApp()
    app.mainloop()
