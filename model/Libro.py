# modules/libro.py
import json
import os

class Libro:
    """Clase que representa la entidad de un Libro."""
    def __init__(self, id_libro, nombre, editorial, autor, copias, fecha):
        self.id = id_libro
        self.nombre = nombre
        self.editorial = editorial
        self.autor = autor
        self.copias = copias
        self.fecha = fecha


class GestionLibros:
    """Clase encargada de la lógica de negocio y almacenamiento en archivo JSON."""
    def __init__(self, archivo_json="data/libros.json"):
        self.archivo_json = archivo_json
        self.lista_libros = []
        # Cargar los datos guardados inmediatamente al iniciar la app
        self._cargar_desde_json()

    def _cargar_desde_json(self):
        """Lee el archivo JSON y reconstruye el array dinámico con objetos Libro."""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.lista_libros = [
                        Libro(item['id'], item['nombre'], item['editorial'], item['autor'], item['copias'], item['fecha'])
                        for item in datos
                    ]
            except Exception:
                self.lista_libros = []

    def _guardar_en_json(self):
        """Convierte el array dinámico a diccionarios y lo vuelca en el archivo JSON."""
        try:
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                # Convertimos la lista de objetos a una lista de diccionarios con __dict__
                datos_dict = [libro.__dict__ for libro in self.lista_libros]
                json.dump(datos_dict, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al escribir en el JSON: {e}")

    def guardar(self, nuevo_libro):
        """Agrega un nuevo libro al array y actualiza el JSON validando que el ID no se repita."""
        for libro in self.lista_libros:
            if libro.id == nuevo_libro.id:
                return False, f"Error: El ID '{nuevo_libro.id}' ya existe."
        
        self.lista_libros.append(nuevo_libro)
        self._guardar_en_json()  # Guardado persistente
        return True, "Libro guardado exitosamente."

    def editar(self, id_libro, nombre, editorial, autor, copias, fecha):
        """Busca un libro por su ID original, actualiza sus campos y lo guarda en el JSON."""
        for libro in self.lista_libros:
            if libro.id == id_libro:
                libro.nombre = nombre
                libro.editorial = editorial
                libro.autor = autor
                libro.copias = copias
                libro.fecha = fecha
                self._guardar_en_json()  # Guardado persistente
                return True, "Libro modificado exitosamente."
                
        return False, "Error: Libro no encontrado para editar."

    def eliminar(self, id_libro):
        """Elimina un libro del array dinámico y del archivo JSON buscando por su ID."""
        for libro in self.lista_libros:
            if libro.id == id_libro:
                self.lista_libros.remove(libro)
                self._guardar_en_json()  # Guardado persistente
                return True, "Libro eliminado exitosamente."
                
        return False, "Error: Libro no encontrado para eliminar."

    def obtener_todos(self):
        """Asegura traer la versión más fresca del JSON y devuelve todos los libros."""
        self._cargar_desde_json()
        return self.lista_libros