import sqlite3

# Conecta (vai criar de novo se não existir)
conn = sqlite3.connect("vemka.db")
cursor = conn.cursor()

# Criação da tabela com todos os campos necessários
cursor.execute('''
CREATE TABLE usuarios (
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
conn.close()

print("Banco criado com sucesso!")
