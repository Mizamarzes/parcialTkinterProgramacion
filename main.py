# main.py
import tkinter as tk
from modules.biblioteca import BibliotecaPantalla
from model.Libro import GestionLibros 

class BibliotecaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA DE GESTIÓN DE BIBLIOTECA UDI")
        self.geometry("900x700")
        self.resizable(False, False)
        
        self.gestion_libros = GestionLibros()
        
        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        
        self.pantalla_biblioteca = BibliotecaPantalla(parent=self.contenedor, controller=self)
        self.pantalla_biblioteca.grid(row=0, column=0, sticky="nsew")
        
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        self.pantalla_biblioteca.actualizar_fecha()

if __name__ == "__main__":
    app = BibliotecaApp()
    app.mainloop()