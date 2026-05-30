# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Desktop library management system ("Sistema de Gestión de Biblioteca UDI") built with Python and Tkinter. Authors: Juan Diego Contreras Melendez & Daniel Gomez Castellanos.

## Running the app

```bash
python main.py
```

No external dependencies beyond the Python standard library (tkinter, json, os, datetime).

## Architecture

The app follows a simple MVC-like structure with three layers:

**Controller / Root** — `main.py`
- `BibliotecaApp(tk.Tk)` is the application root. It owns the `GestionLibros` instance (model) and passes itself as `controller` to the view. The view accesses the model exclusively via `self.controller.gestion_libros`.

**Model** — `model/Libro.py`
- `Libro`: plain data object (id, nombre, editorial, autor, copias, fecha).
- `GestionLibros`: owns `lista_libros` (in-memory list) and `data/libros.json` (persistent store). Every mutating operation (`guardar`, `editar`, `eliminar`) immediately calls `_guardar_en_json()`. `obtener_todos()` re-reads the JSON before returning, so the view always gets fresh data.

**View** — `modules/biblioteca.py`
- `BibliotecaPantalla(tk.Frame)`: single-screen UI containing the input form, action buttons (Nuevo/Editar/Guardar/Eliminar), a search bar, and a `ttk.Treeview` grid. Edit mode is tracked via `self.fila_en_edicion` (the selected Treeview item ID, or `None` when creating).

**Data** — `data/libros.json`
- Flat JSON array of book objects. This file is the sole persistent store; no database.

## Key behaviors to know

- **Duplicate ID check** happens in two places: in `GestionLibros.guardar()` (checks `lista_libros`) and again in `BibliotecaPantalla.guardar_cambios_dialogo()` (checks the Treeview). They must stay in sync.
- **"Mostrar datos"** clears the Treeview and repopulates it from the JSON file — it is the canonical way to refresh the grid. CRUD operations update the Treeview in-place without a full reload.
- **Search** filters the full JSON list and replaces the current Treeview contents; pressing "Cancelar" clears the search field but does not restore the full list automatically (user must press "Mostrar datos").
- Field limits: ID ≤ 10 chars, text fields ≤ 100 chars, copias ≤ 3 digits (numeric-only via `validatecommand`).