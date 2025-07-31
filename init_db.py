import sqlite3
import os

DB_FILE = 'presupuesto.db'

# Eliminar base de datos anterior si existe
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Base de datos anterior eliminada.")

# Crear nueva base de datos con las columnas necesarias
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Tabla de usuarios
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Tabla de movimientos
cursor.execute('''
CREATE TABLE movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    categoria TEXT,
    tipo TEXT CHECK(tipo IN ('ingreso', 'egreso')) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES usuarios(id)
)
''')

conn.commit()
conn.close()
print("Nueva base de datos creada con éxito.")
