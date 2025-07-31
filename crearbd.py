import sqlite3

conn = sqlite3.connect('presupuesto.db')
c = conn.cursor()

# Crear tabla de usuarios si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
''')

# (Opcional) Crear también tablas de ingresos y egresos si no están
c.execute('''
    CREATE TABLE IF NOT EXISTS ingresos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        descripcion TEXT,
        monto REAL,
        categoria TEXT,
        usuario_id INTEGER
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS egresos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        descripcion TEXT,
        monto REAL,
        categoria TEXT,
        usuario_id INTEGER
    )
''')

conn.commit()
conn.close()

print("✔ Base de datos creada correctamente.")
