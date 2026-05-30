# Manual de Usuario — Sistema de Gestión de Biblioteca UDI

**Autores:** Juan Diego Contreras Melendez · Daniel Gomez Castellanos

---

## Tabla de contenido

1. [Requisitos del sistema](#1-requisitos-del-sistema)
2. [Cómo iniciar la aplicación](#2-cómo-iniciar-la-aplicación)
3. [Pantalla de Biblioteca](#3-pantalla-de-biblioteca)
   - [Registrar un libro](#31-registrar-un-libro)
   - [Editar un libro](#32-editar-un-libro)
   - [Eliminar un libro](#33-eliminar-un-libro)
   - [Buscar un libro](#34-buscar-un-libro)
   - [Mostrar todos los libros](#35-mostrar-todos-los-libros)
4. [Pantalla de Préstamos](#4-pantalla-de-préstamos)
   - [Registrar un préstamo](#41-registrar-un-préstamo)
   - [Ver detalle de un préstamo](#42-ver-detalle-de-un-préstamo)
   - [Devolver un libro](#43-devolver-un-libro)
5. [Indicadores de estado](#5-indicadores-de-estado)
6. [Persistencia de datos](#6-persistencia-de-datos)

---

## 1. Requisitos del sistema

- Python 3.12 o superior
- Módulo `tkinter` instalado (`sudo apt install python3-tk` en Linux)
- No requiere librerías externas adicionales

---

## 2. Cómo iniciar la aplicación

Desde la carpeta raíz del proyecto, ejecutar:

```bash
python3 main.py
```

La ventana principal se abre en la **Pantalla de Biblioteca**.

---

## 3. Pantalla de Biblioteca

Esta pantalla permite gestionar el catálogo de libros de la biblioteca.

### Campos del formulario

| Campo | Descripción | Límite |
|---|---|---|
| **Fecha de Ingreso** | Se asigna automáticamente con la fecha actual | Solo lectura |
| **ID Libro** | Identificador único del libro | Máximo 10 caracteres |
| **Nombre del Libro** | Título completo | Máximo 100 caracteres |
| **Editorial** | Casa editorial | Máximo 100 caracteres |
| **Autor** | Nombre del autor | Máximo 100 caracteres |
| **Número de Copias** | Cantidad disponible | Máximo 3 dígitos, solo números |

### Botones superiores

| Botón | Función |
|---|---|
| **Nuevo** | Guarda el libro ingresado en el formulario |
| **Editar** | Carga en el formulario el libro seleccionado en la tabla |
| **Guardar** | Confirma los cambios de una edición en curso |
| **Eliminar** | Elimina el libro seleccionado en la tabla |

### 3.1 Registrar un libro

1. Complete todos los campos del formulario (ID y Nombre son obligatorios).
2. Haga clic en **Nuevo**.
3. Confirme la operación en el diálogo que aparece.
4. El libro queda guardado y aparece en la tabla.

> El ID debe ser único. Si ya existe, el sistema mostrará un error y no guardará el registro.

### 3.2 Editar un libro

1. Haga clic en **Mostrar datos** para cargar los registros en la tabla.
2. Seleccione el libro que desea modificar haciendo clic sobre su fila.
3. Haga clic en **Editar** — los datos se copian al formulario.
4. Realice los cambios necesarios.
5. Haga clic en **Guardar** y confirme el diálogo.

### 3.3 Eliminar un libro

1. Seleccione el libro en la tabla.
2. Haga clic en **Eliminar**.
3. Confirme la operación en el diálogo.

> Si el libro tiene préstamos activos, asegúrese de gestionar las devoluciones antes de eliminarlo.

### 3.4 Buscar un libro

1. Escriba un término en el campo **BUSCAR (ID o Nombre)**.
2. Haga clic en **Buscar**.
3. La tabla mostrará solo los libros que coincidan (búsqueda insensible a mayúsculas).
4. Para volver a ver todos los registros, haga clic en **Mostrar datos**.

### 3.5 Mostrar todos los libros

Haga clic en **Mostrar datos** para leer el archivo JSON y mostrar todos los registros en la tabla.

### Botones inferiores

| Botón | Función |
|---|---|
| **Cancelar** | Limpia el formulario y cancela cualquier edición en curso |
| **Mostrar datos** | Carga todos los libros guardados en la tabla |
| **Salir** | Cierra la aplicación |
| **Préstamos** | Navega a la pantalla de gestión de préstamos |

---

## 4. Pantalla de Préstamos

Accesible desde el botón **Préstamos** en la pantalla de Biblioteca. Permite registrar y gestionar el préstamo de libros a estudiantes.

### 4.1 Registrar un préstamo

1. Ingrese el **Código del Estudiante** y su **Nombre y Apellidos** en los campos superiores.
2. En la tabla **LIBROS DISPONIBLES**, haga clic sobre el libro que desea prestar para seleccionarlo.
3. Haga clic en **Prestar**.

Al confirmar:
- El préstamo queda registrado en la tabla **PRÉSTAMOS REGISTRADOS**.
- El número de copias del libro se reduce en 1 automáticamente.
- La **fecha de devolución** se calcula automáticamente a **15 días** desde la fecha del préstamo.

> No se puede prestar un libro con 0 copias disponibles.

### 4.2 Ver detalle de un préstamo

Haga clic sobre cualquier fila de la tabla **PRÉSTAMOS REGISTRADOS** para abrir un modal con la información completa:

- ID y nombre del libro
- Nombre del estudiante
- Fecha de préstamo y fecha de devolución
- Estado visual (● Verde / ● Rojo)

### 4.3 Devolver un libro

1. Haga clic sobre el préstamo en la tabla para abrir el modal de detalle.
2. Si el préstamo está activo, aparecerá el botón **Devolver Libro**.
3. Haga clic en **Devolver Libro** y confirme la operación.

Al confirmar:
- El préstamo se elimina de la lista y del archivo JSON.
- Las copias del libro se restauran (+1).
- La tabla de libros disponibles se actualiza automáticamente.

### Botones de la pantalla de préstamos

| Botón | Función |
|---|---|
| **Prestar** | Registra el préstamo del libro seleccionado al estudiante indicado |
| **Cancelar** | Limpia los campos de código y nombre del estudiante |
| **Volver** | Regresa a la pantalla de Biblioteca |

---

## 5. Indicadores de estado

La columna **Estado** de la tabla de préstamos usa un círculo de color:

| Indicador | Significado |
|---|---|
| **● Verde** | El préstamo está dentro del plazo de devolución, o el libro ya fue devuelto |
| **● Rojo** | El préstamo está **vencido**: la fecha de devolución ya pasó y tiene días de multa |

El número de **días de multa** se calcula automáticamente al momento de la devolución según los días transcurridos desde la fecha límite.

---

## 6. Persistencia de datos

Todos los datos se guardan automáticamente en archivos JSON dentro de la carpeta `data/`:

| Archivo | Contenido |
|---|---|
| `data/libros.json` | Catálogo completo de libros con sus copias disponibles |
| `data/prestamos.json` | Préstamos activos pendientes de devolución |

No es necesario hacer ninguna acción manual para guardar — cada operación (crear, editar, eliminar, prestar, devolver) persiste inmediatamente en disco.
