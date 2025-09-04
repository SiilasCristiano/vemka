import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import sqlite3

# ---------------- GARANTIR PASTA DE UPLOAD ----------------
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # cria a pasta se não existir

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- CONEXÃO COM BANCO ----------------
conn = sqlite3.connect("vemka.db", check_same_thread=False)
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        nome TEXT,
        idade INTEGER,
        bio TEXT,
        foto1 TEXT,
        foto2 TEXT,
        foto3 TEXT,
        foto4 TEXT
    )
''')
conn.commit()

# ---------------- ROTAS ----------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro1.html')

@app.route('/cadastro2')
def cadastro2():
    option = request.args.get('option')
    return render_template('cadastro2.html', option=option)

@app.route('/cadastro3')
def cadastro3():
    return render_template('cadastro3.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    tipo = request.form.get('tipo')
    email = request.form.get('email')
    senha = request.form.get('senha')
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    bio = request.form.get('bio')

    # Salvar fotos
    fotos = []
    for i in range(1, 5):
        foto = request.files.get(f"foto{i}")
        if foto and foto.filename:
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], foto.filename)
            foto.save(caminho)
            fotos.append(f"/static/uploads/{foto.filename}")  # caminho relativo para usar no HTML
        else:
            fotos.append(None)

    cursor.execute('''
        INSERT INTO usuarios (tipo, email, senha, nome, idade, bio, foto1, foto2, foto3, foto4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, email, senha, nome, idade, bio, fotos[0], fotos[1], fotos[2], fotos[3]))
    conn.commit()

    return redirect(url_for('perfil', email=email))

@app.route('/perfil')
def perfil():
    email = request.args.get('email')
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    return render_template('perfil.html', usuario=usuario)

@app.route('/esqueci')
def esqueci():
    return render_template('esqueci.html')

# ---------------- MAIN ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # usa a porta do Render ou 3000 localmente
    app.run(host='0.0.0.0', port=port, debug=True)
