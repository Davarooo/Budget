from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

DB_NAME = 'presupuesto.db'

# Crear base de datos y tabla de usuarios y movimientos
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo TEXT,
            cantidad REAL,
            descripcion TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT tipo, cantidad, descripcion FROM movimientos WHERE usuario_id = ?", (session['usuario_id'],))
    movimientos = c.fetchall()
    conn.close()

    ingresos = [m for m in movimientos if m[0] == 'ingreso']
    egresos = [m for m in movimientos if m[0] == 'egreso']
    total_ingresos = sum(m[1] for m in ingresos)
    total_egresos = sum(m[1] for m in egresos)
    balance = total_ingresos - total_egresos

    return render_template('index.html', ingresos=ingresos, egresos=egresos,
                           total_ingresos=total_ingresos, total_egresos=total_egresos,
                           balance=balance)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id FROM usuarios WHERE correo = ? AND contrasena = ?", (correo, contrasena))
        usuario = c.fetchone()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get('nuevo_correo')
        contrasena = request.form.get('nueva_contrasena')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO usuarios (correo, contrasena) VALUES (?, ?)", (correo, contrasena))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='El correo ya está registrado')
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

@app.route('/agregar', methods=['POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    tipo = request.form['tipo']
    cantidad_str = request.form['cantidad'].replace('.', '').replace(',', '.')
    try:
        cantidad = float(cantidad_str)
    except ValueError:
        return redirect(url_for('index'))
    descripcion = request.form['descripcion']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO movimientos (usuario_id, tipo, cantidad, descripcion) VALUES (?, ?, ?, ?)",
              (session['usuario_id'], tipo, cantidad, descripcion))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
