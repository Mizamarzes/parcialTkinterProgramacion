# Sistema de Gestión de Biblioteca UDI

Aplicación de escritorio para la gestión de libros y préstamos de una biblioteca universitaria, desarrollada con Python y Tkinter.

**Autores:** Juan Diego Contreras Melendez · Daniel Gomez Castellanos

---

## Requisitos

- Python 3.12+
- Tkinter: `sudo apt install python3-tk` (Linux)

## Iniciar la aplicación

```bash
python3 main.py
```

---

## Funcionalidades principales

**Gestión de libros**
- Registrar, editar y eliminar libros del catálogo
- Búsqueda por ID o nombre (insensible a mayúsculas)
- Datos persistidos automáticamente en `data/libros.json`

**Gestión de préstamos**
- Registrar préstamos asociando un libro a un estudiante
- Al prestar, las copias disponibles se reducen automáticamente
- Al devolver, las copias se restauran y el préstamo se elimina del registro
- Fecha de devolución calculada a 15 días desde el préstamo
- Indicador visual de estado: **● Verde** (vigente) / **● Rojo** (vencido)

---

## Estructura del proyecto

```
├── main.py               # Punto de entrada y controlador principal
├── model/
│   ├── Libro.py          # Modelo y lógica de negocio de libros
│   └── Prestamo.py       # Modelo y lógica de negocio de préstamos
├── modules/
│   ├── biblioteca.py     # Pantalla de gestión de libros
│   └── prestamos.py      # Pantalla de gestión de préstamos
├── data/
│   ├── libros.json       # Almacenamiento de libros
│   └── prestamos.json    # Almacenamiento de préstamos activos
└── MANUAL_USUARIO.md     # Manual de usuario completo
```

---

Para instrucciones detalladas de uso, consulte el [Manual de Usuario](MANUAL_USUARIO.md).
