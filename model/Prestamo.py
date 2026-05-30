import json
import os
from datetime import datetime


class Prestamo:
    def __init__(self, codigo_estudiante, nombre_estudiante, id_libro, nombre_libro,
                 cantidad, fecha_prestamo, fecha_devolucion, dias_multa, estado):
        self.codigo_estudiante = codigo_estudiante
        self.nombre_estudiante = nombre_estudiante
        self.id_libro = id_libro
        self.nombre_libro = nombre_libro
        self.cantidad = cantidad
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.dias_multa = dias_multa
        self.estado = estado


class GestionPrestamos:
    def __init__(self, archivo_json="data/prestamos.json"):
        self.archivo_json = archivo_json
        self.lista_prestamos = []
        self._cargar_desde_json()

    def _cargar_desde_json(self):
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.lista_prestamos = [
                        Prestamo(
                            item['codigo_estudiante'], item['nombre_estudiante'],
                            item['id_libro'], item['nombre_libro'], item['cantidad'],
                            item['fecha_prestamo'], item['fecha_devolucion'],
                            item['dias_multa'], item['estado']
                        )
                        for item in datos
                    ]
            except Exception:
                self.lista_prestamos = []

    def _guardar_en_json(self):
        try:
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                json.dump([p.__dict__ for p in self.lista_prestamos], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al escribir en el JSON: {e}")

    def registrar(self, nuevo_prestamo):
        self.lista_prestamos.append(nuevo_prestamo)
        self._guardar_en_json()
        return True, "Préstamo registrado exitosamente."

    def devolver(self, codigo_estudiante, id_libro):
        for prestamo in self.lista_prestamos:
            if (prestamo.codigo_estudiante == codigo_estudiante and
                    prestamo.id_libro == id_libro and
                    prestamo.estado == "Activo"):
                try:
                    fecha_d = datetime.strptime(prestamo.fecha_devolucion, "%d/%m/%Y")
                    hoy = datetime.now()
                    prestamo.dias_multa = str(max(0, (hoy.date() - fecha_d.date()).days)) if hoy.date() > fecha_d.date() else "0"
                except Exception:
                    prestamo.dias_multa = "0"
                prestamo.estado = "Inactivo"
                self._guardar_en_json()
                return True, "Devolución registrada exitosamente."
        return False, "No se encontró un préstamo activo con esos datos."

    def eliminar(self, codigo_estudiante, id_libro):
        """Elimina el préstamo activo del array y del JSON."""
        for prestamo in self.lista_prestamos:
            if (prestamo.codigo_estudiante == codigo_estudiante and
                    prestamo.id_libro == id_libro and
                    prestamo.estado == "Activo"):
                self.lista_prestamos.remove(prestamo)
                self._guardar_en_json()
                return True, "Préstamo eliminado correctamente."
        return False, "No se encontró un préstamo activo con esos datos."

    def obtener_todos(self):
        self._cargar_desde_json()
        return self.lista_prestamos