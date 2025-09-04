from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Conexão com o banco
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
        bio TEXT
    )
''')
conn.commit()

import os

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- ROTAS ----------------

# Rota inicial -> página de login
@app.route('/')
def home():
    return render_template('index.html')

# Rota para cadastro etapa 1
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro1.html')

# Rota para cadastro etapa 2
@app.route('/cadastro2')
def cadastro2():
    option = request.args.get('option')  # Obtém a opção selecionada
    return render_template('cadastro2.html', option=option)

# Rota para cadastro etapa 3 (fotos, nome, idade, bio)
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

    # Salvar fotos (só os nomes por enquanto)
    fotos = []
    for i in range(1, 5):
        foto = request.files.get(f"foto{i}")
        if foto and foto.filename != "":
            caminho = f"static/uploads/{foto.filename}"
            foto.save(caminho)
            fotos.append(caminho)
        else:
            fotos.append(None)

    cursor.execute('''
        INSERT INTO usuarios (tipo, email, senha, nome, idade, bio, foto1, foto2, foto3, foto4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tipo, email, senha, nome, idade, bio, fotos[0], fotos[1], fotos[2], fotos[3]))
    conn.commit()

    return redirect(url_for('perfil', email=email))
    
# Rota de perfil
@app.route('/perfil')
def perfil():
    email = request.args.get('email')
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()

    return render_template('perfil.html', usuario=usuario)

# Rota para esqueci a senha
@app.route('/esqueci')
def esqueci():
    return render_template('esqueci.html')

# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
