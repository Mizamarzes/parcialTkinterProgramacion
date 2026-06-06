# model/LibrosBaja.py
import json
import os
from datetime import datetime


class LibroBaja:
    """Clase que representa un libro al que se le dio de baja una copia y el motivo."""
    def __init__(self, id_libro, nombre, editorial, autor, motivo, fecha_baja):
        self.id = id_libro
        self.nombre = nombre
        self.editorial = editorial
        self.autor = autor
        self.motivo = motivo
        self.fecha_baja = fecha_baja


class GestionLibrosBaja:
    """Clase encargada de la lógica y el almacenamiento de los libros dados de baja."""
    def __init__(self, archivo_json="data/libros_baja.json"):
        self.archivo_json = archivo_json
        self.lista_bajas = []
        self._cargar_desde_json()

    def _cargar_desde_json(self):
        """Lee el archivo JSON y reconstruye el array dinámico con objetos LibroBaja."""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.lista_bajas = [
                        LibroBaja(
                            item['id'], item['nombre'], item['editorial'],
                            item['autor'], item['motivo'], item['fecha_baja']
                        )
                        for item in datos
                    ]
            except Exception:
                self.lista_bajas = []

    def _guardar_en_json(self):
        """Convierte el array dinámico a diccionarios y lo vuelca en el archivo JSON."""
        try:
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                json.dump([b.__dict__ for b in self.lista_bajas], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al escribir en el JSON: {e}")

    def registrar(self, id_libro, nombre, editorial, autor, motivo):
        """Registra una baja de copia para un libro con su motivo y la fecha actual."""
        nueva_baja = LibroBaja(
            id_libro, nombre, editorial, autor, motivo,
            datetime.now().strftime("%d/%m/%Y")
        )
        self.lista_bajas.append(nueva_baja)
        self._guardar_en_json()
        return True, "Baja registrada exitosamente."

    def obtener_todos(self):
        """Asegura traer la versión más fresca del JSON y devuelve todas las bajas."""
        self._cargar_desde_json()
        return self.lista_bajas

    def contar_por_motivo(self):
        """Devuelve un diccionario {motivo: cantidad} con las bajas agrupadas por motivo."""
        self._cargar_desde_json()
        conteo = {}
        for baja in self.lista_bajas:
            conteo[baja.motivo] = conteo.get(baja.motivo, 0) + 1
        return conteo